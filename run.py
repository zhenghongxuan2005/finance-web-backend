from app import create_app, db

app = create_app()

# 首次运行自动创建数据库表
with app.app_context():
    db.create_all()
    print("数据库表初始化完成")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)