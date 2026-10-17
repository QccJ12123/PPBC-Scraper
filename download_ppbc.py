# -*- coding: utf-8 -*-
"""
PPBC 图片批量下载工具 - Selenium 版
用于获取中国植物图像库的植物生态照，仅供非商业学术研究使用。
"""
import os
import re
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# ========== 配置区 ==========
# 1. 图片保存路径（默认保存在当前目录下的 dataset/raw）
SAVE_ROOT = r"./dataset/raw"

# 2. 填入你在浏览器抓取的 PPBC Cookie
# 获取方法：登录PPBC -> F12 -> 网络 -> 找 getphotopage.ashx 请求 -> 复制 Request Headers 里的 Cookie
COOKIE = "在此处填入你的真实Cookie字符串"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://ppbc.iplant.cn/",
    "Cookie": COOKIE
}

INTERVAL = 1.5      # 请求间隔，防止给服务器造成压力
TIMEOUT = 20
MAX_IMAGES = 200    # 每个物种最大下载数量
SCROLL_TIMES = 10   # 页面滚动次数（触发懒加载）

# 3. 配置要下载的物种
# Key 为 PPBC 的 SP号 (如 ppbc.iplant.cn/sp/32987 中的 32987)
# Value 为保存时的文件夹名称
SPECIES = {
    "32987":  "白术",
    "32985":  "苍术",
    "31334":  "忍冬（金银花）",
    "26552":  "钩吻（断肠草）",
    "34320":  "黄精",
    "34298":  "玉竹",
    "27731":  "栀子",
    "22679":  "芫花",
    "221895": "吴茱萸",
    "20685":  "花椒",
    "12476":  "商陆",
    "234807": "金钱豹（土党参）",
    "23335":  "绞股蓝",
    "766607": "乌蔹莓",
}

# ========== 核心逻辑 ==========
def safe_filename(name):
    return re.sub(r'[\\/:*?"<>|]', "_", name)

def is_plant_image(url):
    if not re.search(r"img\d\.iplant\.cn/.+\.(jpg|jpeg|png)$", url, re.IGNORECASE):
        return False
    bad_keywords = ["logo", "qrcode", "frps", "foc", "cvh", "bkl", "search", "icon", "anniu", "ppbcbiglogo", "sitelogo"]
    return not any(kw in url.lower() for kw in bad_keywords)

def download_image(img_url, save_path):
    try:
        r = requests.get(img_url, headers=HEADERS, timeout=TIMEOUT, stream=True)
        r.raise_for_status()
        with open(save_path, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"    [!] 下载失败: {img_url} ({e})")
        return False

def crawl_species(driver, sp, name):
    print(f"\n===== 开始：{name}（sp={sp}） =====")
    save_dir = os.path.join(SAVE_ROOT, safe_filename(name))
    os.makedirs(save_dir, exist_ok=True)

    existing = [f for f in os.listdir(save_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    if len(existing) >= MAX_IMAGES:
        print(f"  已有 {len(existing)} 张，跳过")
        return

    url = f"https://ppbc.iplant.cn/sp/{sp}"
    print(f"  打开页面：{url}")
    driver.get(url)
    time.sleep(5)

    print(f"  滚动页面 {SCROLL_TIMES} 次...")
    for _ in range(SCROLL_TIMES):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.8)
    time.sleep(2)

    imgs = driver.find_elements(By.TAG_NAME, "img")
    img_urls = []
    for img in imgs:
        src = img.get_attribute("src") or ""
        if is_plant_image(src):
            if src.startswith("//"):
                src = "https:" + src
            if src not in img_urls:
                img_urls.append(src)

    print(f"  找到 {len(img_urls)} 张图片")
    if not img_urls:
        print("  [×] 未找到图片")
        return

    count_ok = 0
    for idx, img_url in enumerate(img_urls[:MAX_IMAGES], 1):
        ext = os.path.splitext(img_url.split("?")[0])[1] or ".jpg"
        filename = f"{safe_filename(name)}_{idx:04d}{ext}"
        save_path = os.path.join(save_dir, filename)
        if os.path.exists(save_path):
            count_ok += 1
            continue
        print(f"  [{idx}/{len(img_urls)}] {img_url}")
        if download_image(img_url, save_path):
            count_ok += 1
        time.sleep(INTERVAL)

    print(f"===== {name} 完成，共 {count_ok} 张 =====\n")

def main():
    os.makedirs(SAVE_ROOT, exist_ok=True)
    print(f"保存目录：{SAVE_ROOT}")
    print(f"共 {len(SPECIES)} 个物种，每类上限 {MAX_IMAGES} 张\n")

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument(f"user-agent={HEADERS['User-Agent']}")

    driver = webdriver.Chrome(options=options)

    try:
        for sp, name in SPECIES.items():
            try:
                crawl_species(driver, sp, name)
            except Exception as e:
                print(f"  [×] {name} 出错：{e}")
    finally:
        driver.quit()
        print("\n全部完成。")

if __name__ == "__main__":
    main()