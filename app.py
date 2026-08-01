from flask import Flask, request, jsonify
from app.service.finance_calc import calc_fixed_invest, calc_product_rate, calc_irr, calc_ledger_total

app = Flask(__name__)

# 统一成功返回封装
def success_resp(data):
    return jsonify({
        "code": 0,
        "msg": "success",
        "data": data
    })

# 定投测算接口
@app.route("/api/finance/fixed_invest", methods=["POST"])
def api_fixed():
    body = request.get_json()
    res = calc_fixed_invest(
        monthly_amount=body["monthly_amount"],
        annual_yield=body["annual_yield"],
        invest_years=body["invest_years"],
        is_start=body.get("is_start", True)
    )
    return success_resp(res)

# 理财产品年化接口
@app.route("/api/finance/product_rate", methods=["POST"])
def api_product():
    body = request.get_json()
    res = calc_product_rate(
        principal=body["principal"],
        profit=body["profit"],
        days=body["days"],
        simple=body.get("simple", True)
    )
    return success_resp(res)

# IRR真实年化接口
@app.route("/api/finance/irr", methods=["POST"])
def api_irr():
    body = request.get_json()
    res = calc_irr(
        cash_flow=body["cash_flow"],
        total_days=body["total_days"]
    )
    return success_resp(res)

# 企业台账核算接口
@app.route("/api/finance/ledger", methods=["POST"])
def api_ledger():
    body = request.get_json() or {}
    # 兜底：如果前端不传、传null，自动替换为空列表
    income_list = body.get("income_list", []) or []
    expense_list = body.get("expense_list", []) or []
    tax_rate = body.get("tax_rate")
    res = calc_ledger_total(
        income_list=income_list,
        expense_list=expense_list,
        tax_rate=tax_rate
    )
    return success_resp(res)

# 全局异常捕获
@app.errorhandler(Exception)
def error_handler(e):
    return jsonify({
        "code": -1,
        "msg": str(e),
        "data": None
    }), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)