#全局通用配置类
class Config(object):
    """项目配置核心类"""
    #调试模式
    DEBUG=False

    # 配置日志
    # LOG_LEVEL = "DEBUG"
    LOG_LEVEL = "INFO"

    # 配置redis
    # 项目上线以后，这个地址就会被替换成真实IP地址，mysql也是
    REDIS_HOST = 'your host'
    REDIS_PORT = 3306
    REDIS_PASSWORD = 'your password'
    REDIS_POLL = 10

    #数据库连接格式
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://user:password@localhost:3306/test?charset=utf8"
    # 动态追踪修改设置，如未设置只会提示警告
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = False
    # 数据库连接池的大小
    SQLALCHEMY_POOL_SIZE=10
    #指定数据库连接池的超时时间
    SQLALCHEMY_POOL_TIMEOUT=10
    # 控制在连接池达到最大值后可以创建的连接数。当这些额外的 连接回收到连接池后将会被断开和抛弃。
    SQLALCHEMY_MAX_OVERFLOW=2

    #rabbitmq参数配置
    RABBITUSER="user"
    RABBITPASSWORD="password"
    RABBITHOST="your ip"
    RABBITPORT=3306
