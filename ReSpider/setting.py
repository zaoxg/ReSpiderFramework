import os
import re

# DEFAULT SETTING

WORKER_PATH = re.sub(r'([\\/]items$)|([\\/]spiders$)|([\\/]utils$)', '', os.getcwd())

SCHEDULER = 'ReSpider.core.scheduler.Scheduler'  # python <Queue> 队列
# SCHEDULER = 'ReSpider.component.redis.scheduler.RedisScheduler'  # redis 队列

DOWNLOADER = 'ReSpider.core.downloader.Downloader'
SSL_FINGERPRINT = False  # ssl指纹

PIPELINE_MANAGER = 'ReSpider.pipelines.PipelineManager'  # 管道管理

# 重试
RETRY_ENABLED = False
RETRY_HTTP_CODES = [999, 600, 601, 602, 603, 604, 605, 400, 401, 405, 408, 500, 502, 503, 504]
MAX_RETRY_TIMES = 5  # 最大重试次数

# 管道
ITEM_PIPELINES = {
    'ReSpider.pipelines.file.CSVPipeline': 4,
    'ReSpider.pipelines.redis.RedisPipeline': 5,
    'ReSpider.pipelines.file.FilePipeline': 6,
    'ReSpider.pipelines.mongodb.MongoDBPipeline': 8
}

# 下载中间件
DOWNLOADER_MIDDLEWARES = {
    'ReSpider.middlewares.useragent.UserAgentMiddleware': 2,
    # 'ReSpider.extend.puppeteer.downloadmiddleware.PuppeteerMiddleware': 5,
    'ReSpider.middlewares.retry.RetryMiddleware': 8
}

# 并发请求
TASK_LIMIT = CONCURRENT_REQUESTS = 4
# 等待任务时间
HEART_BEAT_TIME = 3

# 下载延迟
DOWNLOAD_DELAY = 0

# MongoDB配置
MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DB = 'data_temp'

# Redis配置
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = None  # 'admin000'
REDIS_DB = 0

# 日志配置
LOG_NAME = None
LOG_PATH = f'{WORKER_PATH}/log/'  # 保存日志目录
LOG_TO_CONSOLE = True  # 打印到控制台
LOG_TO_FILE = False  # 保存到文件
LOG_MODE = 'w'  # 写文件模式
LOG_ENCODING = 'utf-8'  # log文件编码
LOG_LEVEL_CONSOLE = 'DEBUG'
LOG_LEVEL_FILE = 'WARNING'

# 请求次数统计
REQUEST_COUNT_INTERVAL_TIME = 60

# 爬虫常驻
ALWAYS_RUNNING = False

# 数据存储
DATA_PATH = f'{WORKER_PATH}/data/'

# PUPPETEER SETTING(浏览器渲染)
PUPPETEER_SETTING = dict(
    PUPPETEER_HEADLESS=False,  # 无头
    PUPPETEER_EXECUTABLE_PATH='D:/Package/Chromium64/chrome.exe',
    PUPPETEER_USER_DIR=None,  # 用户数据目录
    # pyppeteer timeout
    PUPPETEER_DOWNLOAD_TIMEOUT=60,
    # pyppeteer browser window
    PUPPETEER_WINDOW_WIDTH=1400,
    PUPPETEER_WINDOW_HEIGHT=700
)

# cookies 池配置
COOKIE_POOL_KEY = None

# ip池配置
PROXY_POOL_URL = None

# 加载自定义的setting
# 需要把自定义的path加入到这里（作用域）
import sys
sys.path.append(WORKER_PATH)
sys.path.append(os.path.dirname(WORKER_PATH))

try:
    from setting import *
except ModuleNotFoundError:
    pass
# 兼容老版本配置
try:
    from settings import *

    # 日志
    LOG_PATH = LOG_PATH or LOG_FILE_DIRECTORY
    LOG_LEVEL_CONSOLE = STREAM_HANDLER_LEVEL
    LOG_LEVEL_FILE = FILE_HANDLER_LEVEL
    # 数据文件
    # DATA_PATH = DATA_FILE_DIRECTORY
    # 浏览器渲染
    PUPPETEER_SETTING.update({
        'PUPPETEER_HEADLESS': PUPPETEER_HEADLESS,
        'PUPPETEER_EXECUTABLE_PATH': PUPPETEER_EXECUTABLE_PATH,
        'PUPPETEER_USER_DIR': PUPPETEER_USER_DIR
    })
except ModuleNotFoundError:
    pass
except NameError:
    pass
