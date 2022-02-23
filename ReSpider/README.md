# ReSpider

## 开始一个爬虫
> 爬虫继承自 <ReSpider.Spider> 类
```
import ReSpider


class TestSpider(ReSpider.Spider):
    # 自定义配置
    __custom_setting__ = {}
    start_urls = []

    def start_requests(self):
        pass

    def parse(self, response):
        pass


if __name__ == '__main__':
    TestSpider().start()    
```

## 自定义设置
```
__custom__ = {
    'TASK_LIMIT': 1,  # 设置并发数, 默认为1
    'SCHEDULER': 'ReSpider.extend.redis.scheduler.RedisScheduler',  # 设置任务队列, 默认为内存
    'DOWNLOAD_DELAY': 1,  # 下载延迟, 默认为0
    'RETRY_ENABLED': True,  # 重试, 设置为True开启重试, 默认关闭
    'SSL_FINGERPRINT': False  # ssl指纹, 默认关闭, 在创建ssl上下文时会阻塞, 开启后并发会降为1 
}
```

## 中间件设置
```
# 管道
ITEM_PIPELINES = {
    'ReSpider.pipelines.files.CSVPipeline': 4,
    'ReSpider.pipelines.redis.RedisPipeline': 5,
    'ReSpider.pipelines.files.FilesPipeline': 6,
    'ReSpider.pipelines.mongodb.MongoDBPipeline': 8
}

# 下载中间件
DOWNLOADER_MIDDLEWARES = {
    'ReSpider.middlewares.useragent.UserAgentMiddleware': 2,
    # 'ReSpider.extend.puppeteer.downloadmiddleware.PuppeteerMiddleware': 5,
    'ReSpider.middlewares.retry.RetryMiddleware': 8
}
```

## 信号 (待开发)
### 添加信号参数
- 解决任务完成时偶先程序无法正常停止的问题(浏览器渲染下浏览器无法关闭)
- 中间件和管道增加关闭标志(is_closed)
- 根据传递的信号参数对是否关闭标志进行赋值，根据标志来开关中间件或管道
 
## 保存数据
### Item
一般的数据实体
```
from ReSpider import item
data = DataItem({'name': 'ReSpider'}, **kwargs)
```
### xxListItem
数据实体列表, 可以传入一个list来构造
```
from ReSpider import item
data_list_item = DataListItem([1, 2, 3], **kwargs)
```
### 保存数据
```
# 二进制数据
io_item = item.IoItem(b'hello world', filename='hello world', filetype='bin')

# 文件类型, filetype 为文件类型
file_item = item.FileItem('hello world', filename='hello world', filetype='text')

# 表格数据
csv_item = item.CSVItem({'name': '张三', 'age': 14}, filename='hello world')

# 多行使用list
csv_list = item.CSVListItem([{'name': '张三', 'age': 14}, {'name': '李四', 'age': 19}], filename='法外狂徒')

# 使用yield来保存数据
data = item.DataItem()
yield data
```

## Log
### 日志设置
```
__custom_setting__ = {
    'LOG_PATH': None,  # log文件写入位置
    'LOG_TO_CONSOLE': True,  # 输出日志到控制台, 默认开启
    'LOG_LEVEL_CONSOLE': 'DEBUG',  # 输出日志到控制台级别, 默认DEBUG
    'LOG_TO_FILE': False,  # 输出日志到文件, 默认关闭, 设置为True开启
    'LOG_LEVEL_FILE': 'WARNING'  # 输出日志到文件级别, 默认WARNING
}
```


## JS渲染
### 无头模式下cookie问题
