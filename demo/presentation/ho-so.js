'use strict';

const repo = 'https://github.com/YueLouis/tlcn-nids-unsw-nb15';
const files = {
  total: 'downloads/NhomTLCN_tong_BAN_NHAP_20261113.pdf',
  round4: 'downloads/NhomTLCN_dot4_BAN_NHAP_20261113.pdf',
};
const people = {
  anh: {
    name: 'Trịnh Trâm Anh', area: 'DỮ LIỆU · NGUỒN HỌC THUẬT', branch: 'tramanh',
    task: 'Kiểm nguồn UNSW-NB15, 42 feature, cách chia tập, lớp bị giấu và giới hạn do trùng dữ liệu. Mở màn Dữ liệu và Thực nghiệm khi tập nói.',
    total: '16–19 và 33–36', totalStart: 16, round4: '21–24 và 39–42', round4Start: 21,
    sources: [
      ['docs/group_delivery_20261110/TramAnh/PHAN_CHUYEN_MON.md', 'Phần chuyên môn và nguồn cần đọc'],
      ['src/nids_benchmark/data.py', 'Chia dữ liệu và loại lớp held-out'],
      ['src/nids_benchmark/preprocessing.py', 'Vai trò feature và phạm vi fit'],
    ],
    questions: ['Vì sao bỏ id, label và attack_cat khỏi feature?', 'Lớp bị giấu được loại ở bước nào?', 'Vì sao official test phải giữ độc lập?'],
    review: 'Đọc chéo: Thu kiểm phần Anh; Anh đọc phần Tín và ghi góp ý thật.',
  },
  thu: {
    name: 'Hoàng Văn Vương Thu', area: 'MÔ HÌNH · NGƯỠNG · PHÂN TÍCH LỖI', branch: 'vuongthu',
    task: 'Kiểm IF/AE, ý nghĩa score, cách chọn ngưỡng và FPR/Recall/UADR/AP. Mở màn Kết quả và Hỏi đáp; giải thích cả điểm mạnh lẫn trường hợp bỏ sót.',
    total: '12–14, 19, 24–29 · đọc sâu 31–48', totalStart: 12,
    round4: '12–14, 24, 29–34 · đọc sâu 37–54', round4Start: 12,
    sources: [
      ['docs/group_delivery_20261110/VuongThu/PHAN_CHUYEN_MON.md', 'Phần chuyên môn và nguồn cần đọc'],
      ['src/nids_benchmark/evaluation.py', 'Score, ngưỡng và định nghĩa metric'],
    ],
    questions: ['Vì sao IF và AE chỉ học Normal?', 'Ngưỡng cho target FPR 1% và 5% lấy từ đâu?', 'Vì sao AP cao chưa đủ nói phát hiện lớp mới tốt?'],
    review: 'Đọc chéo: Tín kiểm phần Thu; Thu đọc phần Anh và ghi góp ý thật.',
  },
  tin: {
    name: 'Nguyễn Trọng Tín', area: 'PIPELINE · TÁI LẬP · DEMO', branch: 'trongtin',
    task: 'Kiểm RF/XGB, ma trận 80 run, khả năng tái lập, API, demo và phần kết luận chung. Mở màn Bài toán, Demo và Tự đánh giá khi tập nói.',
    total: '12, 20–24 và 53–58', totalStart: 12, round4: '12, 25–29 và 59–64', round4Start: 12,
    sources: [
      ['docs/group_delivery_20261110/TrongTin/PHAN_CHUYEN_MON.md', 'Phần chuyên môn và nguồn cần đọc'],
      ['scripts/demo_server.py', 'Server và API local'],
      ['demo/presentation/', 'Giao diện, worker và suy luận trên trình duyệt'],
    ],
    questions: ['Ma trận 80 run được tính thế nào?', 'Bản public thực hiện suy luận ở đâu?', 'CSV chưa có nhãn cho phép kết luận điều gì?'],
    review: 'Đọc chéo: Anh kiểm phần Tín; Tín đọc phần Thu và gom góp ý vào bản chung.',
  },
};

const tabs = Array.from(document.querySelectorAll('[role="tab"]'));
function selectTab(tab, focus = false) {
  tabs.forEach((item) => {
    const selected = item === tab;
    item.setAttribute('aria-selected', String(selected));
    item.tabIndex = selected ? 0 : -1;
    document.getElementById(item.getAttribute('aria-controls')).hidden = !selected;
  });
  if (focus) tab.focus();
}
tabs.forEach((tab, index) => {
  tab.addEventListener('click', () => selectTab(tab));
  tab.addEventListener('keydown', (event) => {
    let next;
    if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
    if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
    if (event.key === 'Home') next = 0;
    if (event.key === 'End') next = tabs.length - 1;
    if (next !== undefined) { event.preventDefault(); selectTab(tabs[next], true); }
  });
});

function showPerson(key) {
  const person = people[key];
  if (!person) return;
  document.querySelectorAll('[data-person]').forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.person === key)));
  document.getElementById('person-name').textContent = person.name;
  document.getElementById('person-area').textContent = person.area;
  document.getElementById('person-task').textContent = person.task;
  document.getElementById('person-review').textContent = person.review;
  document.getElementById('person-branch').href = `${repo}/tree/${person.branch}`;
  document.getElementById('person-total').href = `${files.total}#page=${person.totalStart}`;
  document.getElementById('person-total-pages').textContent = person.total;
  document.getElementById('person-round4').href = `${files.round4}#page=${person.round4Start}`;
  document.getElementById('person-round4-pages').textContent = person.round4;
  const sources = document.getElementById('person-code');
  sources.replaceChildren(...person.sources.map(([path, description]) => {
    const link = document.createElement('a');
    link.href = `${repo}/${path.endsWith('/') ? 'tree' : 'blob'}/main/${path}`;
    link.target = '_blank'; link.rel = 'noopener'; link.textContent = path;
    const note = document.createElement('span'); note.textContent = description; link.append(note);
    return link;
  }));
  document.getElementById('person-questions').replaceChildren(...person.questions.map((question) => {
    const item = document.createElement('li'); item.textContent = question; return item;
  }));
}
document.querySelectorAll('[data-person]').forEach((button) => button.addEventListener('click', () => showPerson(button.dataset.person)));
showPerson('anh');

document.getElementById('feedback-form').addEventListener('submit', (event) => {
  event.preventDefault();
  const name = document.getElementById('feedback-name').value;
  const note = document.getElementById('feedback-text').value.trim();
  const status = document.getElementById('feedback-status');
  if (!name || !note) { status.textContent = 'Chọn tên và ghi góp ý trước khi tải'; return; }
  const now = new Date();
  const writtenAt = now.toLocaleString('vi-VN', { timeZone: 'Asia/Ho_Chi_Minh', hour12: false });
  const text = `GÓP Ý HỒ SƠ NIDS\nBộ tài liệu 13/11/2026 · bảng đối chiếu 14/11/2026\nNgười ghi: ${name}\nThời điểm tải: ${writtenAt} (Việt Nam)\n\n${note}\n\nĐây là góp ý do người ghi tự gửi; tệp này không xác nhận đã duyệt hoặc đã nộp.\n`;
  const url = URL.createObjectURL(new Blob(['\uFEFF', text], { type: 'text/plain;charset=utf-8' }));
  const link = document.createElement('a');
  const stamp = new Intl.DateTimeFormat('sv-SE', { timeZone: 'Asia/Ho_Chi_Minh', year: 'numeric', month: '2-digit', day: '2-digit' }).format(now);
  link.href = url; link.download = `gop-y-nids-${stamp}.txt`; document.body.append(link); link.click(); link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  status.textContent = 'Đã tạo tệp TXT · tự gửi vào Zalo nhóm';
});
