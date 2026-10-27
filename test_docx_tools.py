import docx
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

print("Testing python-docx XML manipulation capabilities...")
doc = docx.Document()
p = doc.add_paragraph("Hello world")
shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="E7E6E6"/>')
print("Parsed XML successfully:", shd.tag)
