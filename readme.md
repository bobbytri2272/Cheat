# 🤖 Tool Giải Trắc Nghiệm Tự Động (Gemini AI + Overlay)

Công cụ tự động chụp màn hình vùng câu hỏi trắc nghiệm, gửi lên Gemini AI để phân tích và hiển thị kết quả trực tiếp dạng tối giản ngay trên góc màn hình.

---

## 📋 Tính năng chính
* **Thao tác nhanh gọn:** Giữ chuột trái 3 giây ở điểm A và điểm B để khoanh vùng câu hỏi.
* **Giao diện tối giản (Overlay):** Hiển thị trạng thái và đáp án trực tiếp ở góc trên bên trái màn hình mà không che khuất nội dung khác.
* **Trạng thái trực quan:**
  * `OK`: Khởi động thành công, sẵn sàng.
  * `?`: Đang chờ chọn điểm A (góc trên-trái).
  * `+`: Đã nhận điểm A, đang chờ chọn điểm B (góc dưới-phải).
  * `=`: Đang gửi ảnh và chờ AI xử lý.
  * `A/B/C/D`: Hiển thị đáp án chính xác trong 5 giây rồi tự quay về `?`.
* **Phím tắt thoát:** Nhấn phím **`F11` hai lần liên tiếp** bất cứ lúc nào để tắt chương trình.
* **Bảo mật API Key:** Đọc trực tiếp API key từ file `config.txt` riêng biệt.

---

## 🛠️ Yêu cầu hệ thống & Cài đặt thư viện

Chạy lệnh sau trong terminal để cài đặt các thư viện cần thiết:
```bash
pip install google-genai pynput keyboard pillow pyautogui pyinstaller