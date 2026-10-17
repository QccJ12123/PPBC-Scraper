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
