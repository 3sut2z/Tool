import tkinter as tk
from tkinter import messagebox
import random
import string
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType

# Hàm để tạo tên Gmail ngẫu nhiên
def generate_random_email():
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{random_string}@gmail.com"

# Hàm sử dụng proxy để tạo Gmail
def create_gmail_with_proxy(proxy):
    # Cấu hình proxy cho Selenium
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Chạy không giao diện
    chrome_options.add_argument('--disable-gpu')

    proxy_config = Proxy()
    proxy_config.proxy_type = ProxyType.MANUAL
    proxy_config.http_proxy = proxy
    proxy_config.ssl_proxy = proxy

    webdriver.DesiredCapabilities.CHROME['proxy'] = proxy_config

    # Khởi tạo driver Selenium với proxy
    driver = webdriver.Chrome(options=chrome_options)

    # Mở trang tạo tài khoản Gmail
    driver.get("https://accounts.google.com/signup")
    time.sleep(2)

    # Điền thông tin tạo Gmail
    email = generate_random_email()
    driver.find_element(By.ID, "firstName").send_keys("AnTay")
    driver.find_element(By.ID, "lastName").send_keys("Tool")
    driver.find_element(By.ID, "username").send_keys(email)
    driver.find_element(By.NAME, "Passwd").send_keys("password123")
    driver.find_element(By.NAME, "ConfirmPasswd").send_keys("password123")
    driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]").click()
    time.sleep(2)

    # Thực hiện các bước tiếp theo như xác nhận và tạo tài khoản (có thể cần xử lý CAPTCHA)
    print(f"Đã tạo tài khoản Gmail: {email}")
    driver.quit()

# Hàm để thực hiện tạo nhiều Gmail
def create_multiple_gmails():
    try:
        num_gmails = int(gmail_count_entry.get())
        proxy = proxy_entry.get()

        if num_gmails <= 0:
            raise ValueError("Số lượng Gmail phải lớn hơn 0.")

        for _ in range(num_gmails):
            create_gmail_with_proxy(proxy)
            time.sleep(5)  # Thời gian giữa mỗi lần tạo tài khoản

        messagebox.showinfo("Thông báo", f"Đã tạo {num_gmails} tài khoản Gmail thành công!")
    except ValueError as e:
        messagebox.showerror("Lỗi", f"Vui lòng nhập số hợp lệ cho số lượng Gmail.\n{e}")

# Giao diện
root = tk.Tk()
root.title("AnTay Tool - Tạo Gmail Với Proxy")
root.geometry("500x400")

# Logo và giới thiệu
intro_text = """
AnTay Tool Là Một Công Cụ Đa Năng.
Tạo Gmail Với Proxy An Toàn, Không Bị Chặn.
"""
label_intro = tk.Label(root, text=intro_text, font=("Courier", 14), justify="center")
label_intro.pack(pady=10)

# Khung nhập proxy
proxy_label = tk.Label(root, text="Nhập Proxy (định dạng: IP:Port):")
proxy_label.pack()
proxy_entry = tk.Entry(root, width=40)
proxy_entry.pack(pady=5)

# Khung nhập số lượng Gmail
gmail_count_label = tk.Label(root, text="Nhập Số Lượng Gmail:")
gmail_count_label.pack()
gmail_count_entry = tk.Entry(root, width=10)
gmail_count_entry.pack(pady=5)

# Nút bắt đầu tạo Gmail
create_button = tk.Button(root, text="Tạo Gmail", command=create_multiple_gmails)
create_button.pack(pady=20)

root.mainloop()
