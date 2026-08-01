# finance-web-backend
金融财会测算后端系统（Flask）
计算机专业实习项目｜面向理财定投测算、收支台账、Excel流水导入核算

## 📌 项目简介
本项目基于Python Flask搭建轻量化后端接口服务，面向财会、理财场景开发。
实现收支台账管理、定投IRR收益率测算、理财产品年化收益计算，支持Excel流水文件导入导出，使用MySQL持久化存储数据。
适合后端实习简历展示，采用分层工程化编码风格，包含异常捕获、日志记录、参数校验。

## 🛠 技术栈
- 语言：Python3.9+
- Web框架：Flask
- ORM：SQLAlchemy
- 数据库：MySQL
- 文件处理：pandas、openpyxl（Excel读写）
- 工具库：numpy（金融测算）
- 版本管理：Git + GitHub

## ✨ 核心功能
1. 收支台账管理：新增、查询、筛选收支记录
2. 定投收益测算：定期投资IRR内部收益率计算
3. 理财产品年化收益率测算
4. Excel流水批量导入、报表导出
5. 基础接口统一返回格式、全局异常处理
6. 日志持久化，便于线上问题排查

## 📂 项目结构
finance_web
├── .gitignore # Git 忽略文件配置
├── app.py # 项目启动入口
├── config.py # 全局配置（数据库、密钥）
├── requirements.txt # 项目依赖清单
├── models/ # 数据库模型
├── routes/ # 接口蓝图（路由分层）
├── services/ # 核心业务逻辑层
├── uploads/ # Excel 上传临时目录
├── logs/ # 运行日志
├── static/ # 静态资源


## 🚀 本地启动教程
### 1. 克隆项目
```bash
git clone https://github.com/zhenghongxuan2005/finance-web-backend.git
cd finance-web-backend
2. 创建虚拟环境（推荐）
python -m venv venv
# Windows激活
venv\Scripts\activate
3. 安装依赖
pip install -r requirements.txt
4. 修改数据库配置
打开config.py，填写本地 MySQL 账号信息。
5. 启动项目
python app.py
服务默认运行地址：http://127.0.0.1:5000

📝 接口示例
POST /api/ledger/add 新增收支流水
POST /api/calc/irr 定投 IRR 收益率测算
POST /api/excel/import 导入 Excel 财务流水

⚠️ 开发规范
禁止在代码硬编码账号密码，敏感配置建议使用.env环境文件
所有文件上传、输入接口增加参数校验
提交代码前遵循.gitignore 规范，不上传缓存、数据库、虚拟环境

👨‍💻 开发者
zhenghongxuan2005
GitHub：https://github.com/zhenghongxuan2005