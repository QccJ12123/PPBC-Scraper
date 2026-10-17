# 🌿 PPBC 药用植物图像批量获取工具 (PPBC-Scraper)

> 🌐 **项目主页**：[https://github.com/QccJ12123/PPBC-Scraper](https://github.com/QccJ12123/PPBC-Scraper)

由于中国植物图像库（PPBC）未提供官方批量下载接口，且页面采用动态懒加载机制，本项目基于 `Selenium` + `Requests` 编写了自动化获取脚本，用于构建 14 类药用植物（含 7 组易混淆对照品种）的图像数据集。

## ⚠️ 声明与注意事项
1. **学术用途**：本脚本仅供非商业的学术研究（如论文实验、个人学习）使用。
2. **版权说明**：抓取的图像版权归原拍摄者及 PPBC 所有，遵循 **CC BY-NC-ND 4.0** 协议。严禁用于商业用途。
3. **爬虫礼仪**：代码中已设置合理的请求间隔（默认 `1.5秒`），请勿恶意修改参数对服务器造成压力。

## 🛠️ 环境依赖
- Python 3.8+
- Google Chrome 浏览器
- ChromeDriver (Selenium 4.x 以上版本通常会自动管理，若报错请自行配置环境变量)

安装 Python 依赖库：
```bash
pip install selenium requests

📂 输出目录结构
运行脚本后，图片会自动按配置好的物种中文名分类，保存在当前目录的 dataset/raw/ 下：

text
dataset/raw/
├── 白术/
├── 苍术/
├── 忍冬（金银花）/
├── 钩吻（断肠草）/
├── 黄精/
├── 玉竹/
├── 栀子/
├── 芫花/
├── 吴茱萸/
├── 花椒/
├── 商陆/
├── 金钱豹（土党参）/
├── 绞股蓝/
└── 乌蔹莓/
🚀 使用说明
1. 配置 Cookie（重要）
PPBC 的图片列表接口对未登录用户隐藏了部分物种的数据。你必须在代码中配置你的 Cookie。

获取方式：

使用 Chrome 浏览器登录 PPBC。

按 F12 打开开发者工具，切换到 Network (网络) 标签。

刷新页面，在请求列表中找到 getphotopage.ashx 的请求。

在右侧 Headers -> Request Headers 中找到 Cookie，复制其完整字符串。

打开 download_ppbc.py，将字符串填入 COOKIE = "在此处填入你的真实Cookie字符串" 处。

注：Cookie 具有时效性，若发现下载失败、提示“暂无可见图片”，请重新登录并替换最新的 Cookie。

2. 配置物种列表 (SP号)
在代码的 SPECIES 字典中配置你需要抓取的物种。Key 为 PPBC 物种页 URL 中的 sp 号（如 https://ppbc.iplant.cn/sp/32987 中的 32987），Value 为保存的文件夹名称。

python
SPECIES = {
    "32987":  "白术",
    "32985":  "苍术",
    # ... 按此格式自行添加
}
3. 运行脚本
bash
python download_ppbc.py
⚙️ 核心逻辑解析
由于 PPBC 页面采用动态渲染（Ajax + 懒加载），单纯使用 requests 无法获取真实的图片数据。本脚本的解决思路如下：

模拟浏览器：使用 Selenium 驱动 Headless Chrome 访问物种页。

触发懒加载：通过执行 JavaScript 的 window.scrollTo 模拟用户向下滚动，等待图片 DOM 节点渲染。

提取真实 URL：利用 By.TAG_NAME 定位所有 <img> 标签，并配合正则表达式过滤出真实 CDN 地址（如 img*.iplant.cn），剔除网站 Logo、二维码等干扰图片。

流式下载与断点续传：使用 requests.get(..., stream=True) 下载图片，并检查本地是否已存在同名文件，实现断点续传，防止中断后重复下载。
