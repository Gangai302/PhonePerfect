import docx

doc = docx.Document(r"C:\Users\nisha\Downloads\docsphere.docx")

p = doc.paragraphs[32] # 1  INTRODUCTION\t1
pPr = p._p.pPr
print("P32 text:", repr(p.text))
tabs = pPr.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tabs")
if tabs is not None:
    for tab in tabs:
        print("Tab:", tab.attrib)
else:
    print("No tabs in pPr directly, checking style...")
    spPr = p.style._element.pPr
    if spPr is not None:
        stabs = spPr.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tabs")
        if stabs is not None:
            for tab in stabs:
                print("Style Tab:", tab.attrib)
