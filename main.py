import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker

# Cấu hình
WEBHOOK_URL = "https://discord.com/api/webhooks/1339793068823416905/aPuOqS2PyCDBnib26_lfqL3k8M0cGbvdsBeIoufkWotzF4F5QvPdYHinJmOxWdOoKXRV"
PROXY_API_URL = "https://www.proxy-list.download/api/v1/get?type=https"  # API proxy miễn phí
fake = Faker()

def get_proxy():
    """Lấy proxy mới từ API"""
    try:
        response = requests.get(PROXY_API_URL)
        proxy_list = response.text.split("\r\n")
        return random.choice(proxy_list) if proxy_list else None
    except Exception as e:
        print("Lỗi lấy proxy:", e)
        return None

def setup_driver(proxy=None):
    """Cấu hình Selenium với proxy nếu có"""
    options = Options()
    if proxy:
        options.add_argument(f"--proxy-server={proxy}")

    options.add_argument("--disable-blink-features=AutomationControlled")  # Tránh bị phát hiện là bot
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def create_gmail(driver):
    """Tự động tạo tài khoản Gmail"""
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = f"{first_name.lower()}{last_name.lower()}{random.randint(1000, 9999)}"
    password = "AnTay@123456"

    driver.get("https://accounts.google.com/signup")
    time.sleep(3)

    try:
        driver.find_element(By.ID, "firstName").send_keys(first_name)
        driver.find_element(By.ID, "lastName").send_keys(last_name)
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.NAME, "Passwd").send_keys(password)
        driver.find_element(By.NAME, "ConfirmPasswd").send_keys(password)
        driver.find_element(By.XPATH, "//span[text()='Tiếp theo']").click()
        time.sleep(5)

        print(f"📌 Gmail: {username}@gmail.com | 🔑 Mật khẩu: {password}")

        # Gửi thông tin qua Discord Webhook
        requests.post(WEBHOOK_URL, json={"content": f"📌 Gmail: `{username}@gmail.com`\n🔑 Mật khẩu: `{password}`"})

        return True
    except Exception as e:
        print("❌ Tạo Gmail thất bại:", e)
        return False

def main():
    num_accounts = int(input("🔹 Nhập số lượng Gmail muốn tạo: "))
    success = 0

    for _ in range(num_accounts):
        proxy = get_proxy()
        print(f"🛠️ Đang dùng proxy: {proxy}")

        driver = setup_driver(proxy)
        if create_gmail(driver):
            success += 1
        driver.quit()

    print(f"✅ Đã tạo thành công {success}/{num_accounts} tài khoản Gmail!")

if __name__ == "__main__":
    main()
