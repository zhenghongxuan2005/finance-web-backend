from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
from app.config import *

# 全局数据库实例
db = SQLAlchemy

#日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("FinanceWebSystem")

def create_app():
    app = Flask(__name__)
    #加载配置
    app.config.from_object("app.config")
    #绑定数据库
    db.init_app(app)

    #注册接口蓝图
    from app.api.calc_api import calc_bp
    from app.api.ledger_api import ledger_bp
    app.register_blueprint(calc_bp, url_prefix="/api/calc")
    app.register_blueprint(ledger_bp, url_prefix="/api/ledger")

    return app