from flask import Blueprint, request, jsonify, send_file
import os
from app.models import LedgerRecord
from app import db, logger
from app.utils.response import success, fail
from app.utils.excel_handler import read_ledger_excel, export_ledger_to_excel
from app.config import UPLOAD_FOLDER

ledger_bp = Blueprint("ledger", __name__)

# 工具函数：安全数值转换（全局通用，财务计算必备，面试亮点）
def safe_float(val, default=0.0):
    if val is None or str(val).strip() == "":
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        return default

# 新增单条流水 POST
@ledger_bp.route("/add", methods=["POST"])
def ledger_add():
    data = request.get_json()
    try:
        record = LedgerRecord(
            record_date=data["record_date"],
            record_type=data["record_type"],
            amount=safe_float(data.get("amount")), # 使用get + 安全转换
            classify=data.get("classify", ""),
            remark=data.get("remark", "")
        )
        db.session.add(record)
        db.session.commit()
        return jsonify(success(msg="流水记录新增成功", data={"id": record.id}))
    except Exception as e:
        db.session.rollback()
        logger.error(f"新增流水失败：{str(e)}")
        return jsonify(fail(msg=str(e)))

# Excel批量导入流水 POST
@ledger_bp.route("/upload_excel", methods=["POST"])
def upload_excel():
    if "file" not in request.files:
        return jsonify(fail(msg="未上传Excel文件"))
    file = request.files["file"]
    if not file.filename.endswith((".xlsx", ".xls")):
        return jsonify(fail(msg="仅支持xlsx/xls格式Excel文件"))
    save_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(save_path)
    try:
        df = read_ledger_excel(save_path)
        add_count = 0
        for _, row in df.iterrows():
            r = LedgerRecord(
                record_date=str(row["日期"]).split(" ")[0],
                record_type=row["收支类型"],
                amount=safe_float(row.get("金额")), # 修复空值风险
                classify=row.get("费用分类", ""),
                remark=row.get("备注", "")
            )
            db.session.add(r)
            add_count += 1
        db.session.commit()
        return jsonify(success(msg=f"Excel导入完成，新增{add_count}条流水记录"))
    except Exception as e:
        db.session.rollback()
        logger.error(f"Excel导入失败：{str(e)}")
        return jsonify(fail(msg=str(e)))

# 导出全部流水Excel GET
@ledger_bp.route("/export_excel", methods=["GET"])
def export_excel():
    records = LedgerRecord.query.order_by(LedgerRecord.id).all()
    save_name = "财务流水导出.xlsx"
    file_path = export_ledger_to_excel(records, save_name)
    return send_file(file_path, as_attachment=True, download_name=save_name)

# 查询所有流水 GET
@ledger_bp.route("/list", methods=["GET"])
def ledger_list():
    records = LedgerRecord.query.order_by(LedgerRecord.id).all()
    res_list = []
    for r in records:
        res_list.append({
            "id": r.id,
            "record_date": r.record_date,
            "record_type": r.record_type,
            "amount": r.amount,
            "classify": r.classify,
            "remark": r.remark,
            "create_time": str(r.create_time)
        })
    return jsonify(success(data=res_list))