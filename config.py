import redis


class Config(object):
    """配置信息"""
    SECRET_KEY = 'FIRST_PRO_KEY(随便写)'

    # 数据库
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/ihome'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 配置redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # 配置flask-session
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 86400


class DevelopmentConfig(Config):
    """开发者模式的配置"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境模式的配置"""
    pass


config_map = {
    'develop': DevelopmentConfig,
    'product': ProductionConfig
}
