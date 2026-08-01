from app import db
from datetime import datetime

#收支流水台账表
class LedgerRecord(db.Model):
   __tablename__ = "ledger_record"
   id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="主键ID")
   record_date = db.Column(db.String(20), nullable=False, comment="收支日期")
   record_date = db.Column(db.String(10), nullable=False, comment="收支类型，收入/支出")
   amount = db.Column(db.Float, nullable=False, comment="金额")
   classify = db.Column(db.String(30), comment="费用分类")
   remark = db.Column(db.String(200), comment="备注")
   create_time = db.Column(db.DateTime, default=datetime.now, comment="录入时间")

#理财测算结果存储表
class CalcResult(db.Model):
   __tablename__ = "calc_result"
   id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="主键ID")
   calc_type = db.Column(db.String(20), nullable=False, comment="测算类型：定投/理财/IRR/台账")
   content_json = db.Column(db.Text, nullable=False, comment="测算参数与结果JSON")
   create_time = db.Column(db.DateTime, default=datetime.now, comment="测算时间")