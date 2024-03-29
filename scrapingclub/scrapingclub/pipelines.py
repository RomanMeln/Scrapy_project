# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class ProductPipelineSQLite:
    def open_spider(self, spider):
        self.connection = sqlite3.connect('products.db') # создаю базу данных
        self.cursor = self.connection.cursor() # переменная для обращения к базе данных

        # переменная с командой на создание таблицы
        create_query = '''
            CREATE TABLE IF NOT EXISTS product(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                price TEXT,
                description TEXT,
                image TEXT
                )
        '''

        # команда для готовности создания таблицы
        self.cursor.execute(create_query)

        # команда подтверждения создания таблицы
        self.connection.commit()



    def process_item(self, item, spider):
        # переменная с командой внесения данных в таблицу
        insert_query = '''
            INSERT INTO product(
                title,
                price,
                description,
                image
                )
            VALUES(
                ?,
                ?,
                ?,
                ?
                )
        '''

        self.cursor.execute(insert_query, (
                                            item.get('title'),
                                            item.get('price'),
                                            item.get('description'),
                                            item.get('image')
                                           )
                            )
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()
