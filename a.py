from hayagriva import check_csl, reference

csl = """
<style
      xmlns="http://purl.org/net/xbiblio/csl"
      class="note"
      version="1.0">
  <info>
    <id />
    <title />
    <updated>2009-08-10T04:49:00+09:00</updated>
  </info>
  <citation>
    <layout>
      <number variable="page"/>
    </layout>
  </citation>
  <bibliography>
    <layout>
      <text value="Title: "/>
      <text variable="title"/>
    </layout>
  </bibliography>
</style>
"""

entries = """
[
    {
        "id": "ITEM-1",
        "page": "22-45",
        "title": "His Anonymous Life",
        "type": "book"
    },
    {
        "id": "ITEM-1",
        "page": "22-45",
        "title": "Title",
        "type": "article"
    }
]
"""

print(check_csl(csl))
print(reference(entries, csl))
