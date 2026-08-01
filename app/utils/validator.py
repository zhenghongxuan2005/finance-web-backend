def check_positive_num(num, desc):
    if not isinstance(num, (int, float)):
        raise ValueError(f"{desc} 必须为数字")
    if num <= 0:
        raise ValueError(f"{desc} 必须大于0")