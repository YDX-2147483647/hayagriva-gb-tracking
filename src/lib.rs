use pyo3::prelude::*;

use hayagriva::archive::locales;
use hayagriva::citationberg::{IndependentStyle, json as csl_json};
use hayagriva::{BibliographyDriver, BibliographyRequest, CitationItem, CitationRequest};

/// Checks if a CSL style is considered malformed by hayagriva.
///
/// Returns the error message if considered malformed, and returns `None` otherwise.
#[pyfunction]
fn check_csl(csl: &str) -> Option<String> {
    IndependentStyle::from_xml(csl)
        .map(|_| None)
        .unwrap_or_else(|e| Some(format!("CSL file malformed: {:?}", e)))
}

fn warn_hacky_entries(entries: &[csl_json::Item]) {
    let hacky_entries: Vec<_> = entries
        .iter()
        .filter_map(|x| {
            if x.may_have_hack() {
                Some((
                    x.id().unwrap_or_default(),
                    x.0.get("note")?.to_str().unwrap_or_default(),
                ))
            } else {
                None
            }
        })
        .collect();
    if !hacky_entries.is_empty() {
        eprintln!(
            "These entries may contain cheater data in their note fields, which will be ignored in most cases: {:#?}",
            hacky_entries
        );
    }
}

/// Format a bibliography of all entries.
///
/// At present, the support for CSL is still quite limited. Therefore, this function returns tab-separated plain text rather than stylized HTML.
#[pyfunction]
fn reference(entires: &str, style: &str) -> PyResult<String> {
    let style = IndependentStyle::from_xml(style).map_err(|e| {
        pyo3::exceptions::PyValueError::new_err(format!("CSL file malformed: {:?}", e))
    })?;

    let entries: Vec<csl_json::Item> = serde_json::from_str(entires).map_err(|e| {
        pyo3::exceptions::PyValueError::new_err(format!("CSL-JSON file malformed: {:?}", e))
    })?;
    warn_hacky_entries(&entries);

    let locales = locales();

    let mut driver: BibliographyDriver<'_, csl_json::Item> = BibliographyDriver::new();

    driver.citation(CitationRequest::new(
        entries.iter().map(CitationItem::with_entry).collect(),
        &style,
        None,
        &locales,
        Some(1),
    ));

    let result = driver.finish(BibliographyRequest {
        style: &style,
        locale: None,
        locale_files: &locales,
    });

    let mut output = String::new();
    for row in result.bibliography.map(|b| b.items).unwrap_or_default() {
        if let Some(prefix) = row.first_field {
            output.push_str(&format!("{prefix:#}\t"));
        }
        output.push_str(&format!("{:#}\n", row.content));
    }
    Ok(output)
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
#[pyo3(name = "hayagriva")]
fn hayagriva_py(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(reference, m)?)?;
    m.add_function(wrap_pyfunction!(check_csl, m)?)?;

    Ok(())
}
