from flask import Blueprint, request, jsonify
import json
from app.service.finance_calc import *
from app.models import CalcResult
from app import db, logger
from app.utils.response import success, fail

calc_bp = Blueprint("calc", __name__)

# 定投测算接口 POST
@calc_bp.route("/invest", methods=["POST"])
def api_invest():
    data = request.get_json()
    try:
        res = calc_fixed_invest(
            monthly_amount=data["monthly_amount"],
            annual_yield=data["annual_yield"],
            invest_years=data["invest_years"],
            is_start=data.get("is_start", True)
        )
        # 存入数据库
        record = CalcResult(
            calc_type="定投测算",
            content_json=json.dumps({"params":data, "result":res}, ensure_ascii=False)
        )
        db.session.add(record)
        db.session.commit()
        return jsonify(success(data=res))
    except Exception as e:
        logger.error(f"定投测算接口异常：{str(e)}")
        return jsonify(fail(msg=str(e)))

# 理财年化测算接口 POST
@calc_bp.route("/product", methods=["POST"])
def api_product():
    data = request.get_json()
    try:
        res = calc_product_rate(
            principal=data["principal"],
            profit=data["profit"],
            days=data["days"],
            simple=data.get("simple", True)
        )
        record = CalcResult(
            calc_type="理财年化测算",
            content_json=json.dumps({"params":data, "result":res}, ensure_ascii=False)
        )
        db.session.add(record)
        db.session.commit()
        return jsonify(success(data=res))
    except Exception as e:
        logger.error(f"理财测算异常：{str(e)}")
        return jsonify(fail(msg=str(e)))

# IRR测算接口 POST
@calc_bp.route("/irr", methods=["POST"])
def api_irr():
    data = request.get_json()
    try:
        res = calc_irr(cash_flow=data["cash_flow"], total_days=data["total_days"])
        record = CalcResult(
            calc_type="IRR内部收益率",
            content_json=json.dumps({"params":data, "result":res}, ensure_ascii=False)
        )
        db.session.add(record)
        db.session.commit()
        return jsonify(success(data=res))
    except Exception as e:
        logger.error(f"IRR测算异常：{str(e)}")
        return jsonify(fail(msg=str(e)))