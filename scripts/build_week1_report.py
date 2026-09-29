"""Build the Week 1 internal progress report as a polished DOCX."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "week_01" / "BAO_CAO_TIEN_DO_TUAN_01.docx"

NAVY = "17365D"
BLUE = "D9EAF7"
PALE = "F4F7FA"
GRID = "C9D2DC"
BLACK = "000000"


def set_cell_shading(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_border(cell, color: str = GRID, size: str = "6") -> None:
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    borders = tc_pr.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = f"w:{edge}"
        element = borders.find(qn(tag))
        if element is None:
            element = OxmlElement(tag)
            borders.append(element)
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), size)
        element.set(qn("w:space"), "0")
        element.set(qn("w:color"), color)


def set_cell_margins(cell, top=90, start=110, bottom=90, end=110) -> None:
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for margin, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{margin}"))
        if node is None:
            node = OxmlElement(f"w:{margin}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_repeat_table_header(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def set_col_widths(table, widths) -> None:
    for row in table.rows:
        for cell, width in zip(row.cells, widths):
            cell.width = Inches(width)


def set_run_font(run, name="Aptos", size=10.5, bold=False, color=BLACK, italic=False):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:ascii"), name)
    run._element.rPr.rFonts.set(qn("w:hAnsi"), name)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor.from_string(color)


def style_paragraph(paragraph, before=0, after=5, line=1.12, alignment=None):
    fmt = paragraph.paragraph_format
    fmt.space_before = Pt(before)
    fmt.space_after = Pt(after)
    fmt.line_spacing = line
    if alignment is not None:
        paragraph.alignment = alignment


def add_text(paragraph, text, bold=False, italic=False, color=BLACK, size=10.5):
    run = paragraph.add_run(text)
    set_run_font(run, size=size, bold=bold, italic=italic, color=color)
    return run


def add_bullet(doc, text, level=0):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.left_indent = Inches(0.23 + level * 0.2)
    p.paragraph_format.first_line_indent = Inches(-0.12)
    style_paragraph(p, after=3)
    add_text(p, text)
    return p


def add_numbered(doc, number, text):
    # Use explicit labels so separate lists always restart at one in Word/LibreOffice.
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.27)
    p.paragraph_format.first_line_indent = Inches(-0.16)
    style_paragraph(p, after=3)
    add_text(p, f"{number}. {text}")
    return p


def add_heading(doc, text, level=1):
    p = doc.add_paragraph(style=f"Heading {level}")
    style_paragraph(p, before=9 if level == 1 else 6, after=4, line=1.0)
    run = p.add_run(text)
    set_run_font(run, name="Aptos Display", size=13 if level == 1 else 11.5, bold=True, color=NAVY)
    return p


def add_table(doc, headers, rows, widths, font_size=8.8, header_fill=NAVY):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_col_widths(table, widths)
    header = table.rows[0]
    set_repeat_table_header(header)
    for cell, text in zip(header.cells, headers):
        set_cell_shading(cell, header_fill)
        set_cell_border(cell)
        set_cell_margins(cell)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = cell.paragraphs[0]
        style_paragraph(p, after=0, line=1.0, alignment=WD_ALIGN_PARAGRAPH.CENTER)
        add_text(p, text, bold=True, color="FFFFFF", size=font_size)
    for idx, row_data in enumerate(rows):
        row = table.add_row()
        for cell, value in zip(row.cells, row_data):
            set_cell_shading(cell, "FFFFFF" if idx % 2 == 0 else PALE)
            set_cell_border(cell)
            set_cell_margins(cell)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            p = cell.paragraphs[0]
            style_paragraph(p, after=0, line=1.05)
            if len(str(value)) <= 24 and any(token in str(value) for token in ("Đang", "Có", "Không", "16/09", "11/09", "15/09", "Tuần 2")):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            add_text(p, str(value), size=font_size)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)
    return table


def add_meta_line(doc, label, value):
    p = doc.add_paragraph()
    style_paragraph(p, after=1, line=1.0)
    add_text(p, f"{label}: ", bold=True, size=9.4)
    add_text(p, value, size=9.4)
    return p


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = paragraph.add_run("Trang ")
    set_run_font(run, size=8.5, color="6B7280")
    fld_char1 = OxmlElement("w:fldChar")
    fld_char1.set(qn("w:fldCharType"), "begin")
    instr_text = OxmlElement("w:instrText")
    instr_text.set(qn("xml:space"), "preserve")
    instr_text.text = "PAGE"
    fld_char2 = OxmlElement("w:fldChar")
    fld_char2.set(qn("w:fldCharType"), "end")
    run._r.append(fld_char1)
    run._r.append(instr_text)
    run._r.append(fld_char2)


def build() -> None:
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.65)
    section.left_margin = Inches(0.78)
    section.right_margin = Inches(0.78)
    section.header_distance = Inches(0.3)
    section.footer_distance = Inches(0.3)

    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Aptos"
    normal._element.rPr.rFonts.set(qn("w:ascii"), "Aptos")
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Aptos")
    normal.font.size = Pt(10.5)
    normal.font.color.rgb = RGBColor.from_string(BLACK)
    for style_name in ("Title", "Heading 1", "Heading 2"):
        style = styles[style_name]
        style.font.name = "Aptos Display"
        style._element.rPr.rFonts.set(qn("w:ascii"), "Aptos Display")
        style._element.rPr.rFonts.set(qn("w:hAnsi"), "Aptos Display")
        style.font.color.rgb = RGBColor.from_string(NAVY)

    header = section.header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    style_paragraph(hp, after=0, line=1.0)
    add_text(hp, "TLCN AN TOÀN THÔNG TIN  |  BÁO CÁO TIẾN ĐỘ NỘI BỘ", bold=True, size=8.2, color="5B6573")

    footer = section.footer
    fp = footer.paragraphs[0]
    style_paragraph(fp, after=0, line=1.0)
    add_page_number(fp)

    title = doc.add_paragraph(style="Title")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.paragraph_format.space_after = Pt(5)
    add_text(title, "Báo cáo tiến độ nội bộ Tuần 1", bold=True, size=20, color=NAVY)
    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    style_paragraph(subtitle, after=12, line=1.0)
    add_text(subtitle, "Khóa protocol và chuẩn bị Gate 1", italic=True, size=11, color="5B6573")

    for label, value in [
        ("Đề tài", "So sánh mô hình học có giám sát và phát hiện bất thường cho hệ thống phát hiện xâm nhập mạng trên UNSW-NB15: Đánh giá theo phương pháp leave-one-attack-class-out"),
        ("Nhóm", "Trịnh Trâm Anh (23162005), Nguyễn Trọng Tín (23162102), Hoàng Văn Vương Thu (23162099)"),
        ("Người hướng dẫn", "Nguyễn Đăng Quang"),
        ("Kỳ báo cáo", "10/09/2026-16/09/2026"),
        ("Phiên bản", "0.1 - cập nhật đến 11/09/2026"),
        ("Trạng thái", "Bản nội bộ chuẩn bị Gate 1"),
    ]:
        add_meta_line(doc, label, value)

    add_heading(doc, "1. Tóm tắt tiến độ")
    p = doc.add_paragraph()
    style_paragraph(p, after=6)
    add_text(p, "Trong những ngày đầu của Tuần 1, nhóm đã dựng repository nghiên cứu, thống nhất phạm vi dự kiến, ba câu hỏi nghiên cứu, bốn mô hình, ba vòng LOACO, năm random seed và bộ quy tắc đánh giá. Nhóm cũng đã tạo ma trận 80 run, schema kết quả, ánh xạ câu hỏi nghiên cứu sang bằng chứng, đặc tả metric/threshold và danh sách kiểm thử synthetic.")
    p = doc.add_paragraph()
    style_paragraph(p, after=6)
    add_text(p, "Theo kế hoạch, nhóm ")
    add_text(p, "chưa tải dataset và chưa huấn luyện mô hình", bold=True)
    add_text(p, ". Đây không phải là thiếu tiến độ: Tuần 1 chỉ nhằm khóa protocol và hoàn tất Gate 1 trước khi chuyển sang kiểm kê dữ liệu. Tại thời điểm lập báo cáo, hồ sơ kỹ thuật đã sẵn sàng để review nhưng Gate 1 ")
    add_text(p, "chưa được kết luận PASS", bold=True)
    add_text(p, " vì biên bản họp, ngày họp, nhận xét review chéo và xác nhận của cả ba thành viên còn bỏ trống.")

    add_heading(doc, "2. Công việc đã thực hiện")
    add_table(doc,
              ["Hạng mục", "Kết quả hiện có", "Bằng chứng"],
              [
                  ("Cấu trúc repository và quy tắc lưu trữ", "Đã tạo repo, configs, docs, scripts, src, data; raw data và model nặng được loại khỏi Git", "README.md; .gitignore"),
                  ("Phạm vi và câu hỏi nghiên cứu", "Đã khóa dự thảo RQ1 closed-set, RQ2 held-out attack và RQ3 detection/false-alarm trade-off", "docs/protocol/RQ_TO_EVIDENCE.md"),
                  ("Kịch bản thí nghiệm", "Đã định nghĩa closed-set và LOACO cho Reconnaissance, DoS, Exploits", "configs/experiment_matrix.yaml"),
                  ("Mô hình và seed", "Random Forest, XGBoost, Isolation Forest, Autoencoder; seed 42, 52, 62, 72, 82", "configs/experiment_matrix.yaml"),
                  ("Ma trận run", "Có 80 run dự kiến, gồm 4 scenario x 4 model x 5 seed; run_id không trùng", "RUN_MATRIX.csv; generate_run_matrix.py"),
                  ("Hợp đồng đầu ra", "Đã mô tả run.json, metrics.csv, predictions.csv và điều kiện một run hợp lệ", "docs/protocol/RESULT_SCHEMA.md"),
                  ("Metric và threshold", "Score cao hơn = giống Attack/anomaly hơn; threshold lấy từ Normal validation tại FPR 1% và 5%", "METRIC_THRESHOLD_SPEC.md"),
                  ("Kiểm thử trước dataset thật", "Đã lập 10 synthetic tests cho score direction, threshold, label mapping, mẫu số bằng 0 và duplicate run_id", "SYNTHETIC_TESTS.md"),
                  ("Artifact dữ liệu và thuật ngữ", "Đã có glossary, checklist data audit và mẫu ma trận related work", "GLOSSARY.md; DATA_AUDIT_CHECKLIST.md; RELATED_WORK_MATRIX.csv"),
                  ("Kế hoạch và phân công", "Đã ghi mốc ngày cụ thể, owner, reviewer và mốc báo cáo 4 tuần/lần", "PHAN_CONG_NHOM.md; GANTT_CHART.md"),
              ],
              [1.65, 3.55, 1.75], font_size=8.0)

    add_heading(doc, "3. Kiểm tra bằng chứng kỹ thuật")
    for item in [
        "Trước khi tạo báo cáo, repository ở nhánh main và bộ artifact nền tảng đã được commit; báo cáo Tuần 1 này là các file bổ sung đang chờ commit.",
        "Commit gần nhất chứa bộ artifact Tuần 1 là f5686f0 (docs: add week 1 team artifacts).",
        "RUN_MATRIX.csv có 80 dòng dữ liệu; mỗi scenario có 20 run: closed_set, loaco_reconnaissance, loaco_dos và loaco_exploits.",
        "Kiểm tra trùng run_id không phát hiện bản ghi trùng.",
        "Dataset raw chưa xuất hiện trong repository, phù hợp với quy tắc bảo mật và kế hoạch chỉ tải dữ liệu sau khi Gate 1 được duyệt.",
    ]:
        add_bullet(doc, item)

    add_heading(doc, "4. Tiến độ theo thành viên")
    add_table(doc,
              ["Thành viên", "Đã có", "Còn phải đóng trong Tuần 1", "Trạng thái"],
              [
                  ("Trịnh Trâm Anh", "Glossary, data-audit checklist, related-work template", "Review chéo; bổ sung nguồn/tiêu chí nếu nhóm thống nhất; xác nhận trong biên bản", "Đang review"),
                  ("Hoàng Văn Vương Thu", "Metric/threshold specification, 10 synthetic tests", "Review score direction và metric; ghi test owner", "Đang review"),
                  ("Nguyễn Trọng Tín", "Repository, config, ma trận 80 run, result schema, Gate 1 checklist", "Mời/xác nhận tài khoản GitHub; tổng hợp review chéo; điền biên bản họp", "Đang tích hợp"),
              ],
              [1.35, 2.05, 2.85, 0.7], font_size=7.9)

    add_heading(doc, "5. Các quyết định protocol cần xác nhận bằng văn bản")
    p = doc.add_paragraph()
    style_paragraph(p, after=4)
    add_text(p, "Các điểm dưới đây đã có đề xuất trong tài liệu làm việc nhưng chưa được đánh dấu PASS trong biên bản họp:")
    for number, item in enumerate([
        "Giữ official train/test split của UNSW-NB15 và không dùng official test để fit, tuning hoặc chọn threshold.",
        "Chọn Reconnaissance, DoS và Exploits làm ba held-out attack classes.",
        "Dùng bốn mô hình Random Forest, XGBoost, Isolation Forest và Autoencoder.",
        "Chạy năm seed 42, 52, 62, 72, 82 và báo cáo mean +/- standard deviation.",
        "Chọn threshold trên Normal validation tại ngân sách FPR 1% và 5%.",
        "Loại id, label và attack_cat khỏi feature matrix.",
        "Chỉ gọi kết quả là held-out/unseen trong thiết kế LOACO, không gọi là bằng chứng phát hiện zero-day thực tế.",
    ], start=1):
        add_numbered(doc, number, item)

    add_heading(doc, "6. Vấn đề còn mở và cách đóng")
    add_table(doc,
              ["Vấn đề", "Owner", "Hạn nội bộ", "Cách đóng"],
              [
                  ("Chưa có ngày, hình thức và nội dung kết luận của kickoff", "Tín + cả nhóm", "16/09/2026", "Họp 30-45 phút, điền BIEN_BAN_HOP_01.md"),
                  ("Chưa có review chéo và xác nhận của ba thành viên", "Cả nhóm", "15/09/2026", "Review từng artifact, ghi người review và commit/link"),
                  ("Chưa xác nhận username GitHub của Trâm Anh và Vương Thu", "Tín", "11/09/2026", "Xác nhận tài khoản riêng và quyền truy cập repo"),
                  ("Related-work matrix mới là header, chưa có bài cụ thể", "Trâm Anh", "Tuần 2", "Lập danh mục 10-15 nguồn có kiểm chứng"),
                  ("Gantt và nhịp báo cáo cần đối chiếu deadline chính thức", "Tín", "16/09/2026", "Xác nhận với giảng viên; giữ mốc 07/10/2026 là mốc nội bộ"),
              ],
              [2.6, 0.8, 1.0, 2.55], font_size=7.9)

    add_heading(doc, "7. Kế hoạch ngay sau Gate 1")
    for item in [
        "Hoàn thiện related work có nguồn và tiêu chí so sánh.",
        "Thiết kế kiến trúc pipeline, interface model và test plan.",
        "Rà lại protocol theo góp ý của giảng viên nếu có.",
        "Chuẩn bị checklist tải dữ liệu chính thức cho giai đoạn 24/09-30/09/2026.",
        "Không đưa số liệu thực nghiệm vào báo cáo trước khi có data audit và Gate 2.",
    ]:
        add_bullet(doc, item)

    add_heading(doc, "8. Kết luận và đề nghị xác nhận")
    p = doc.add_paragraph()
    style_paragraph(p, after=6)
    add_text(p, "Tuần 1 đã tạo được nền tảng cần thiết để bắt đầu nghiên cứu có kiểm soát: phạm vi, protocol dự thảo, ma trận run, schema kết quả và phân công đều đã có artifact truy vết được. Mức hoàn thành hiện tại phù hợp với mục tiêu Tuần 1, nhưng chưa đủ cơ sở để ghi Gate 1 là PASS.")
    p = doc.add_paragraph()
    style_paragraph(p, after=4)
    add_text(p, "Nhóm đề nghị xác nhận ba việc trong buổi kickoff ngày 16/09/2026:")
    for number, item in enumerate([
        "Chấp thuận các quyết định protocol ở Mục 5.",
        "Ghi rõ vấn đề còn mở, owner và deadline nếu có thay đổi.",
        "Ký kết luận PASS/FAIL trong docs/meetings/BIEN_BAN_HOP_01.md.",
    ], start=1):
        add_numbered(doc, number, item)
    p = doc.add_paragraph()
    style_paragraph(p, before=3, after=9)
    add_text(p, "Kết luận hiện tại: ", bold=True, color=NAVY)
    add_text(p, "NOT REVIEWED - chờ review chéo và xác nhận Gate 1", bold=True, color=NAVY)

    add_heading(doc, "Phụ lục A - Danh mục artifact Tuần 1", level=1)
    add_table(doc,
              ["Artifact", "Vai trò"],
              [
                  ("docs/week_01/KE_HOACH_TUAN_01.md", "Mục tiêu và lịch 7 ngày"),
                  ("docs/week_01/GLOSSARY.md", "Thuật ngữ thống nhất"),
                  ("docs/week_01/DATA_AUDIT_CHECKLIST.md", "Checklist chuẩn bị Gate 2"),
                  ("docs/week_01/RELATED_WORK_MATRIX.csv", "Mẫu tổng hợp tài liệu liên quan"),
                  ("docs/week_01/METRIC_THRESHOLD_SPEC.md", "Metric, score và threshold"),
                  ("docs/week_01/SYNTHETIC_TESTS.md", "Danh sách test trước dataset thật"),
                  ("docs/protocol/RQ_TO_EVIDENCE.md", "Ánh xạ RQ sang bằng chứng"),
                  ("docs/protocol/RESULT_SCHEMA.md", "Hợp đồng artifact kết quả"),
                  ("docs/protocol/RUN_MATRIX.csv", "Ma trận 80 run"),
                  ("docs/protocol/GATE_1_CHECKLIST.md", "Điều kiện PASS/FAIL Gate 1"),
                  ("docs/meetings/BIEN_BAN_HOP_01.md", "Biên bản kickoff và xác nhận Gate 1"),
              ],
              [3.6, 3.35], font_size=8.4)

    # Keep tables and headings legible in headless renderers.
    for paragraph in doc.paragraphs:
        if paragraph.style.name == "Normal":
            style_paragraph(paragraph)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print("Built Week 1 report DOCX")


if __name__ == "__main__":
    build()
