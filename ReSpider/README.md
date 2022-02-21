# RestSpider

## 开始一个爬虫
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
    TemplateSpider().start()    
```

## 信号 (待开发)
### 添加信号参数
- 解决任务完成时偶先程序无法正常停止的问题(浏览器渲染下浏览器无法关闭)
- 中间件和管道增加关闭标志(is_closed)
- 根据传递的信号参数对是否关闭标志进行赋值，根据标志来开关中间件或管道
 
## ITEM
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
### 全局日志 (已完成)
- 日志写入.log文件
- 各个模块继承Logger类 (细节需要修改)


## JS渲染
### 无头模式下cookie问题 (维普为例)
