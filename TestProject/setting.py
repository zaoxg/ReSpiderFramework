# import os
# import re
#
# # DEFAULT SETTING
#
# WORKER_PATH = re.sub(r'([\\/]items$)|([\\/]spiders$)|([\\/]utils$)', '', os.getcwd())
#
# SCHEDULER = 'ReSpider.core.scheduler.Scheduler'  # python <Queue> 队列
# SCHEDULER = 'ReSpider.extend.redis.scheduler.RedisScheduler'  # redis 队列
# DUPEFILTER = 'ReSpider.extend.redis.dupefilter.RFPDupeFilters'
#
# DOWNLOADER = 'ReSpider.core.downloader.Downloader'
# SSL_FINGERPRINT = False  # ssl指纹
#
# PIPELINE_MANAGER = 'ReSpider.pipelines.PipelineManager'  # 管道管理
#
# # 重试
# RETRY_ENABLED = False
# RETRY_HTTP_CODES = [999, 600, 601, 602, 603, 604, 605, 606, 400, 401, 405, 408, 500, 502, 503, 504]
# MAX_RETRY_TIMES = 5  # 最大重试次数
#
# # 管道
# ITEM_PIPELINES = {
#     'ReSpider.pipelines.file.CSVPipeline': 4,
#     'ReSpider.pipelines.file.FilePipeline': 4,
#     # 'ReSpider.pipelines.redis.RedisPipeline': 5,
#     # 'ReSpider.pipelines.mysql.MySQLPipeline': 6
#     'ReSpider.pipelines.mongo.MongoPipeline': 8
# }
#
# # 默认User-Agent
# DEFAULT_USERAGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
#
# 下载中间件
DOWNLOADER_MIDDLEWARES = {
    # 'ReSpider.middlewares.useragent.UserAgentMiddleware': 2,
    # 'ReSpider.extend.puppeteer.downloadmiddleware.PuppeteerMiddleware': 5,
    'ReSpider.middlewares.retry.RetryMiddleware': 8
}
#
# # 并发请求
# TASK_LIMIT = CONCURRENT_REQUESTS = 4
# # 等待任务时间
# HEART_BEAT_TIME = 3
#
# # 下载延迟
# DOWNLOAD_DELAY = 0
#
# # MySQL配置
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_DB = 'crawler'
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = 'kcidea1509'
#
# # MongoDB配置
#
# MONGODB_HOST = '127.0.0.1'
# MONGODB_PORT = 27017
# MONGODB_DB = 'data_temp'
# MONGODB_USERNAME = None
# MONGODB_PASSWORD = None
# MONGODB_URL = None  # 如果需要使用密码, 需要使用url: mongodb://username:password@host:port
#
# # Redis配置
# REDIS_HOST = '127.0.0.1'
# REDIS_PORT = 6379
# REDIS_PASSWORD = None  # 'admin000'
# REDIS_DB = 0
#
# # 自定义任务队列
# REDIS_TASK_QUEUE = None
# # 自定义去重
# REDIS_DUPE_FILTERS = None
# # 保存失败任务
# SAVE_FAILED_TASK = True
# # 自定义失败任务队列
# FAILED_TASK_QUEUE = None
# # 重试失败任务
# RETRY_FAILED_TASK = False
#
# # 日志配置
# LOG_NAME = None
# LOG_PATH = f'{WORKER_PATH}/log/'  # 保存日志目录
# LOG_TO_CONSOLE = True  # 打印到控制台
# LOG_TO_FILE = False  # 保存到文件
# LOG_MODE = 'w'  # 写文件模式
# LOG_ENCODING = 'utf-8'  # log文件编码
# LOG_LEVEL_CONSOLE = 'DEBUG'  # 控制台输出log等级
# LOG_LEVEL_FILE = 'WARNING'  # 文件输出log等级
# LOG_FILE_SIZE = 5 * 1024 * 1024  # 每个日志文件大小, bytes
# LOG_BACKUP_COUNT = 7  # 日志文件保存数量
#
#
# # 请求次数统计
# REQUEST_COUNT_INTERVAL_TIME = 60
#
# # 爬虫常驻
# ALWAYS_RUNNING = False
#
# # 数据存储
# DATA_PATH = f'{WORKER_PATH}/data/'
#
# # PUPPETEER SETTING(浏览器渲染)
# PUPPETEER_SETTING = dict(
#     PUPPETEER_HEADLESS=False,  # 无头
#     PUPPETEER_EXECUTABLE_PATH='D:/Package/Chromium89/chrome.exe',
#     PUPPETEER_USER_DIR=None,  # 用户数据目录
#     # pyppeteer timeout
#     PUPPETEER_DOWNLOAD_TIMEOUT=60,
#     # pyppeteer browser window
#     PUPPETEER_WINDOW_WIDTH=1400,
#     PUPPETEER_WINDOW_HEIGHT=700
# )

# # cookies 池配置
# COOKIE_POOL_KEY = None
#
# # ip池配置
# PROXY_POOL_URL = None
