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

/// Format a bibliography of all entries.
#[pyfunction]
fn reference(entires: &str, style: &str) -> PyResult<String> {
    let style = IndependentStyle::from_xml(style).map_err(|e| {
        pyo3::exceptions::PyValueError::new_err(format!("CSL parse error: {:?}", e))
    })?;
    let entries: Vec<csl_json::Item> = serde_json::from_str(entires).map_err(|e| {
        pyo3::exceptions::PyValueError::new_err(format!("Input JSON parse error: {:?}", e))
    })?;

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
            output.push_str(&format!("{prefix:#}\n"));
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
