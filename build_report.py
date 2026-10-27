"""
PhonePerfect Project Report Builder
Reads report data modules and modifies the cloned Word document in-place.
"""
import os
import shutil
import docx
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

from report_prelims import PRELIMINARY
from report_lists import TOC_ITEMS, LOF_ITEMS, LOT_ITEMS, ABBREVIATIONS
from report_tables import (
    TABLE_2_1, TABLE_5_1, TABLE_6_1, TABLE_6_2,
    TABLE_7_1, TABLE_7_2, TABLE_7_3, TABLE_7_4, TABLE_7_5
)
from report_figures import FIGURE_BOXES
from report_chap1_4 import CHAPTER_1, CHAPTER_2, CHAPTER_3, CHAPTER_4
from report_chap5_8 import CHAPTER_5, CHAPTER_6, CHAPTER_7, CHAPTER_8, REFERENCES_LIST

TEMPLATE_DOCX = r"C:\Users\nisha\Downloads\docsphere.docx"
TARGET_DOCX = r"c:\Users\nisha\OneDrive\Desktop\scratch\PhonePerfect_Project_Report.docx"

def set_para_text(p, text):
    """Sets paragraph text while preserving runs formatting if possible."""
    if p.runs:
        p.runs[0].text = text
        for r in p.runs[1:]:
            r.text = ""
    else:
        p.text = text

def fill_table_data(table, data):
    """
    Fills table with data (list of tuples/lists).
    Adjusts row count if necessary and preserves header formatting.
    """
    num_data_rows = len(data)
    current_rows = len(table.rows)

    # If table has fewer rows, add rows
    while len(table.rows) < num_data_rows:
        new_row = table.add_row()
        # copy cell borders & shading from previous row if needed

    # If table has more rows, delete extra rows
    while len(table.rows) > num_data_rows:
        row_elem = table.rows[-1]._tr
        row_elem.getparent().remove(row_elem)

    # Populate cell data
    for r_idx, row_data in enumerate(data):
        row = table.rows[r_idx]
        for c_idx, cell_value in enumerate(row_data):
            if c_idx < len(row.cells):
                cell = row.cells[c_idx]
                if cell.paragraphs:
                    p = cell.paragraphs[0]
                    set_para_text(p, str(cell_value))
                    # Clear any subsequent paragraphs in cell
                    for p_extra in cell.paragraphs[1:]:
                        p_extra._p.getparent().remove(p_extra._p)
                else:
                    cell.text = str(cell_value)

def format_figure_box(table, fig_info):
    """Formats a single-cell figure placeholder table."""
    cell = table.rows[0].cells[0]
    cell.text = fig_info["description"]
    # Ensure shading is clean
    tcPr = cell._tc.get_or_add_tcPr()
    # Apply soft light gray shading
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F9FBFD"/>')
    tcPr.append(shd)

def main():
    print(f"Cloning {TEMPLATE_DOCX} to {TARGET_DOCX}...")
    shutil.copyfile(TEMPLATE_DOCX, TARGET_DOCX)
    doc = docx.Document(TARGET_DOCX)
    print("Cloned successfully.")

    # ── 1. PRELIMINARIES: TITLE PAGE ──────────────────────────────────────────
    t_info = PRELIMINARY["title_page"]
    set_para_text(doc.paragraphs[0], t_info["title"])
    set_para_text(doc.paragraphs[1], t_info["subtitle"])
    set_para_text(doc.paragraphs[2], t_info["submitted_by"])
    set_para_text(doc.paragraphs[3], t_info["students"][0])
    set_para_text(doc.paragraphs[4], t_info["students"][1])
    set_para_text(doc.paragraphs[5], t_info["students"][2])
    set_para_text(doc.paragraphs[6], t_info["students"][3])
    set_para_text(doc.paragraphs[7], t_info["degree_prefix"])
    set_para_text(doc.paragraphs[8], t_info["degree"])
    set_para_text(doc.paragraphs[9], t_info["dept_prefix"])
    set_para_text(doc.paragraphs[10], t_info["department"])
    set_para_text(doc.paragraphs[11], t_info["institution"])
    set_para_text(doc.paragraphs[12], t_info["place"])
    set_para_text(doc.paragraphs[13], t_info["university"])
    set_para_text(doc.paragraphs[14], t_info["date"])

    # ── 2. PRELIMINARIES: BONAFIDE CERTIFICATE ────────────────────────────────
    cert = PRELIMINARY["certificate"]
    set_para_text(doc.paragraphs[16], cert["heading"])
    set_para_text(doc.paragraphs[17], cert["body"])
    set_para_text(doc.paragraphs[19], cert["viva"])

    # ── 3. PRELIMINARIES: ACKNOWLEDGEMENT ─────────────────────────────────────
    ack = PRELIMINARY["acknowledgement"]
    set_para_text(doc.paragraphs[20], ack["heading"])
    set_para_text(doc.paragraphs[21], ack["p1"])
    set_para_text(doc.paragraphs[22], ack["p2"])
    set_para_text(doc.paragraphs[23], ack["p3"])
    set_para_text(doc.paragraphs[24], ack["p4"])

    # ── 4. PRELIMINARIES: ABSTRACT ────────────────────────────────────────────
    ab = PRELIMINARY["abstract"]
    set_para_text(doc.paragraphs[25], ab["heading"])
    set_para_text(doc.paragraphs[26], ab["p1"])
    set_para_text(doc.paragraphs[27], ab["p2"])
    set_para_text(doc.paragraphs[28], ab["p3"])
    set_para_text(doc.paragraphs[29], ab["keywords"])

    # ── 5. PRELIMINARIES: TABLE OF CONTENTS (P32 to P82) ──────────────────────
    set_para_text(doc.paragraphs[30], "TABLE OF CONTENTS")
    set_para_text(doc.paragraphs[31], "PAGE NO.")
    for idx, (title, page_num) in enumerate(TOC_ITEMS):
        p_idx = 32 + idx
        if p_idx < len(doc.paragraphs):
            set_para_text(doc.paragraphs[p_idx], f"{title}\t{page_num}")

    # ── 6. PRELIMINARIES: LIST OF FIGURES (P85 to P93) ────────────────────────
    set_para_text(doc.paragraphs[83], "LIST OF FIGURES")
    set_para_text(doc.paragraphs[84], "PAGE NO.")
    for idx, (fig_title, page_num) in enumerate(LOF_ITEMS):
        p_idx = 85 + idx
        if p_idx < len(doc.paragraphs):
            set_para_text(doc.paragraphs[p_idx], f"{fig_title}\t{page_num}")

    # ── 7. PRELIMINARIES: LIST OF TABLES (P96 to P104) ────────────────────────
    set_para_text(doc.paragraphs[94], "LIST OF TABLES")
    set_para_text(doc.paragraphs[95], "PAGE NO.")
    for idx, (tbl_title, page_num) in enumerate(LOT_ITEMS):
        p_idx = 96 + idx
        if p_idx < len(doc.paragraphs):
            set_para_text(doc.paragraphs[p_idx], f"{tbl_title}\t{page_num}")

    # ── 8. PRELIMINARIES: LIST OF ABBREVIATIONS ───────────────────────────────
    set_para_text(doc.paragraphs[105], "LIST OF ABBREVIATIONS")
    abbrev_table = doc.tables[2]
    abbrev_data = [("Abbreviation", "Expansion")] + ABBREVIATIONS
    fill_table_data(abbrev_table, abbrev_data)

    # ── 9. CHAPTER 1: INTRODUCTION (P107 to P145) ─────────────────────────────
    c1 = CHAPTER_1
    set_para_text(doc.paragraphs[107], c1["title"])
    set_para_text(doc.paragraphs[108], c1["description_heading"])
    set_para_text(doc.paragraphs[109], c1["description_p1"])
    set_para_text(doc.paragraphs[110], c1["description_p2"])
    set_para_text(doc.paragraphs[111], c1["description_p3"])

    set_para_text(doc.paragraphs[112], c1["domain_heading"])
    set_para_text(doc.paragraphs[113], c1["domain_p1"])
    set_para_text(doc.paragraphs[114], c1["domain_sub1_heading"])
    set_para_text(doc.paragraphs[115], c1["domain_sub1_p1"])
    set_para_text(doc.paragraphs[116], c1["domain_sub2_heading"])
    set_para_text(doc.paragraphs[117], c1["domain_sub2_p1"])
    set_para_text(doc.paragraphs[118], c1["domain_sub3_p1"][:len(c1["domain_sub3_p1"])//2])
    set_para_text(doc.paragraphs[119], c1["domain_sub3_heading"])
    set_para_text(doc.paragraphs[120], c1["domain_sub3_p1"])

    set_para_text(doc.paragraphs[121], c1["problem_heading"])
    set_para_text(doc.paragraphs[122], c1["problem_p1"])
    set_para_text(doc.paragraphs[123], c1["problem_p2"])

    set_para_text(doc.paragraphs[124], c1["objectives_heading"])
    set_para_text(doc.paragraphs[125], c1["obj_sub1_heading"])
    set_para_text(doc.paragraphs[126], c1["obj_intro"])
    for b_idx, bullet in enumerate(c1["obj_bullets"]):
        p_idx = 127 + b_idx
        if p_idx < len(doc.paragraphs):
            set_para_text(doc.paragraphs[p_idx], bullet)

    set_para_text(doc.paragraphs[134], c1["obj_sub2_heading"])
    set_para_text(doc.paragraphs[135], c1["obj_sub2_p1"])
    set_para_text(doc.paragraphs[136], c1["obj_sub2_p2"])

    set_para_text(doc.paragraphs[137], c1["obj_sub3_heading"])
    set_para_text(doc.paragraphs[138], c1["obj_sub3_p1"])
    for b_idx, bullet in enumerate(c1["obj_bullets_apps"] if "obj_bullets_apps" in c1 else c1["obj_sub3_bullets"]):
        p_idx = 139 + b_idx
        if p_idx < len(doc.paragraphs):
            set_para_text(doc.paragraphs[p_idx], bullet)

    set_para_text(doc.paragraphs[144], c1["org_heading"])
    set_para_text(doc.paragraphs[145], c1["org_p1"])

    # ── 10. CHAPTER 2: LITERATURE SURVEY (P146 to P160, Table 3) ──────────────
    c2 = CHAPTER_2
    set_para_text(doc.paragraphs[146], c2["title"])
    set_para_text(doc.paragraphs[147], c2["overview_heading"])
    set_para_text(doc.paragraphs[148], c2["overview_p1"])
    set_para_text(doc.paragraphs[149], c2["review_heading"])
    set_para_text(doc.paragraphs[150], c2["review_p1"])
    set_para_text(doc.paragraphs[151], c2["table_caption"])
    set_para_text(doc.paragraphs[152], "")

    fill_table_data(doc.tables[3], TABLE_2_1)

    set_para_text(doc.paragraphs[153], c2["gap_heading"])
    set_para_text(doc.paragraphs[154], c2["gap_p1"])
    set_para_text(doc.paragraphs[155], c2["gap_p2"])
    for b_idx, bullet in enumerate(c2["gap_bullets"][:4]):
        set_para_text(doc.paragraphs[156 + b_idx], bullet)
    set_para_text(doc.paragraphs[160], c2["gap_bullets"][4])

    # ── 11. CHAPTER 3: EXISTING SYSTEM (P161 to P168) ─────────────────────────
    c3 = CHAPTER_3
    set_para_text(doc.paragraphs[161], c3["title"])
    set_para_text(doc.paragraphs[162], c3["intro_p1"])
    set_para_text(doc.paragraphs[163], c3["sub1_heading"])
    set_para_text(doc.paragraphs[164], c3["sub1_p1"])
    set_para_text(doc.paragraphs[165], c3["sub2_heading"])
    set_para_text(doc.paragraphs[166], c3["sub2_p1"])
    set_para_text(doc.paragraphs[167], c3["sub3_heading"])
    set_para_text(doc.paragraphs[168], c3["sub3_p1"])

    # ── 12. CHAPTER 4: PROBLEMS IDENTIFIED (P169 to P184) ─────────────────────
    c4 = CHAPTER_4
    set_para_text(doc.paragraphs[169], c4["title"])
    set_para_text(doc.paragraphs[170], c4["intro_p1"])
    set_para_text(doc.paragraphs[171], c4["sub1_heading"])
    set_para_text(doc.paragraphs[172], c4["sub1_p1"])
    set_para_text(doc.paragraphs[173], c4["sub2_heading"])
    set_para_text(doc.paragraphs[174], c4["sub2_p1"])
    set_para_text(doc.paragraphs[175], c4["sub3_heading"])
    set_para_text(doc.paragraphs[176], c4["sub3_p1"])
    set_para_text(doc.paragraphs[177], c4["sub4_heading"])
    set_para_text(doc.paragraphs[178], c4["sub4_p1"])
    set_para_text(doc.paragraphs[179], c4["sub5_heading"])
    set_para_text(doc.paragraphs[180], c4["sub5_p1"])
    set_para_text(doc.paragraphs[181], c4["sub6_heading"])
    set_para_text(doc.paragraphs[182], c4["sub6_p1"])
    set_para_text(doc.paragraphs[183], c4["sub7_heading"])
    set_para_text(doc.paragraphs[184], c4["sub7_p1"])

    # ── 13. CHAPTER 5: PROPOSED SYSTEM (P185 to P222, Tables 4, 5, 6) ─────────
    c5 = CHAPTER_5
    set_para_text(doc.paragraphs[185], c5["title"])
    set_para_text(doc.paragraphs[186], c5["overview_heading"])
    set_para_text(doc.paragraphs[187], c5["overview_p1"])
    set_para_text(doc.paragraphs[188], c5["arch_heading"])
    set_para_text(doc.paragraphs[189], c5["arch_p1"])
    set_para_text(doc.paragraphs[190], c5["fig_5_1_caption"])
    format_figure_box(doc.tables[4], FIGURE_BOXES[4])

    set_para_text(doc.paragraphs[191], c5["arch_layers_intro"])
    for l_idx, layer in enumerate(c5["arch_layers"]):
        set_para_text(doc.paragraphs[192 + l_idx], layer)

    set_para_text(doc.paragraphs[197], c5["workflow_heading"])
    set_para_text(doc.paragraphs[198], c5["workflow_p1"])
    for w_idx, step in enumerate(c5["workflow_bullets"][:8]):
        p_idx = 199 + w_idx
        if p_idx <= 206:
            set_para_text(doc.paragraphs[p_idx], step)
    set_para_text(doc.paragraphs[207], c5["workflow_bullets"][7])

    set_para_text(doc.paragraphs[208], c5["fig_5_2_caption"])
    format_figure_box(doc.tables[5], FIGURE_BOXES[5])

    set_para_text(doc.paragraphs[209], "5.4 KEY FEATURES")
    for f_idx, feat in enumerate(c5["features_bullets"][:7]):
        set_para_text(doc.paragraphs[210 + f_idx], feat)

    set_para_text(doc.paragraphs[217], c5["comparison_heading"])
    set_para_text(doc.paragraphs[218], c5["comparison_p1"])
    set_para_text(doc.paragraphs[219], c5["table_5_1_caption"])
    set_para_text(doc.paragraphs[220], "")
    fill_table_data(doc.tables[6], TABLE_5_1)

    set_para_text(doc.paragraphs[221], c5["deployment_heading"])
    set_para_text(doc.paragraphs[222], c5["deployment_p1"] + " " + c5["deployment_p2"])

    # ── 14. CHAPTER 6: SYSTEM REQUIREMENTS (P223 to P230, Tables 7, 8) ────────
    c6 = CHAPTER_6
    set_para_text(doc.paragraphs[223], c6["title"])
    set_para_text(doc.paragraphs[224], c6["intro_p1"])
    set_para_text(doc.paragraphs[225], c6["hard_heading"])
    set_para_text(doc.paragraphs[226], c6["table_6_1_caption"])
    set_para_text(doc.paragraphs[227], "")
    fill_table_data(doc.tables[7], TABLE_6_1)

    set_para_text(doc.paragraphs[228], c6["soft_heading"])
    set_para_text(doc.paragraphs[229], c6["table_6_2_caption"])
    set_para_text(doc.paragraphs[230], "")
    fill_table_data(doc.tables[8], TABLE_6_2)

    # ── 15. CHAPTER 7: SYSTEM IMPLEMENTATIONS (P231 to P284, Tables 9 to 20) ──
    c7 = CHAPTER_7
    set_para_text(doc.paragraphs[231], c7["title"])
    set_para_text(doc.paragraphs[232], c7["intro_p1"])
    set_para_text(doc.paragraphs[233], c7["modules_heading"])
    set_para_text(doc.paragraphs[234], c7["modules_intro"])
    for m_idx, mod in enumerate(c7["modules_bullets"]):
        set_para_text(doc.paragraphs[235 + m_idx], mod)

    set_para_text(doc.paragraphs[241], c7["desc_heading"])

    # 7.2.1
    set_para_text(doc.paragraphs[242], c7["sub1_heading"])
    set_para_text(doc.paragraphs[243], c7["sub1_p1"])
    set_para_text(doc.paragraphs[244], c7["sub1_p2"])
    set_para_text(doc.paragraphs[245], c7["sub1_p3"])
    set_para_text(doc.paragraphs[246], c7["table_7_1_caption"])
    set_para_text(doc.paragraphs[247], "")
    fill_table_data(doc.tables[9], TABLE_7_1)
    set_para_text(doc.paragraphs[248], c7["fig_7_1_caption"])
    format_figure_box(doc.tables[10], FIGURE_BOXES[10])

    # 7.2.2
    set_para_text(doc.paragraphs[249], c7["sub2_heading"])
    set_para_text(doc.paragraphs[250], c7["sub2_p1"])
    set_para_text(doc.paragraphs[251], c7["sub2_p2"])
    set_para_text(doc.paragraphs[252], c7["sub2_p3"])
    set_para_text(doc.paragraphs[253], c7["fig_7_2_caption"])
    format_figure_box(doc.tables[11], FIGURE_BOXES[11])

    # 7.2.3
    set_para_text(doc.paragraphs[254], c7["sub3_heading"])
    set_para_text(doc.paragraphs[255], c7["sub3_p1"])
    set_para_text(doc.paragraphs[256], c7["sub3_p2"] + " " + c7["sub3_p3"])
    set_para_text(doc.paragraphs[257], c7["table_7_2_caption"])
    set_para_text(doc.paragraphs[258], "")
    fill_table_data(doc.tables[12], TABLE_7_2)
    set_para_text(doc.paragraphs[259], c7["fig_7_3_caption"])
    format_figure_box(doc.tables[13], FIGURE_BOXES[13])

    # 7.2.4
    set_para_text(doc.paragraphs[260], c7["sub4_heading"])
    set_para_text(doc.paragraphs[261], c7["sub4_p1"])
    set_para_text(doc.paragraphs[262], c7["table_7_3_caption"])
    set_para_text(doc.paragraphs[263], "")
    fill_table_data(doc.tables[14], TABLE_7_3)
    set_para_text(doc.paragraphs[264], c7["sub4_p2"])
    set_para_text(doc.paragraphs[265], c7["sub4_p3"])
    set_para_text(doc.paragraphs[266], c7["fig_7_4_caption"])
    format_figure_box(doc.tables[15], FIGURE_BOXES[15])

    # 7.2.5
    set_para_text(doc.paragraphs[267], c7["sub5_heading"])
    set_para_text(doc.paragraphs[268], c7["sub5_p1"])
    set_para_text(doc.paragraphs[269], c7["sub5_p2"])
    set_para_text(doc.paragraphs[270], "diffPct = ((currentPrice - expectedMarketPrice) / expectedMarketPrice) * 100")
    set_para_text(doc.paragraphs[271], c7["sub5_p3"])
    set_para_text(doc.paragraphs[272], c7["table_7_4_caption"])
    set_para_text(doc.paragraphs[273], "")
    fill_table_data(doc.tables[16], TABLE_7_4)
    set_para_text(doc.paragraphs[274], "Platform security and client isolation are maintained through strict CORS policies and Android container sandboxing, as summarized in Table 7.5.")
    set_para_text(doc.paragraphs[275], c7["table_7_5_caption"])
    set_para_text(doc.paragraphs[276], "")
    fill_table_data(doc.tables[17], TABLE_7_5)
    set_para_text(doc.paragraphs[277], c7["fig_7_5_caption"])
    format_figure_box(doc.tables[18], FIGURE_BOXES[18])

    # 7.2.6
    set_para_text(doc.paragraphs[278], c7["sub6_heading"])
    set_para_text(doc.paragraphs[279], c7["sub6_p1"])
    set_para_text(doc.paragraphs[280], c7["sub6_p2"])
    set_para_text(doc.paragraphs[281], c7["sub6_p3"])
    set_para_text(doc.paragraphs[282], "The resulting Progressive Web Application and native Android WebView container deliver sub-second startup times, resilient offline execution, and fluid 60/120 FPS frame rates without framework bloat.")
    set_para_text(doc.paragraphs[283], c7["fig_7_6_caption"])
    format_figure_box(doc.tables[19], FIGURE_BOXES[19])
    set_para_text(doc.paragraphs[284], c7["fig_7_7_caption"])
    format_figure_box(doc.tables[20], FIGURE_BOXES[20])

    # ── 16. CHAPTER 8: CONCLUSION AND FUTURE ENHANCEMENTS (P285 to P295) ──────
    c8 = CHAPTER_8
    set_para_text(doc.paragraphs[285], c8["title"])
    set_para_text(doc.paragraphs[286], c8["conc_heading"])
    set_para_text(doc.paragraphs[287], c8["conc_p1"])
    set_para_text(doc.paragraphs[288], c8["conc_p2"] + " " + c8["conc_p3"])
    set_para_text(doc.paragraphs[289], c8["enh_heading"])
    for e_idx, enh in enumerate(c8["enh_bullets"][:6]):
        set_para_text(doc.paragraphs[290 + e_idx], enh)

    # ── 17. REFERENCES (P296 to P306) ─────────────────────────────────────────
    set_para_text(doc.paragraphs[296], "REFERENCES")
    for r_idx, ref in enumerate(REFERENCES_LIST[:10]):
        set_para_text(doc.paragraphs[297 + r_idx], ref)

    print(f"Saving final report to {TARGET_DOCX}...")
    doc.save(TARGET_DOCX)
    print("Report saved successfully!")

if __name__ == "__main__":
    main()
