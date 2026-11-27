from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/group_delivery_20261110/TrongTin/CAM_NANG_BAO_CAO_TRONG_TIN_20261118.docx"
BLUE = "176B87"
PALE = "EAF4F7"
PALE_GREEN = "EDF5F1"
INK = "1F2A30"
MUTED = "52616A"
WHITE = "FFFFFF"


def shade(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=95, start=110, bottom=95, end=110):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    margins = tc_pr.first_child_found_in("w:tcMar")
    if margins is None:
        margins = OxmlElement("w:tcMar")
        tc_pr.append(margins)
    for side, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = margins.find(qn(f"w:{side}"))
        if node is None:
            node = OxmlElement(f"w:{side}")
            margins.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    repeat = OxmlElement("w:tblHeader")
    repeat.set(qn("w:val"), "true")
    tr_pr.append(repeat)


def set_keep_with_next(paragraph):
    paragraph.paragraph_format.keep_with_next = True


def set_run_font(run, size=None, bold=None, color=None, name="Segoe UI"):
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), name)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def set_cell_text(cell, text, size=9, color=INK, bold=False):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.12
    r = p.add_run(str(text))
    set_run_font(r, size, bold, color)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    set_cell_margins(cell)


def add_field(paragraph, name):
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instruction = OxmlElement("w:instrText")
    instruction.set(qn("xml:space"), "preserve")
    instruction.text = name
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = "1"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.extend((begin, instruction, separate, text, end))
    set_run_font(run, 8, color=MUTED)


def add_p(doc, text="", style=None, size=10, color=INK, bold=False, italic=False,
          before=0, after=5, align=None, keep=False):
    p = doc.add_paragraph(style=style)
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = 1.12
    if align is not None:
        p.alignment = align
    r = p.add_run(text)
    set_run_font(r, size, bold, color)
    r.italic = italic
    if keep:
        set_keep_with_next(p)
    return p


def add_bullet(doc, text, level=0, size=9.6):
    p = doc.add_paragraph(style="List Bullet" if level == 0 else "List Bullet 2")
    p.paragraph_format.left_indent = Inches(0.23 + level * 0.2)
    p.paragraph_format.first_line_indent = Inches(-0.13)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.1
    r = p.add_run(text)
    set_run_font(r, size, color=INK)
    return p


def add_num(doc, text, size=9.6):
    p = doc.add_paragraph(style="List Number")
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.first_line_indent = Inches(-0.17)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.1
    r = p.add_run(text)
    set_run_font(r, size, color=INK)
    return p


def heading(doc, text, level=1):
    p = doc.add_paragraph(style=f"Heading {level}")
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(8 if level == 1 else 5)
    p.paragraph_format.space_after = Pt(4 if level == 1 else 3)
    r = p.add_run(text)
    set_run_font(r, 15 if level == 1 else 11.5, True, "000000")
    return p


def table(doc, headers, rows, widths=None, font=8.6, header_fill=BLUE):
    t = doc.add_table(rows=1, cols=len(headers))
    t.autofit = False
    t.style = "Table Grid"
    for i, value in enumerate(headers):
        set_cell_text(t.rows[0].cells[i], value, font, WHITE, True)
        shade(t.rows[0].cells[i], header_fill)
    set_repeat_table_header(t.rows[0])
    for row in rows:
        cells = t.add_row().cells
        for i, value in enumerate(row):
            set_cell_text(cells[i], value, font)
            if len(t.rows) % 2 == 0:
                shade(cells[i], "F5F8F9")
    if widths:
        for row in t.rows:
            for i, width in enumerate(widths):
                row.cells[i].width = Inches(width)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)
    return t


def callout(doc, label, text, fill=PALE, size=9.5):
    t = doc.add_table(rows=1, cols=1)
    t.autofit = False
    c = t.cell(0, 0)
    shade(c, fill)
    set_cell_margins(c, 140, 180, 140, 180)
    c.text = ""
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(label)
    set_run_font(r, 9.4, True, BLUE)
    p2 = c.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.space_after = Pt(0)
    p2.paragraph_format.line_spacing = 1.12
    r = p2.add_run(text)
    set_run_font(r, size, color=INK)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)


def flow(doc, labels):
    t = doc.add_table(rows=1, cols=len(labels) * 2 - 1)
    t.autofit = False
    for i, label in enumerate(labels):
        cell = t.rows[0].cells[i * 2]
        shade(cell, PALE)
        set_cell_text(cell, label, 8.3, INK, True)
        if i < len(labels) - 1:
            set_cell_text(t.rows[0].cells[i * 2 + 1], ">", 12, BLUE, True)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)


def hyperlink(paragraph, text, url):
    part = paragraph.part
    rid = part.relate_to(url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True)
    link = OxmlElement("w:hyperlink")
    link.set(qn("r:id"), rid)
    run = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), BLUE)
    rpr.append(color)
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    rpr.append(underline)
    fonts = OxmlElement("w:rFonts")
    fonts.set(qn("w:ascii"), "Segoe UI")
    fonts.set(qn("w:hAnsi"), "Segoe UI")
    fonts.set(qn("w:eastAsia"), "Segoe UI")
    rpr.append(fonts)
    run.append(rpr)
    txt = OxmlElement("w:t")
    txt.text = text
    run.append(txt)
    link.append(run)
    paragraph._p.append(link)


def page(doc, title, intro=None):
    doc.add_page_break()
    heading(doc, title, 1)
    if intro:
        add_p(doc, intro, size=9.7, color=MUTED, after=7)


def main():
    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(0.62)
    section.bottom_margin = Inches(0.62)
    section.left_margin = Inches(0.7)
    section.right_margin = Inches(0.7)

    normal = doc.styles["Normal"]
    normal.font.name = "Segoe UI"
    normal._element.rPr.rFonts.set(qn("w:ascii"), "Segoe UI")
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Segoe UI")
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Segoe UI")
    normal.font.size = Pt(9.7)
    normal.font.color.rgb = RGBColor.from_string(INK)
    for style_name in ("Heading 1", "Heading 2", "Title", "Subtitle"):
        st = doc.styles[style_name]
        st.font.name = "Segoe UI"
        st._element.rPr.rFonts.set(qn("w:ascii"), "Segoe UI")
        st._element.rPr.rFonts.set(qn("w:hAnsi"), "Segoe UI")
        st._element.rPr.rFonts.set(qn("w:eastAsia"), "Segoe UI")
        st.font.color.rgb = RGBColor(0, 0, 0)
    doc.styles["Normal"].paragraph_format.line_spacing = 1.12

    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    footer.paragraph_format.space_before = Pt(0)
    r = footer.add_run("Sổ tay học cá nhân của Nguyễn Trọng Tín  |  Trang ")
    set_run_font(r, 8, color=MUTED)
    add_field(footer, "PAGE")

    # Cover and quick route.
    add_p(doc, "SỔ TAY BÁO CÁO CÁ NHÂN", size=10, color=BLUE, bold=True, before=30, after=14,
          align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "Nguyễn Trọng Tín", size=29, bold=True, after=6, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "Phần phụ trách và cách trình bày đề tài NIDS", size=14, color=MUTED,
          after=28, align=WD_ALIGN_PARAGRAPH.CENTER)
    callout(doc, "ĐỀ TÀI CỦA NHÓM",
        "So sánh mô hình học có giám sát và phát hiện bất thường cho hệ thống phát hiện xâm nhập mạng trên UNSW-NB15: Đánh giá theo phương pháp leave-one-attack-class-out.", size=10)
    add_p(doc, "Tài liệu ôn riêng cho phần Protocol · Pipeline · RF/XGB · Tái lập · Demo",
          size=11, bold=True, after=10, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "Bản học cá nhân ngày 18/11/2026", size=9.5, color=MUTED,
          after=24, align=WD_ALIGN_PARAGRAPH.CENTER)
    callout(doc, "CÁCH DÙNG",
        "Đọc phần giải thích trước, sau đó mở đúng màn hình web và tự làm theo từng bước. Các câu trong khung “Tín có thể nói” là gợi ý để tập; em hãy diễn đạt lại bằng cách hiểu thật của mình. Đây là tài liệu ôn, không thay báo cáo chính thức hoặc phần tự kiểm của em.", fill=PALE_GREEN)
    heading(doc, "Lộ trình trong sổ tay", 2)
    table(doc, ["Chặng", "Em sẽ nắm được"], [
        ("1–3", "Vai trò của Tín, ý nghĩa đề tài và thiết kế 80 lượt thí nghiệm"),
        ("4–6", "Đường đi dữ liệu, RF/XGBoost, tái lập và cách đọc kết quả"),
        ("7–9", "Bản public/local, demo từng nút và kịch bản nói trên bục"),
        ("10–12", "Câu hỏi phản biện, thao tác code, phương án mất mạng/HDMI và checklist"),
    ], widths=[0.8, 5.8], font=9)

    # Chapter 1.
    page(doc, "1 Vai trò của Tín trong nhóm",
         "Em là người phụ trách giải thích cách nhóm tổ chức thí nghiệm, nối các bước xử lý và trình diễn đầu ra của mô hình. Đây là phạm vi em cần hiểu sâu khi bảo vệ.")
    table(doc, ["Mảng", "Việc cần hiểu", "Bằng chứng nên mở"], [
        ("Protocol", "Vì sao có 4 kịch bản, 4 mô hình, 5 seed; tránh dùng test để chọn ngưỡng.", "Màn Thực nghiệm; configs/experiment_matrix.yaml"),
        ("Pipeline", "Dữ liệu đi từ CSV qua kiểm schema, tiền xử lý, mô hình, score, ngưỡng và dự đoán.", "Màn Bài toán/Demo; src/nids_benchmark/"),
        ("RF và XGBoost", "Hai mô hình có giám sát học từ nhãn; đọc score rồi so với threshold.", "models.py; bảng AP và operating points"),
        ("Tái lập", "Lưu cấu hình, seed, dấu vân tay dữ liệu/phần mềm và artifact để truy lại một run.", "runner.py; run.json; manifest SHA-256"),
        ("Demo và tích hợp", "Mở web, chạy một CSV, giải thích dòng cụ thể và nêu đúng giới hạn.", "presentation/index.html; demo_server.py"),
        ("Kết luận chung", "Nói điều nghiên cứu chứng minh được, điều còn thiếu và hướng làm tiếp.", "Màn Tự đánh giá; báo cáo tổng phần bàn luận"),
    ], widths=[1.0, 3.0, 2.6], font=8.2)
    callout(doc, "RANH GIỚI CẦN GIỮ",
        "Phân công có nghĩa là em chịu trách nhiệm đọc, hiểu và trả lời về phạm vi này. Nó không tự chứng minh em là người duy nhất viết mọi dòng mã hoặc đã tự kiểm từng artifact. Chỉ kể đúng thao tác em đã thật sự làm; phần chưa tự chạy thì hãy chạy thử trước buổi báo cáo.")
    heading(doc, "Bản đồ người phụ trách", 2)
    table(doc, ["Bạn", "Trọng tâm"], [
        ("Trịnh Trâm Anh", "Nguồn dữ liệu, 42 feature, chia tập và giới hạn benchmark"),
        ("Hoàng Văn Vương Thu", "IF/AE, ngưỡng, metric và phân tích lỗi"),
        ("Nguyễn Trọng Tín", "Protocol, pipeline, RF/XGB, tái lập, demo và phần tổng"),
    ], widths=[2.1, 4.5], font=8.8)
    add_p(doc, "Bản tổng hợp của nhóm nằm ở nhánh main; phần cá nhân của em nằm ở nhánh trongtin. Nhánh Git và lịch sử commit là bằng chứng phiên bản, không thay cho phần em tự hiểu và trình bày.", size=9.2)

    # Chapter 2.
    page(doc, "2 Đề tài nói gì bằng tiếng người",
         "Đề tài hỏi một câu cụ thể: nếu máy chưa từng được cho xem một loại tấn công trong lúc học, nó có còn nhận ra loại đó khác với lưu lượng bình thường khi đem ra kiểm tra không?")
    table(doc, ["Từ trong tên đề tài", "Nghĩa dễ hiểu", "Điều cần nhớ"], [
        ("NIDS", "Network Intrusion Detection System: hệ thống theo dõi hoạt động mạng và báo dấu hiệu đáng ngờ.", "Báo động khác với tự chặn tấn công."),
        ("UNSW-NB15", "Bộ dữ liệu hoạt động mạng đã công bố, có mẫu Normal và mẫu tấn công.", "Nhóm dùng bộ chuẩn chung; preset web lấy một phần từ bộ này."),
        ("Học có giám sát", "Cho mô hình các ví dụ có nhãn để học phân biệt Normal và Attack.", "RF/XGB là hai mô hình thuộc nhóm này."),
        ("Phát hiện bất thường", "Cho mô hình học hình dáng của Normal rồi xem mẫu khác thường đến mức nào.", "IF/AE thuộc nhóm này trong dự án."),
        ("LOACO", "Giữ kín một lớp tấn công khỏi vùng dùng để phát triển, rồi kiểm nó ở test.", "Mô phỏng lớp chưa gặp trong benchmark, không đại diện mọi zero-day ngoài đời."),
    ], widths=[1.25, 3.5, 1.85], font=8.2)
    heading(doc, "Một hình dung nhanh", 2)
    flow(doc, ["Dữ liệu có Normal và Attack", "Giấu một lớp", "Cho máy học phần còn lại", "Đưa lớp bị giấu vào test", "Đếm điểm mạnh và lỗi"])
    callout(doc, "TÍN CÓ THỂ NÓI",
        "“Nói ngắn gọn, nhóm so sánh các cách phát hiện xâm nhập trên cùng một bộ dữ liệu. Nhóm cố ý giữ lại một loại tấn công khi huấn luyện rồi kiểm tra xem mô hình phản ứng ra sao. Trọng tâm là khả năng phát hiện lớp chưa xuất hiện trong vùng phát triển, chứ nhóm chưa tuyên bố đã xây một thiết bị chặn tấn công dùng ngoài thực tế.”")
    heading(doc, "Vì sao đề tài có ý nghĩa", 2)
    add_bullet(doc, "Trong vận hành mạng, kiểu tấn công có thể đổi; chỉ kiểm tra loại đã thấy trước có thể đánh giá quá lạc quan.")
    add_bullet(doc, "Thử nghiệm giúp đo sự đánh đổi giữa báo nhầm lưu lượng bình thường và bỏ sót tấn công.")
    add_bullet(doc, "Kết quả là bằng chứng nghiên cứu trên benchmark. Để thành sản phẩm thực tế còn cần dữ liệu phù hợp, đo tốc độ, kiểm thử an toàn và giám sát khi triển khai.")

    # Chapter 3.
    page(doc, "3 Ma trận 80 lượt thí nghiệm",
         "Con số 80 là số lần huấn luyện theo các cấu hình khác nhau trong protocol nghiên cứu. Nó không phải số dòng CSV, số lần bấm demo hoặc 80 mô hình được web huấn luyện trực tiếp.")
    table(doc, ["Chiều thử nghiệm", "Các giá trị", "Số lựa chọn"], [
        ("Kịch bản", "CS, LR, LD, LE", "4"),
        ("Mô hình", "RF, XGB, IF, AE", "4"),
        ("Seed", "42, 52, 62, 72, 82", "5"),
        ("Tổng", "4 × 4 × 5", "80 run"),
    ], widths=[1.35, 3.6, 1.65], font=9)
    table(doc, ["Mã", "Diễn giải"], [
        ("CS", "Closed-set: không giấu lớp tấn công khỏi vùng phát triển."),
        ("LR", "Giấu Reconnaissance."),
        ("LD", "Giấu DoS."),
        ("LE", "Giấu Exploits."),
    ], widths=[1.0, 5.6], font=8.7)
    heading(doc, "Một run gồm những gì", 2)
    add_p(doc, "Ví dụ CS-RF-S42 nghĩa là kịch bản CS, mô hình Random Forest, seed 42. Mỗi run có hai ngưỡng được chọn từ cùng mô hình đã fit. Do đó 80 run vẫn là 80 lượt fit; nếu ghi bảng theo hai ngưỡng thì số dòng metric nhiều hơn nhưng số lần huấn luyện không tăng gấp đôi.", size=9.5)
    flow(doc, ["4 kịch bản", "× 4 mô hình", "× 5 seed", "= 80 lượt fit", "2 ngưỡng / run"])
    callout(doc, "CÂU TRẢ LỜI NGẮN",
        "“Có bốn kịch bản, bốn mô hình và năm seed nên là 4 × 4 × 5 = 80 lượt huấn luyện. Mỗi lượt lưu hai operating point 1% và 5%; hai điểm này không phải hai lượt huấn luyện mới.”")
    heading(doc, "Vì sao cần seed", 2)
    add_p(doc, "Seed cố định giúp điều khiển các bước ngẫu nhiên để so sánh lần chạy có thể truy lại. Năm seed cho phép báo cáo trung bình và độ lệch chuẩn; nó cho biết kết quả dao động thế nào trong các lần thử, chứ không đảm bảo mọi môi trường tương lai có cùng đầu ra từng bit.", size=9.5)

    # Chapter 4.
    page(doc, "4 Luồng dữ liệu và tránh rò rỉ",
         "Điều quan trọng là test chỉ được dùng để đánh giá cuối. Nếu nhìn test để chỉnh cách xử lý hoặc chọn ngưỡng rồi lại báo cáo test như chưa từng xem, kết quả sẽ không còn là phép kiểm độc lập.")
    heading(doc, "Thứ tự của pipeline", 2)
    flow(doc, ["CSV nguồn", "Loại lớp bị giấu", "Chia train / validation", "Fit xử lý trên train", "Chọn ngưỡng bằng Normal validation", "Đánh giá trên test"])
    table(doc, ["Bước", "Giải thích", "Điều cần tránh"], [
        ("1. Đọc dữ liệu", "Đọc official train và official test theo schema đã khai báo.", "Không tự trộn test vào train."),
        ("2. Giấu lớp", "Ở LR/LD/LE, loại lớp được chọn khỏi official train trước khi chia train/validation.", "Không để mẫu held-out lọt vào vùng phát triển."),
        ("3. Chia vùng phát triển", "Chia 80% train và 20% validation theo cấu hình, giữ seed.", "Không chọn ngưỡng bằng test."),
        ("4. Fit xử lý", "Điền thiếu, scale số và one-hot biến phân loại; học tham số xử lý trên train được phép.", "Không fit preprocessing trên toàn bộ test."),
        ("5. Học và chốt ngưỡng", "RF/XGB học nhãn; IF/AE học Normal. Ngưỡng lấy từ score Normal validation.", "Không thay threshold sau khi xem test để làm đẹp kết quả."),
        ("6. Đánh giá", "Dùng mô hình, preprocessing, ngưỡng đã lưu để chấm official test.", "Không fit lại trên test."),
    ], widths=[1.3, 3.5, 1.8], font=8.1)
    callout(doc, "BA CỘT KHÔNG ĐƯỢC HỌC NHƯ FEATURE",
        "id dùng truy vết dòng; label là đáp án Normal/Attack; attack_cat là tên nhóm để phân tích. Ba cột này không đi vào mô hình như đầu vào. Nếu cho label hoặc tên loại tấn công vào input, mô hình có thể thấy đáp án thay vì tự phát hiện.", fill=PALE_GREEN)
    add_p(doc, "UNSW-NB15 có 42 feature gốc và ba cột metadata chính trong các tệp dùng ở đây. One-hot có thể làm tăng số chiều đầu vào sau biến đổi, nên “42 feature” không có nghĩa ma trận cuối cùng luôn chỉ rộng đúng 42 cột.", size=9.2)

    # Chapter 5.
    page(doc, "5 Hiểu hai mô hình RF và XGBoost",
         "Hai mô hình này có giám sát: lúc huấn luyện chúng nhận feature cùng nhãn. Khi demo, chúng không nhận đáp án của dòng để dự đoán; đáp án chỉ được dùng sau đó nếu CSV có nhãn để đối chiếu.")
    table(doc, ["Mô hình", "Hình dung", "Cấu hình full run trong mã", "Điểm trả về"], [
        ("RF", "Nhiều cây quyết định bỏ phiếu; kết quả gom lại.", "RandomForestClassifier, 300 cây, min_samples_leaf=2, class_weight balanced_subsample.", "Xác suất lớp Attack từ predict_proba."),
        ("XGB", "Các cây được thêm nối tiếp, từng bước giảm lỗi của tổ hợp trước.", "XGBClassifier, 350 cây, depth 6, learning_rate 0.08, subsample/colsample 0.85.", "Điểm xác suất Attack sau sigmoid."),
    ], widths=[0.7, 2.0, 2.55, 1.35], font=7.9)
    heading(doc, "Điều gì xảy ra với một dòng", 2)
    flow(doc, ["42 feature gốc", "Tiền xử lý đã fit", "RF hoặc XGB", "Score", "So với ngưỡng", "Normal / Attack"])
    add_p(doc, "Trong code chung, RF và XGB đều chuyển score theo hướng “càng cao càng giống Attack”. Hàm quyết định là so sánh score với threshold: score lớn hơn hoặc bằng threshold thì Attack; thấp hơn threshold thì Normal. Các model khác có cách tạo score khác nhau nhưng pipeline đưa về cùng chiều diễn giải.", size=9.5)
    table(doc, ["Điểm số", "Nó có nghĩa gì", "Không nên nói"], [
        ("Score", "Mức điểm mô hình dùng để xếp thứ tự nghi ngờ trong model/scenario đó.", "Không gọi là xác suất chắc chắn đúng cho mọi mô hình; thang điểm khác nhau."),
        ("Threshold", "Mốc phân cách hai nhãn theo chính sách đã chọn trên validation.", "Không phải một luật phổ quát áp dụng y hệt mọi model."),
        ("Prediction", "Kết luận nhị phân Normal hoặc Attack sau khi so điểm với mốc.", "Không phải tên cụ thể của loại tấn công."),
    ], widths=[1.05, 3.1, 2.45], font=8.1)
    callout(doc, "MẪU GIẢI THÍCH",
        "“Mô hình chấm dòng dữ liệu một điểm. Mốc ngưỡng đã chọn quyết định khi nào hệ thống coi điểm đó đủ đáng ngờ để gắn nhãn Attack. Vì vậy có thể cùng một score nhưng quyết định khác nếu thay threshold.”")

    # Chapter 6.
    page(doc, "6 Đọc kết quả mà không hiểu nhầm",
         "Một số toàn test có thể rất cao vì tập đó gồm cả nhiều loại tấn công mô hình đã thấy. Khi câu hỏi là “nhận ra lớp chưa thấy ra sao”, cần đọc riêng phạm vi Normal cộng lớp bị giấu.")
    heading(doc, "Ví dụ LR với Reconnaissance bị giấu", 2)
    table(doc, ["Model", "AP toàn test", "AP Normal + lớp bị giấu", "Mẫu số phạm vi hẹp"], [
        ("RF", "0,9852 ± 0,0003", "0,7077 ± 0,0173", "40.496 tổng; 3.496 Recon"),
        ("XGB", "0,9852 ± 0,0004", "0,6623 ± 0,0357", "40.496 tổng; 3.496 Recon"),
    ], widths=[0.72, 1.42, 1.8, 2.66], font=8.2)
    add_p(doc, "Các giá trị trên là trung bình ± độ lệch chuẩn qua năm seed. AP là Average Precision: đo chất lượng xếp hạng dựa trên precision/recall khi đổi ngưỡng; nó không phải phần trăm dòng phân loại đúng. All-test có 82.332 dòng và 45.332 Attack; phạm vi hẹp ở LR gồm Normal và 3.496 dòng Reconnaissance.", size=9.1)
    callout(doc, "CÁCH ĐỌC ĐÚNG",
        "Trong ví dụ LR, AP toàn test của hai model gần 0,985 nhưng AP ở Normal + Recon thấp hơn đáng kể. Điều này cho thấy nhìn số toàn test một mình có thể che mất khó khăn ở lớp bị giấu. Cần nêu rõ phạm vi, số mẫu và chỉ số trước khi nhận xét.")
    heading(doc, "Các chỉ số em cần phân biệt", 2)
    table(doc, ["Chỉ số", "Câu hỏi nó trả lời", "Lưu ý khi nói"], [
        ("AP", "Mô hình xếp các mẫu Attack lên trên Normal tốt đến đâu khi nhìn qua nhiều ngưỡng?", "Không phải accuracy; xem theo đúng phạm vi và mẫu số."),
        ("FPR", "Trong Normal, tỷ lệ nào bị báo nhầm thành Attack?", "Target được chọn ở validation; FPR test được đo riêng."),
        ("Recall", "Trong Attack của phạm vi đang xét, tỷ lệ nào được phát hiện?", "Phải nói rõ đang gộp mọi Attack hay chỉ lớp bị giấu."),
        ("UADR", "Trong lớp tấn công bị giấu, tỷ lệ nào bị phát hiện ở ngưỡng đã chọn?", "Chỉ có ý nghĩa ở kịch bản có lớp held-out."),
        ("Precision", "Trong các dòng bị báo Attack, phần nào là Attack thật?", "Có thể giảm khi nhiều báo nhầm."),
        ("Độ lệch chuẩn", "Kết quả dao động thế nào qua các seed?", "Nhỏ hơn nghĩa là ít dao động trong năm run này, không bảo đảm tổng quát."),
    ], widths=[1.02, 3.35, 2.23], font=7.9)
    heading(doc, "Target FPR không phải cam kết trên test", 2)
    add_p(doc, "Ví dụ bảng operating points của CS–RF: target 1% cho FPR test trung bình khoảng 4,21% và recall khoảng 90,27%; target 5% cho FPR test khoảng 18,57% và recall khoảng 97,14% qua năm seed. Ngưỡng được chọn để đáp ứng target trên Normal validation; test khác phân bố/mẫu nên FPR đo trên test có thể cao hơn. Đây cũng là ví dụ đánh đổi: ngưỡng thấp hơn thường bắt được nhiều Attack hơn nhưng báo nhầm nhiều Normal hơn.", size=9.1)

    # Chapter 7.
    page(doc, "7 Tái lập và dấu vết một run",
         "Tái lập không chỉ là bấm lại và mong con số giống nhau. Cần ghi nhận dữ liệu nào, cấu hình nào, seed nào, phần mềm nào và file kết quả nào thuộc về lần chạy.")
    table(doc, ["Artifact", "Nội dung", "Cách dùng khi bị hỏi"], [
        ("run.json", "Scenario, model, seed, tham số, mốc thời gian, phiên bản thư viện, hash cấu hình/dữ liệu, số dòng.", "Trả lời run này được tạo với điều kiện nào."),
        ("metrics.csv", "AP, precision, recall, F1, FPR, UADR và mẫu số.", "Truy ra bảng báo cáo và so sánh."),
        ("predictions.csv", "Score, threshold, dự đoán và nhãn đối chiếu theo dòng.", "Giải thích TP/FP/TN/FN của một bản ghi."),
        ("model_bundle.joblib", "Preprocessor đã fit, model đã fit và hai ngưỡng.", "Dùng để suy luận lại mà không học lại."),
        ("Manifest SHA-256", "Mã băm nhận diện file và kiểm tra file có thay đổi hay không.", "Đối chiếu tính toàn vẹn; hash không tự chứng minh nguồn dữ liệu."),
    ], widths=[1.45, 3.2, 1.95], font=8)
    heading(doc, "Tên run đọc như thế nào", 2)
    add_p(doc, "CS-RF-S42: CS là kịch bản; RF là model; S42 là seed 42. Tên nhất quán giúp lần từ bảng tổng hợp về metrics.csv, predictions.csv, run.json và bundle của đúng lượt.", size=9.5)
    heading(doc, "Ba mức kết luận cần tách", 2)
    table(doc, ["Mức", "Ví dụ phát biểu"], [
        ("Đã kiểm bằng máy", "Validator xác nhận các tổ hợp được khai báo và số liệu đối chiếu được với nguồn."),
        ("Em đã tự làm/hiểu", "Chỉ nói sau khi em tự mở, chạy, đọc và giải thích được artifact đó."),
        ("Thầy/nhóm đã duyệt hoặc đã nộp", "Chỉ nói khi có phản hồi hoặc bằng chứng gửi tương ứng; không suy từ kiểm kỹ thuật."),
    ], widths=[1.8, 4.8], font=8.6)
    callout(doc, "TÁI LẬP KHÔNG CÓ NGHĨA LÀ...",
        "...mọi máy, phiên bản thư viện và phép tính phải cho cùng từng bit. Cấu hình/seed/hash hỗ trợ truy vết; còn môi trường, phần cứng và sai số số thực phải được lưu ý. Không dùng một lần smoke-test nhỏ để nhận là đã lặp lại toàn bộ benchmark.", fill=PALE_GREEN)

    # Chapter 8.
    page(doc, "8 Web public local và API",
         "Cùng một giao diện có thể đi qua hai đường suy luận khác nhau. Khi trả lời giảng viên, nói rõ mình đang mở bản nào để tránh gọi web public là API Python.")
    table(doc, ["Bản", "Đường chạy", "Ý nghĩa"], [
        ("Web public ATTQ NIDS", "Trình duyệt tải tham số 16 model seed 42; Web Worker JavaScript kiểm CSV, biến đổi feature, tính score và so threshold ngay trên máy.", "CSV người dùng chọn không được gửi lên API dự đoán Python. Cần Internet để tải trang/model assets."),
        ("Local Python demo", "demo_server.py phục vụ UI và API local: /api/lab/run, /api/predict, /api/compare.", "API chạy ở loopback 127.0.0.1:4397; dùng bundle Python đã lưu và thư viện cài trong môi trường."),
        ("Offline v4", "CHAY_DEMO.cmd mở server local, rồi truy cập địa chỉ localhost được in trong cửa sổ.", "Đã đóng kèm 16 model và CSV mẫu; không cần Internet cho suy luận. Không mở HTML bằng nhấp đúp."),
    ], widths=[1.2, 3.35, 2.05], font=7.9)
    heading(doc, "FE BE và API trong đề tài", 2)
    add_bullet(doc, "FE (frontend): màn hình web, nút chọn dữ liệu, chọn model và vùng hiển thị kết quả.")
    add_bullet(doc, "BE (backend): phần xử lý phía server. Ở local Python demo, server đọc yêu cầu và gọi hàm suy luận.")
    add_bullet(doc, "API: đường giao tiếp có tên và định dạng giữa giao diện và backend. Ví dụ local POST /api/lab/run nhận cấu hình rồi trả kết quả JSON.")
    add_bullet(doc, "Bản public dùng JavaScript trong browser worker cho inference đã đóng gói; vì vậy không nên nói mọi lần bấm web đều gọi Python API.")
    callout(doc, "CSV CHƯA CÓ NHÃN",
        "Có thể tính dự đoán Normal/Attack nếu đủ feature. Khi không có label thật, không biết dòng đó đúng hay sai nên không tính accuracy, precision, recall, confusion matrix có căn cứ. attack_cat là nhãn tên lớp để đối chiếu, không phải tên tấn công mà model dự đoán.")

    # Chapter 9.
    page(doc, "9 Demo từng bước trên web",
         "Kịch bản chính dùng 20 dòng “Chỉ Normal” để cô lập lỗi báo nhầm. Giao diện hiện nút 1 · Chọn dữ liệu và 2 · Xem kết quả; mỗi lần đổi cấu hình phải bấm chạy lại.")
    table(doc, ["Bước", "Thao tác", "Điều em cần quan sát"], [
        ("1", "Mở https://attq-nids.phttrongtin-nguyen-a46.workers.dev/ và bấm Demo.", "Đúng web trình bày của nhóm."),
        ("2", "Ở 1 · Chọn dữ liệu, chọn Chỉ Normal · xem báo động nhầm.", "Preset này có 20 dòng normal; giúp nhìn rõ false alarm."),
        ("3", "Chọn CS · Không giấu lớp, mô hình RF, target 5% · ngưỡng đã lưu.", "Seed giữ cố định 42; không có thao tác huấn luyện."),
        ("4", "Bấm Chạy suy luận rồi chờ màn 2 · Xem kết quả.", "Xem tổng số dòng, số Attack/Normal, rồi giữ vị trí bản ghi #1."),
        ("5", "Đọc score, ký hiệu ≥ hoặc <, threshold và dự đoán.", "Đối chiếu nhãn Normal; target 5% cho FP ở dòng đầu."),
        ("6", "Bấm Tải kết quả CSV để lưu lượt 5%.", "Không cần mở Excel trước lớp nếu thời gian ít; chỉ cho thấy CSV có thể tải."),
        ("7", "Bấm 1 · Chọn dữ liệu; chỉ đổi target thành 1%, chạy lại.", "Cùng dòng/model/score; threshold tăng, dự đoán đổi Normal, thành TN."),
        ("8", "Tải CSV lượt 1%; cuối cùng bấm Phạm vi demo.", "Nêu dữ liệu là subset UNSW-NB15 và demo không bắt traffic trực tiếp."),
    ], widths=[0.45, 3.48, 2.67], font=7.8)
    heading(doc, "Số đối chiếu bản ghi đầu tiên", 2)
    table(doc, ["CS–RF–S42 · ID 1", "Target 5%", "Target 1%"], [
        ("Nhãn thật", "Normal", "Normal"),
        ("Score", "0,705741", "0,705741"),
        ("Ngưỡng", "0,557282", "0,805367"),
        ("Quyết định", "0,705741 ≥ 0,557282 → Attack", "0,705741 < 0,805367 → Normal"),
        ("Đối chiếu", "FP · báo động nhầm", "TN · nhận đúng bình thường"),
    ], widths=[1.7, 2.45, 2.45], font=8.2)
    callout(doc, "LỜI GIẢI THÍCH NGẮN",
        "“Ở target 5%, điểm dòng này cao hơn ngưỡng nên bị báo Attack, trong khi nhãn đối chiếu là Normal. Đây là FP. Khi đổi sang target 1%, ngưỡng cao hơn; score của dòng không đổi nhưng nằm dưới ngưỡng nên kết quả thành Normal, tức TN. Mô hình không được huấn luyện lại giữa hai lượt.”")
    add_p(doc, "Mốc 1% và 5% là target FPR khi chọn threshold bằng Normal validation. Không nói rằng bộ CSV demo có FPR đúng 1% hoặc 5%, và không lấy một bản ghi này để kết luận RF tốt hơn XGB.", size=9.1, bold=True, color=BLUE)

    # Chapter 10.
    page(doc, "10 Hai cách chạy demo và phương án dự phòng",
         "Trong giao diện có hai preset hữu ích. Dùng một preset cho cả hai target trong cùng phần trình bày; không đổi CSV giữa hai lượt vì lúc đó không còn là so sánh cùng một mẫu.")
    table(doc, ["Mục đích", "Preset", "Cách giải thích"], [
        ("Tập riêng một lỗi báo nhầm", "Chỉ Normal · 20 dòng", "Dòng #1 Normal cho thấy FP ở 5% rồi TN ở 1%."),
        ("Theo lời dẫn mặc định của web", "Normal xen các nhóm tấn công · 50 dòng", "Cũng có thể so cùng dòng đầu; thêm được bức tranh mẫu có cả hai lớp. Không trộn tổng số của preset này với preset kia."),
        ("Nhận CSV mới", "Mở tệp CSV trên máy…", "Cần schema feature tương thích, đúng cột categorical/numeric, 1–1.000 dòng. Không chọn pcap hoặc log tùy ý."),
        ("Không có nhãn", "Dữ liệu chưa có nhãn", "Có thể dự đoán nếu schema đúng; kết quả không có căn cứ đúng/sai."),
        ("Thử lỗi đầu vào", "CSV sai schema · thử kiểm tra", "Web phải báo thiếu/không hợp lệ; không tự bịa feature bị thiếu."),
    ], widths=[1.45, 2.2, 3.0], font=8)
    heading(doc, "Trước buổi diễn tập", 2)
    add_num(doc, "Tự mở web trên chính laptop sẽ trình chiếu, không chỉ dựa trên ảnh chụp hoặc nhớ rằng ai đó đã chạy được.")
    add_num(doc, "Tập chuyển màn bằng các nút dưới cùng: Bài toán → Thực nghiệm → Demo → Hỏi đáp → Tự đánh giá. Bàn phím mũi tên trái/phải cũng chuyển màn khi focus không nằm trong ô nhập.")
    add_num(doc, "Chạy đủ hai target, xem đúng số dòng và đúng ID; lưu hai CSV nếu muốn minh chứng lần tự thực hành.")
    add_num(doc, "Thử mở hồ sơ nguồn/đường dẫn PDF; mở trước tab cần thiết để khỏi tìm kiếm lâu trên bục.")
    add_num(doc, "Nếu web public mất mạng, chạy gói offline v4 đã tải và giải nén trước; không chờ đến lớp mới tải model hoặc cài thư viện.")
    callout(doc, "GIỚI HẠN DEMO",
        "Preset là tập con UNSW-NB15. Bản ghi mới không phải traffic do nhóm tự thu chỉ vì em vừa tải file lên. Demo không học lại, không bắt gói mạng trực tiếp, chưa phân loại tên attack_cat thành loại tấn công và không chặn kết nối.", fill=PALE_GREEN)

    # Chapter 11.
    page(doc, "11 Đi tour code theo đúng luồng",
         "Nếu giảng viên hỏi “code đi từ đâu tới đâu”, mở lần lượt các file dưới đây. Chỉ mở file cần trả lời câu hỏi; không cần trình chiếu toàn bộ IDE.")
    table(doc, ["Thứ tự", "File", "Vai trò bằng tiếng người", "Điểm vào"], [
        ("1", "src/nids_benchmark/contracts.py", "Hợp đồng schema: kiểm cột bắt buộc và cấm metadata đi vào feature.", "validate_required_columns / validate_feature_columns"),
        ("2", "src/nids_benchmark/data.py", "Đọc hai split, chuẩn hóa nhãn, bỏ lớp held-out rồi chia vùng phát triển.", "load_official_splits / make_development_split"),
        ("3", "src/nids_benchmark/preprocessing.py", "Điền thiếu, scale số, one-hot biến phân loại; transform bằng bộ xử lý đã fit.", "build_preprocessor / transform_frame"),
        ("4", "src/nids_benchmark/models.py", "Tạo RF/XGB/IF/AE, fit theo đúng nhóm và tính score cùng chiều.", "fit_model / FittedModel.score"),
        ("5", "src/nids_benchmark/evaluation.py", "Chọn threshold từ Normal validation rồi đánh giá score trên test.", "select_threshold / evaluate_test_scores"),
        ("6", "src/nids_benchmark/runner.py", "Nối một cấu hình end-to-end, lưu metrics, prediction, model bundle và run.json.", "run_experiment"),
        ("7", "src/nids_benchmark/demo.py", "Nạp bundle đã lưu, kiểm CSV rồi trả score, threshold và nhãn.", "load_bundle / predict_frame / predict_csv"),
        ("8", "scripts/demo_server.py", "Phục vụ giao diện/API local Python.", "do_GET / do_POST"),
        ("9", "demo/presentation/browser-engine.mjs", "Bản public chuyển tham số đóng gói sang inference ở JavaScript.", "parseCSV / transform / score / predict"),
    ], widths=[0.55, 2.15, 2.75, 1.2], font=7.25)
    heading(doc, "Một câu code nên hiểu", 2)
    t = doc.add_table(rows=1, cols=1)
    shade(t.cell(0, 0), "F1F4F5")
    set_cell_text(t.cell(0, 0), "prediction = (score >= threshold) ? Attack : Normal", 10, INK, True)
    add_p(doc, "Đây là cách viết ý tưởng, không phải đoạn chép nguyên văn Python/JavaScript. Nó cho thấy model tạo score trước, threshold chuyển score thành quyết định sau. Nhãn thật chỉ tham gia bước đối chiếu khi có.", size=9.3)
    heading(doc, "Mã browser và API local khác nhau", 2)
    add_p(doc, "Trong public web, browser-worker.mjs tải tham số seed 42 và gọi browser-engine.mjs; xử lý CSV diễn ra trong worker phía trình duyệt. Ở local, demo_server.py nhận đường /api/lab/run hoặc /api/predict rồi gọi hàm Python trong demo.py. Hai đường cùng phục vụ demo nhưng không phải cùng backend.", size=9.3)

    # Chapter 12.
    page(doc, "12 Lời dẫn mẫu của Tín trên bục",
         "Em có thể dùng khung này để tập. Đừng đọc liên tục như thuộc lòng; nói từng ý, dừng cho người nghe nhìn màn hình và mời bạn khác tiếp khi đến phần của bạn ấy.")
    heading(doc, "Mở đầu khoảng 45 giây", 2)
    callout(doc, "LỜI DẪN", 
        "“Dạ, em kính chào quý thầy cô. Em là Nguyễn Trọng Tín, cùng bạn Trịnh Trâm Anh và bạn Hoàng Văn Vương Thu thực hiện đề tài dưới sự hướng dẫn của thầy Nguyễn Đăng Quang. Đề tài của nhóm so sánh học có giám sát với phát hiện bất thường trên bộ dữ liệu UNSW-NB15, đặc biệt trong tình huống một loại tấn công không xuất hiện khi huấn luyện. Em xin trình bày cách nhóm tổ chức thí nghiệm và minh họa cách đọc một quyết định của mô hình.”")
    heading(doc, "Giải thích protocol khoảng 60 giây", 2)
    callout(doc, "LỜI DẪN",
        "“Nhóm có bốn kịch bản, bốn mô hình và năm seed, thành 80 lượt huấn luyện. Ba kịch bản LOACO lần lượt giữ lại Reconnaissance, DoS và Exploits khỏi vùng phát triển; test vẫn có loại được giữ lại để đánh giá. Threshold được chọn từ điểm của Normal validation, rồi giữ nguyên khi chấm test.”", fill=PALE_GREEN)
    heading(doc, "Dẫn vào demo khoảng 2 phút", 2)
    add_p(doc, "“Bây giờ em xin chạy một ví dụ trên cùng bản ghi. Em chọn preset chỉ có Normal, scenario CS, mô hình RF và target 5%. Điểm dòng đầu là khoảng 0,705741, lớn hơn threshold khoảng 0,557282 nên hệ thống dự đoán Attack. Nhãn đối chiếu là Normal nên đây là báo nhầm.”", size=9.5)
    add_p(doc, "“Em đổi riêng target sang 1% và chạy lại. Điểm vẫn như cũ nhưng threshold tăng lên khoảng 0,805367. Điểm thấp hơn ngưỡng nên hệ thống dự đoán Normal, thành TN. Đây là demo inference với model đã lưu; em không huấn luyện lại.”", size=9.5)
    add_p(doc, "“Ví dụ này giải thích cách threshold đổi quyết định ở một dòng. Để kết luận mô hình tốt tới đâu, nhóm dùng kết quả trên toàn test, nhiều seed và các phạm vi/metric trong báo cáo.”", size=9.5)
    heading(doc, "Chuyển sang hỏi đáp và tự đánh giá", 2)
    callout(doc, "LỜI DẪN",
        "“Phần trình bày của nhóm đến đây. Nhóm xin phép được lắng nghe câu hỏi của thầy cô. Sau phần trao đổi, nhóm xin tự đánh giá những điểm đã làm được, những giới hạn hiện tại và hướng có thể cải thiện.”")
    add_p(doc, "Nếu câu hỏi nằm ngoài phần em phụ trách: nghe trọn câu, nhắc lại ý chính, trả lời phần em nắm được rồi mời đúng bạn phụ trách bổ sung. Nếu chưa có bằng chứng, nói thẳng “phần đó nhóm chưa triển khai/đo trong phiên bản này”.", size=9.4, color=BLUE, bold=True)

    # Chapter 13.
    page(doc, "13 Câu hỏi giảng viên có thể hỏi Tín",
         "Đọc câu trả lời, rồi thử gấp tài liệu và nói lại không nhìn. Câu trả lời tốt thường nêu phạm vi, bằng chứng và giới hạn; không cần dài hơn câu hỏi.")
    qa = [
        ("80 run được tính ra sao?", "4 kịch bản × 4 model × 5 seed = 80 lần fit. Hai threshold mỗi run không nhân đôi số lượt huấn luyện."),
        ("Vì sao cần giấu lớp trước khi chia?", "Để mẫu của lớp held-out không lọt vào train hoặc validation. Nếu đã thấy nó trước, kiểm tra sau không còn mô phỏng lớp chưa gặp."),
        ("Target 1% nghĩa là test FPR đúng 1% à?", "Không. Threshold được chọn trên Normal validation để hướng tới target đó; FPR test được đo riêng và có thể khác."),
        ("RF/XGB có biết attack_cat không?", "Không dùng cột attack_cat làm feature. Mô hình supervised học nhãn nhị phân label. attack_cat dùng để chia phạm vi và phân tích kết quả."),
        ("Public web gọi API nào?", "Bản public dùng browser worker JavaScript với tham số seed 42. Local Python demo có API loopback riêng. Em sẽ chỉ rõ đang dùng bản nào."),
        ("CSV không có nhãn làm được gì?", "Nếu đủ feature thì vẫn trả Normal/Attack. Không có label thật thì chưa tính được độ chính xác hay biết đúng/sai."),
        ("Web vừa huấn luyện model mới à?", "Không. Web dùng bundle/parameters đã lưu. Demo đang minh họa inference trên mẫu hoặc CSV tương thích."),
        ("Có dataset do nhóm tự thu chưa?", "Chưa có bộ traffic độc lập do nhóm tự thu trong phiên bản hiện tại. Các preset lấy mẫu từ UNSW-NB15."),
        ("Đã xây NIDS có chặn tấn công chưa?", "Chưa. Đề tài hiện đánh giá khả năng phát hiện trên dữ liệu; demo không bắt gói trực tiếp và không chặn traffic."),
        ("AP 0,985 có nghĩa đúng 98,5% không?", "Không. AP đo chất lượng xếp hạng precision/recall qua nhiều threshold, không phải tỷ lệ dự đoán đúng."),
        ("Sao nhìn all-test cao nhưng lớp mới thấp?", "All-test trộn các nhóm đã biết với lớp giữ lại. Vì vậy cần đọc riêng Normal + held-out và nêu đúng support."),
        ("Em dùng AI bao nhiêu phần trăm?", "Không có cách đo đáng tin để tự gán một tỷ lệ. Em trình bày trung thực công cụ đã hỗ trợ việc gì và phần nào em đã tự kiểm, hiểu, chỉnh; không nhận việc chưa làm."),
        ("Thí nghiệm có áp dụng mọi zero-day ngoài đời không?", "Không. LOACO là phép thử giữ lại một nhãn trong benchmark, không đại diện mọi dạng tấn công, môi trường hoặc thay đổi phân bố thực tế."),
    ]
    table(doc, ["Câu hỏi", "Trả lời ngắn có căn cứ"], qa, widths=[2.45, 4.15], font=7.8)
    callout(doc, "KHI CHƯA CHẮC",
        "“Dạ, trong phiên bản nhóm đã chạy, phần này chưa được đo/triển khai nên em không muốn khẳng định quá phạm vi. Nhóm có thể xem đó là hướng bổ sung, nhưng cần xác định dữ liệu và cách đánh giá trước.”", fill=PALE_GREEN)

    # Chapter 14.
    page(doc, "14 Mở báo cáo và code lúc cần",
         "Trang dưới đây là số trang trong trình xem PDF, tính từ trang bìa. Mở và đặt bookmark trước buổi báo cáo để không phải tìm giữa lúc đang căng thẳng.")
    table(doc, ["Tài liệu", "Trang của Tín", "Đọc để làm gì"], [
        ("Báo cáo tổng 62 trang", "12, 20–24, 53–58", "Phân công; protocol, pipeline, score, RF/XGB; kết quả, giới hạn và kết luận."),
        ("Báo cáo đợt 4 68 trang", "12, 25–29, 59–64", "Đối chiếu cùng mảng trong bản đợt 4 và phần bàn giao."),
        ("Web trình bày", "Bài toán, Thực nghiệm, Demo, Hỏi đáp, Tự đánh giá", "Luồng nói và thao tác minh họa."),
        ("Phần chuyên môn cá nhân", "docs/group_delivery_20261110/TrongTin/PHAN_CHUYEN_MON.md", "Ma trận, số demo, tái lập và lệnh local."),
    ], widths=[1.7, 1.6, 3.3], font=8.2)
    heading(doc, "URL cần mở sẵn", 2)
    for label, url in [
        ("Web trình bày và demo", "https://attq-nids.phttrongtin-nguyen-a46.workers.dev/"),
        ("Hồ sơ nhóm và theo từng thành viên", "https://attq-nids.phttrongtin-nguyen-a46.workers.dev/ho-so"),
        ("Báo cáo tổng PDF", "https://attq-nids.phttrongtin-nguyen-a46.workers.dev/downloads/NhomTLCN_tong_20261114.pdf"),
        ("Báo cáo đợt 4 PDF", "https://attq-nids.phttrongtin-nguyen-a46.workers.dev/downloads/NhomTLCN_dot4_20261114.pdf"),
        ("Nhánh trongtin", "https://github.com/YueLouis/tlcn-nids-unsw-nb15/tree/trongtin"),
    ]:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(label + ": ")
        set_run_font(r, 9, True, INK)
        hyperlink(p, url, url)
    heading(doc, "Chạy local trong repository", 2)
    add_p(doc, "Từ thư mục repo, lệnh đã dùng trong hồ sơ là:", size=9.4)
    t = doc.add_table(rows=1, cols=1)
    shade(t.cell(0, 0), "F1F4F5")
    set_cell_text(t.cell(0, 0), "$env:PYTHONPATH='src'\npython scripts/demo_server.py\n# mở http://127.0.0.1:4397/presentation/", 9, INK)
    add_p(doc, "Bản repository cần môi trường Python/phụ thuộc và bundle S42 đã có tại results/runs. Nếu máy lớp không mang repo/phụ thuộc, dùng gói offline v4 đã giải nén thử trước.", size=9.1)

    # Chapter 15.
    page(doc, "15 Chuẩn bị bục giảng và checklist",
         "Chạy trơn tru phụ thuộc cả trình duyệt, điện, màn hình, mạng và thao tác của người nói. Tập thử trên đúng laptop và cáp dự kiến để giảm việc phải xử lý mới tại lớp.")
    table(doc, ["Thời điểm", "Việc của Tín"], [
        ("Tối trước", "Tải/giải nén gói offline v4; mở một lần; chạy cả hai ngưỡng; để sẵn PDF, web và thư mục dự phòng."),
        ("Trước giờ", "Cắm sạc, tắt thông báo, đóng tab riêng tư; mở web tại màn đầu, mở PDF dự phòng ở tab khác."),
        ("Cắm HDMI", "Chọn đúng input trên TV/máy chiếu; thử Win + P → Duplicate; kiểm chữ nhỏ và vị trí màn hình."),
        ("Nếu lỗi hình", "Thử lại đầu cáp/cổng khác, Win + P → Duplicate; nếu cần thử 1920×1080 ở 60 Hz hoặc dùng PDF trên máy dự phòng."),
        ("Nếu mất mạng", "Mở demo offline bằng CHAY_DEMO.cmd, giữ cửa sổ server mở và dùng localhost được in ra."),
        ("Nếu demo không chạy", "Chuyển sang PDF slide; nói rõ lúc đó đang trình bày kết quả đã lưu, không giả vờ là vừa chạy inference."),
    ], widths=[1.25, 5.35], font=8.3)
    heading(doc, "Checklist tự đánh dấu", 2)
    for item in [
        "Em tự giải thích được câu hỏi nghiên cứu mà không đọc nguyên tên đề tài.",
        "Em tính được 4 × 4 × 5 = 80 và giải thích hai threshold không phải 160 lần fit.",
        "Em nói được vì sao loại lớp held-out trước khi chia train/validation.",
        "Em phân biệt được RF/XGB với IF/AE; biết score không đồng nghĩa xác suất chắc chắn đúng.",
        "Em mở đúng preset, chạy target 5% và 1%, đọc đúng FP rồi TN của dòng đầu.",
        "Em giải thích target FPR validation có thể khác FPR test.",
        "Em phân biệt web public browser worker với Python API local.",
        "Em nói đúng CSV không nhãn chỉ cho phép dự đoán, chưa tính đúng/sai.",
        "Em nêu đúng demo chưa thu traffic trực tiếp, chưa tự học và chưa chặn tấn công.",
        "Em đã thử HDMI và mở được phương án PDF/offline dự phòng.",
    ]:
        add_p(doc, "☐  " + item, size=9.1, after=3)
    callout(doc, "MỤC TIÊU CUỐI",
        "Đừng cố nhớ từng chữ. Em cần hiểu đường đi dữ liệu, nhìn đúng bằng chứng, giải thích một ví dụ rõ ràng và biết nói giới hạn khi chưa có kết quả. Tập lại đến khi em tự làm được mà không phải dò nút.", fill=PALE_GREEN)

    # Source note.
    page(doc, "Nguồn dùng để soạn sổ tay",
         "Nội dung kỹ thuật được đối chiếu với tài liệu phân công, mã, bảng số liệu và bộ phát hành hiện hành trong workspace ngày 18/11/2026.")
    table(doc, ["Nguồn", "Đường dẫn trong repository"], [
        ("Phân công và giao thức của Tín", "docs/group_delivery_20261110/TrongTin/PHAN_CHUYEN_MON.md"),
        ("Bàn giao bảo vệ riêng Tín", "docs/group_delivery_20261110/TrongTin/BAN_GIAO_BAO_VE_20261115.md"),
        ("CSV ví dụ hai ngưỡng", "docs/group_delivery_20261110/TrongTin/VI_DU_HAI_NGUONG.csv"),
        ("Bảng AP và operating points", "demo/presentation/assets/AP_MEAN_STD.csv; OPERATING_POINTS_MEAN_STD.csv"),
        ("Giao diện trình bày", "demo/presentation/index.html; presentation.js; browser-engine.mjs; browser-worker.mjs"),
        ("Mã nghiên cứu", "src/nids_benchmark/data.py; preprocessing.py; models.py; evaluation.py; runner.py; demo.py"),
        ("Hướng dẫn ba thành viên", "docs/management/BAN_GIAO_BAO_VE_20261113.md"),
        ("Bộ hiện hành", "docs/releases/final_handoff_20261114/README.md; reports/NhomTLCN_tong_20261114.pdf; reports/NhomTLCN_dot4_20261114.pdf"),
    ], widths=[2.0, 4.6], font=8.1)
    callout(doc, "GHI CHÚ VỀ TRẠNG THÁI",
        "Sổ tay này được chuẩn bị để em ôn và tập giải thích. Nó không thay cho việc em tự đọc các trang được giao, tự chạy demo, ghi góp ý thật hoặc xác nhận thay nhóm. Khi nội dung web, PDF hay mã đổi, hãy đối chiếu phiên bản mới nhất trước buổi báo cáo.")

    doc.core_properties.title = "Sổ tay báo cáo cá nhân Nguyễn Trọng Tín"
    doc.core_properties.subject = "Phần phụ trách protocol, pipeline, RF/XGBoost, tái lập và demo"
    doc.core_properties.author = ""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
