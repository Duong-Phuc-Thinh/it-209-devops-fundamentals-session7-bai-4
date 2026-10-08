import os
import subprocess
import sys

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return True, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr

def main():
    print("=== Nginx Reverse Proxy Deployer ===")
    
    # Check for root privilege
    is_root = os.getuid() == 0 if hasattr(os, 'getuid') else False
    if not is_root:
        print("[Warning] Script is not running with root privileges.")
        print("Running in Dry-Run mode. Creating files in the current directory for testing.")
        print("To deploy to system, run: sudo python3 main.py\n")

    html_content = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Thông tin học viên</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; background-color: #f4f4f9; text-align: center; }
        .container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); display: inline-block; }
        h1 { color: #333; }
        p { font-size: 18px; color: #555; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Thông Tin Học Viên</h1>
        <p><strong>Họ và tên:</strong> Nguyễn Văn Kỳ Anh</p>
        <p><strong>Mã lớp:</strong> DevOps-07</p>
    </div>
</body>
</html>"""

    nginx_conf = """server {
    listen 80;
    server_name localhost;

    location / {
        root /var/www/html;
        index index.html index.htm;
        try_files $uri $uri/ =404;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8082;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}"""

    if is_root:
        # Write static file
        os.makedirs("/var/www/html", exist_ok=True)
        with open("/var/www/html/index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("[+] Created /var/www/html/index.html")

        # Write Nginx configuration
        os.makedirs("/etc/nginx/sites-available", exist_ok=True)
        with open("/etc/nginx/sites-available/spring-proxy.conf", "w", encoding="utf-8") as f:
            f.write(nginx_conf)
        print("[+] Created /etc/nginx/sites-available/spring-proxy.conf")

        # Symlink to sites-enabled
        os.makedirs("/etc/nginx/sites-enabled", exist_ok=True)
        symlink_path = "/etc/nginx/sites-enabled/spring-proxy.conf"
        if os.path.exists(symlink_path):
            os.remove(symlink_path)
        os.symlink("/etc/nginx/sites-available/spring-proxy.conf", symlink_path)
        print("[+] Symlink created in sites-enabled")

        # Test Nginx
        print("[*] Testing Nginx Syntax...")
        ok, out, err = run_command("nginx -t")
        if ok:
            print("[+] Nginx syntax is OK!")
            print(err)
            # Reload nginx
            reload_ok, _, reload_err = run_command("systemctl reload nginx")
            if reload_ok:
                print("[+] Nginx reloaded successfully!")
            else:
                print(f"[-] Reload failed: {reload_err}")
        else:
            print(f"[-] Nginx syntax check failed:\n{err}")
    else:
        # Local/dry-run writing
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        with open("spring-proxy.conf", "w", encoding="utf-8") as f:
            f.write(nginx_conf)
        print("[Dry-Run] Local 'index.html' and 'spring-proxy.conf' have been created successfully.")

if __name__ == '__main__':
    main()