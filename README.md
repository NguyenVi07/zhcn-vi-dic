# Chinese-Vietnamese Dictionary for NVDA (KtGame)

Add-on từ điển Trung-Việt chuyên biệt dành cho game thủ khiếm thị và người dùng NVDA tại Việt Nam.

## Giới thiệu
Add-on này giúp chuyển đổi các ký tự và cụm từ tiếng Trung sang âm đọc tiếng Việt (Hán Việt/Convert) một cách tức thì, hỗ trợ đắc lực cho việc chơi game, đọc tài liệu hoặc duyệt web tiếng Trung.

## Nguồn gốc dữ liệu
- **Dữ liệu gốc**: Phát triển bởi cộng đồng Convert truyện Trung-Việt (Tang Thư Viện, các diễn đàn Convert...).
- **Chuyển đổi định dạng**: Lê Trọng Tấn (tối ưu hóa để tương thích hoàn toàn với cơ chế của NVDA).
- **Phát triển Add-on**: KtGame.

## Tính năng nổi bật
- **Hiệu suất cực cao**: Sử dụng thuật toán Hash Table (O(1)) giúp tra cứu hơn 300.000 từ mà không gây lag máy.
- **Thông minh**: Tự động xử lý dấu câu, khoảng trắng và loại bỏ các trợ từ gây nhiễu (như liễu, đích) để câu văn trôi chảy hơn.
- **Tương thích rộng**: Hỗ trợ NVDA từ bản 2024.1 đến bản mới nhất 2026.1 (Python 3.13).

## Cách sử dụng
- **Phím tắt**: Nhấn `NVDA + Alt + V` để bật hoặc tắt addon.
- **Tín hiệu âm thanh**: 
  - Bíp cao: Đã bật.
  - Bíp thấp: Đã tắt.

## Cài đặt
1. Tải file `.nvda-addon` từ mục [Releases](https://github.com/NguyenVi07/zhcn-vi-dic/releases).
2. Mở file bằng NVDA và chọn "Yes" để cài đặt.
3. Khởi động lại NVDA.

## Giấy phép
Phát hành dưới giấy phép [GNU General Public License v2.0](LICENSE).
