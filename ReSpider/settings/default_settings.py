# DEFAULT SETTING

SCHEDULER = 'ReSpider.core.scheduler.Scheduler'  # python <Queue> 队列
# SCHEDULER = 'ReSpider.component.redis.scheduler.RedisScheduler'  # redis 队列

DOWNLOADER = 'ReSpider.core.downloader.Downloader'
SSL_FINGERPRINT = False  # ssl指纹

PIPELINE_MANAGER = 'ReSpider.pipelines.PipelineManager'  # 管道管理

# 重试
RETRY_ENABLED = False
RETRY_HTTP_CODES = [999, 600, 601, 602, 603, 604, 400, 401, 405, 408, 500, 502, 503, 504]
MAX_RETRY_TIMES = 5  # 最大重试次数

# 管道
ITEM_PIPELINES = {
    'ReSpider.pipelines.files.CSVPipeline': 4,
    'ReSpider.pipelines.files.FilesPipeline': 6,
    'ReSpider.pipelines.mongodb.MongoDBPipeline': 8
}

# 下载中间件
DOWNLOADER_MIDDLEWARES = {
    'ReSpider.middlewares.useragent.UserAgentMiddleware': 2,
    'ReSpider.middlewares.retry.RetryMiddleware': 8
}

# 并发请求
CONCURRENT_REQUESTS = 16

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

