def biblatex_to_hayagriva []: string -> record {
  $in | uv run python -c 'from sys import stdin; from hayagriva import biblatex_to_hayagriva; print(biblatex_to_hayagriva(stdin.read()))' | from yaml
}

# Panic if `expr` is no longer `false`
def check [bib: string, expr: string]: nothing -> nothing {
	let converted = $bib | biblatex_to_hayagriva
	let converted = if ($converted | values | length) == 1 {
		$converted | values | first
	} else { $converted }
	let converted = $converted | to yaml

	try {
		let _ = $"
		#let converted = yaml\(bytes\(sys.inputs.converted))
		($expr)
		" | typst compile --input $"converted=($converted)" - - --format svg
	} catch { |err|
		let msg = $"This claim is no longer true:
```bib
($bib)
```
```yaml
($converted)
```
```typst
($expr)
```"
 		error make { msg: $msg, inner: [$err] }
	}
}

# Check the claims in result.md
def main [] {
  cd ($env.CURRENT_FILE | path dirname)
	
	let code_blocks = open result.md | where {|x| $x.type == "code" and $x.attrs.lang in ["bib", "typst"] } | get attrs
	let claims = $code_blocks | enumerate | where item.lang == typst | get index | each {|expr_index|
		let bib = $code_blocks | get ($expr_index - 1) | get value
		let expr = $code_blocks | get $expr_index | get value
		{bib: $bib, expr: $expr}
	}
	$claims | par-each {|c| check $c.bib $c.expr }

  cd -
}
