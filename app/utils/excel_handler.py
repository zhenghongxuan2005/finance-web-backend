import pandas as pd
import os
from openpyxl import Workbook
from app import logger
from app.config import UPLOAD_FOLDER, EXPORT_FOLDER
from app.models import LedgerRecord
from app import db

# 读取上传的Excel流水文件
def read_ledger_excel(file_path):
    try:
        df = pd.read_excel(file_path, engine="openpyxl")
        #校验必填列
        need_cols = ["日期", "收支类型", "金额"]
        miss = [c for c in need_cols if c not in df.columns]
        if miss:
            raise Exception(f"Excel缺少列: {miss}")
        #清洗数据
        df["日期"] = pd.to_datetime(df["日期"], errors="coerce")
        df = df.dropna(subset=need_cols)
        df["金额"] = df["金额"].astype(float)
        return df
    except Exception as e:
        logger.error(f"读取Excel失败: {str(e)}")
        raise e

#将台账数据导出为Excel文件
def export_ledger_to_excel(record_list, save_name):
    save_path = os.path.join(EXPORT_FOLDER, save_name)
    wb = Workbook()
    ws = wb.active
    ws.title = "收支流水"
    #表头
    headers = ["ID", "日期", "收支类型", "金额", "费用类型", "备注", "录入时间"]
    ws.append(headers)
    #写入数据
    for r in record_list:
        row = [
            r.id, r.record_date, r.record_type, r.amount,
            r.classify, r.remark, str(r.create_time)
        ]
        ws.append(row)
    wb.save(save_path)
    return save_path