from flask import Flask
from config import config_map
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_session import Session
from flask_wtf import CSRFProtect
from logging.handlers import RotatingFileHandler
import logging
from ihome.utils.commons import ReConverter

# 数据库
db = SQLAlchemy()

# 创建redis连接对象
redis_store = None


# 设置日志的等级
logging.basicConfig(level=logging.INFO)
# 创建日志记录器，指明日志保存的路径、每个日志文件的大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
# 创建日志记录的格式
formatter = logging.Formatter('%(levelname)s %(filename)s :%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用）添加日志记录器
logging.getLogger().addHandler(file_log_handler)


# 工厂模式
def creat_app(config_name):
    """
    创建flask的应用对象
    :param config_name:
    :return:
    """
    app = Flask(__name__)
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)

    # 使用app初始化db
    db.init_app(app)

    # 初始化redis
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)

    # 利用flask-session，将session保存在redis中
    Session(app)

    # 开启CSRF防护
    CSRFProtect(app)

    # 添加自定义转化器
    app.url_map.converters["re"] = ReConverter

    # 注册蓝图
    from ihome import api_1_0  # 放在这里导入，延迟导包的时间可防止循环导包
    app.register_blueprint(api_1_0.api, url_prefix='/api/v1.0')

    # 为静态文件注册蓝图
    from ihome import web_html
    app.register_blueprint(web_html.html)

    return app
