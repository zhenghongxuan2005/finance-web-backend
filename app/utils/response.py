def success(data=None, msg="操作成功", code=200):
    return{
        "code": code,
        "msg": msg,
        "data": data
    }

def fail(msg="操作失败", code=400, data=None):
    return{
        "code": code,
        "msg": msg,
        "data": data
    }