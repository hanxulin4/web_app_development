from flask import Blueprint

# 建立 Blueprint 實例，方便之後註冊到 main app
bp = Blueprint('event_routes', __name__)

from . import event_routes
