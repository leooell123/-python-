# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScrapyDushuPipeline:
    def open_spider(self,spider):
        self.fp=open('book.json','w',encoding='utf-8')

    def process_item(self, item, spider):

        self.fp.write(str(item))
        return item

    def close_spider(self,spider):
        self.fp.close()

from scrapy.utils.project import get_project_settings
import pymysql
class MysqlPipeline:
    #init是获取settings中的连接参数
    def open_spider(self,spider):
# DB_HOST = 'localhost'
# DB_PORT = 3306
# DB_USER = 'root'
# DB_PASSWORD = 'leo'
# DB_NAME = 'spider'
# DB_CHARSET = 'utf8'
        settings = get_project_settings()
        self.host = settings['DB_HOST']
        self.port = settings['DB_PORT']
        self.user = settings['DB_USER']
        self.pwd = settings['DB_PASSWORD']
        self.name = settings['DB_NAME']
        self.charset = settings['DB_CHARSET']
        self.connect()
    # 连接数据库并且获取cursor对象
    def connect(self):
        self.conn = pymysql.connect(host=self.host,
                                    port=self.port,
                                    user=self.user,
                                    password=self.pwd,
                                    db=self.name,
                                    charset=self.charset)
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        sql = 'insert into books(title,author,src) values("{}","{}", "{}")'.format(item['title'], item['author'], item['src'])
        # 执行sql语句
        self.cursor.execute(sql)
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.close()
        self.cursor.close()