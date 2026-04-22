import os
from flask import Flask
from app.routes import event_routes
from app.models import init_db

def create_app():
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    # 設定 SECRET_KEY 用於 flash message 等 session 操作
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key_12345')

    # 初始化資料庫
    init_db()

    # 註冊 Blueprints
    app.register_blueprint(event_routes.bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
