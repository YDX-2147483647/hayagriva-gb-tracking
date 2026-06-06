def parse-md-fixture [file: path] {
  let md = open $file --raw | from md --verbose

  let url = $md | where type == list | get children.0.1.attrs.url | str replace '/blob/' '/raw/'

  let code = $md | where {|x| $x.type == "code" and $x.attrs.lang == "diff" } | first
  let patch = if $code == null { null } else {
    ($code | get attrs.value | str replace "\n\n" "\n \n") + "\n"
    # The space will fix the _malformed patch_ error
  }

  { name: $"($file | path parse | get stem).bib", url: $url, patch: $patch }
}

# Setup the cache of fixtures/*.md
def main []: nothing -> nothing {
  cd ($env.CURRENT_FILE | path dirname)

  let cache_dir = "../target/bib-interop-cache"
  mkdir $cache_dir

  for $file in (ls ./fixtures/*.md) {
    let fixture = parse-md-fixture $file.name
    let cache = [$cache_dir, $fixture.name] | path join
    if ($cache | path exists) {
      print $"👌 Skip ($fixture.name) because it has already existed."
    } else {
      print $"Setting up ($fixture.name)… \(($fixture.url) → ($cache)\)"
      http get $fixture.url | save $cache

      if $fixture.patch != null {
        $fixture.patch | patch --directory $cache_dir
        print $"✅ Downloaded and patched ($fixture.name)."
      } else {
        print $"✅ Downloaded ($fixture.name)."
      }
    }
  }

  cd -
}
