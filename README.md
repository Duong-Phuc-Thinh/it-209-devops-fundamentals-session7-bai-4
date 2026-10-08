# Cấu hình Reverse Proxy Nginx cho ứng dụng Spring Boot

Bài tập thực hành cấu hình **Nginx** làm Reverse Proxy điều hướng và phân chia lưu lượng mạng:
- Lưu lượng tĩnh (tại `/`): được phục vụ trực tiếp từ thư mục `/var/www/html/` qua cấu hình Nginx.
- Lưu lượng động (tại `/api/`): chuyển tiếp an toàn tới Spring Boot backend đang hoạt động tại cổng `8082` phía sau.

## Cấu trúc thư mục
```bash
homework/session_07/ex4/
├── index.html           # Trang tĩnh hiển thị thông tin học viên
├── spring-proxy.conf    # Tệp cấu hình máy chủ ảo Nginx
├── main.py              # Script Python hỗ trợ triển khai nhanh tự động
└── README.md            # Báo cáo và hướng dẫn vận hành
```

## Hướng dẫn cài đặt thủ công

1. **Chuẩn bị thư mục trang tĩnh:**
   ```bash
   sudo mkdir -p /var/www/html/
   sudo cp index.html /var/www/html/index.html
   ```

2. **Đưa tệp cấu hình vào Nginx:**
   ```bash
   sudo cp spring-proxy.conf /etc/nginx/sites-available/spring-proxy.conf
   ```

3. **Kích hoạt Virtual Host:**
   ```bash
   sudo ln -sf /etc/nginx/sites-available/spring-proxy.conf /etc/nginx/sites-enabled/
   ```

4. **Kiểm tra cú pháp và khởi động lại Nginx:**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

---

## Sử dụng Python Deployer Script (Tự động)

Nếu muốn tự động hóa toàn bộ quá trình cài đặt, chạy symlink và nạp lại cấu hình, bạn có thể chạy tệp `main.py` bằng quyền root:
```bash
sudo python3 main.py
```

---

## Kết quả kiểm tra (Verification Result)

### 1. Kiểm tra cú pháp Nginx (`sudo nginx -t`)
```text
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

### 2. Truy cập cổng 80 mặc định (`/`)
```bash
curl -I http://localhost/
```
**Phản hồi kì vọng:**
```text
HTTP/1.1 200 OK
Server: nginx/1.18.0 (Ubuntu)
Date: Mon, 20 Oct 2023 12:00:00 GMT
Content-Type: text/html
Content-Length: 624
Last-Modified: Mon, 20 Oct 2023 11:30:00 GMT
Connection: keep-alive
ETag: "653266e8-270"
Accept-Ranges: bytes
```

### 3. Truy cập Endpoint Spring Boot Backend (`/api/health`)
```bash
curl -I http://localhost/api/health
```
**Phản hồi kì vọng:**
```text
HTTP/1.1 200 OK
Server: nginx/1.18.0 (Ubuntu)
Date: Mon, 20 Oct 2023 12:01:00 GMT
Content-Type: application/json
Connection: keep-alive
Keep-Alive: timeout=60
```