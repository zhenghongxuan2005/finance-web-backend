import numpy as np
import json
from app.config import GLOBAL_TAX_RATE, YEAR_DAYS
from app.utils.validator import check_positive_num

# 统一安全数值转换（和ledger蓝图保持一致，工程规范）
def safe_float(val, default=0.0):
    if val is None or str(val).strip() == "":
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        return default

def calculate_npv(rate, cash_flows):
    """计算净现值NPV，用于IRR迭代"""
    npv = 0.0
    for t, cf in enumerate(cash_flows):
        cf_safe = safe_float(cf)
        npv += cf_safe / ((1 + rate) ** t)
    return npv

# IRR真实年化（纯Python二分法，无第三方依赖）
def calc_irr(cash_flow, total_days, tol=1e-7, max_iter=2000):
    low = -0.9999
    high = 5.0
    # 清理列表中的空值
    clean_cashflow = [safe_float(x) for x in cash_flow]
    signs = [1 if x > 0 else -1 for x in clean_cashflow if x != 0]
    if len(set(signs)) < 2:
        raise Exception("现金流必须同时包含资金投入和资金收回，无法求解IRR")

    for _ in range(max_iter):
        mid = (low + high) / 2
        npv_val = calculate_npv(mid, clean_cashflow)
        if abs(npv_val) < tol:
            break
        if npv_val > 0:
            low = mid
        else:
            high = mid
    else:
        raise Exception("现金流数据异常,无法计算IRR，请检查现金流输入")

    period_irr = (low + high) / 2
    annual_irr = (np.power(1 + period_irr, YEAR_DAYS / safe_float(total_days)) - 1) * 100
    return {
        "现金流": cash_flow,
        "总投资天数": total_days,
        "真实IRR年化%": float(round(annual_irr, 4))
    }

# 定投测算
def calc_fixed_invest(monthly_amount, annual_yield, invest_years, is_start=True):
    monthly_amount = safe_float(monthly_amount)
    annual_yield = safe_float(annual_yield)
    invest_years = safe_float(invest_years)
    
    check_positive_num(monthly_amount, "月投金额")
    check_positive_num(annual_yield, "年化收益率")
    check_positive_num(invest_years, "投资年限")
    
    month_rate = annual_yield / 12
    total_period = invest_years * 12
    total_principal = monthly_amount * total_period
    annuity = (np.power(1 + month_rate, total_period) - 1) / month_rate
    final_asset = monthly_amount * annuity * (1 + month_rate) if is_start else monthly_amount * annuity
    profit = final_asset - total_principal
    return {
        "月定投金额": monthly_amount,
        "预期年化": float(round(annual_yield * 100, 2)),
        "投资年限": invest_years,
        "总本金": float(round(total_principal, 2)),
        "到期总资产": float(round(final_asset, 2)),
        "总收益": float(round(profit, 2)),
        "收益占本金%": float(round(profit / total_principal * 100, 2))
    }

# 理财年化测算
def calc_product_rate(principal, profit, days, simple=True):
    principal = safe_float(principal)
    profit = safe_float(profit)
    days = safe_float(days)
    
    check_positive_num(principal, "本金")
    check_positive_num(days, "持有天数")
    if simple:
        rate = (profit / principal) * (YEAR_DAYS / days) * 100
    else:
        total = principal + profit
        rate = (np.power(total / principal, YEAR_DAYS / days) - 1) * 100
    return {
        "本金": principal,
        "持有收益": profit,
        "持有天数": days,
        "年化收益率%": float(round(rate, 4))
    }

# 企业台账核算
def calc_ledger_total(income_list, expense_list, tax_rate=None):
    # 强制转为空列表兜底，防止传入None无法遍历
    if not isinstance(income_list, list):
        income_list = []
    if not isinstance(expense_list, list):
        expense_list = []
        
    tax_rate = safe_float(tax_rate if tax_rate is not None else GLOBAL_TAX_RATE)
    
    # 清理列表，过滤所有None
    income_clean = [safe_float(item) for item in income_list]
    expense_clean = [safe_float(item) for item in expense_list]

    for m in income_clean + expense_clean:
        if m > 0:
            check_positive_num(m, "收支金额")
            
    total_inc = sum(income_clean)
    total_exp = sum(expense_clean)
    gross = total_inc - total_exp
    
    tax = total_inc * tax_rate
    net = gross - tax
    return {
        "累计总收入": float(round(total_inc, 2)),
        "累计总支出": float(round(total_exp, 2)),
        "毛利润": float(round(gross, 2)),
        "预估增值税": float(round(tax, 2)),
        "税后净利润": float(round(net, 2))
    }