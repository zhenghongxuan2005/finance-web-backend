import os

# Flask基础配置
SECRET_KEY = "finance-system-2026-secret-key"
DEBUG = True

#MySQL数据库配置
DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_USER ="root"
DB_PASSWORD = "root"
DB_NAME = "finance_db"

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
SQLALCHEMY_TRACK_MODIFICATIONS = False

#文件存储路径（Excel导入导出）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "upload")
EXPORT_FOLDER = os.path.join(BASE_DIR, "export")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXPORT_FOLDER, exist_ok=True)

# 业务常量
GLOBAL_TAX_RATE = 0.13
SMALL_TAX_RATE = 0.03
YEAR_DAYS= 365