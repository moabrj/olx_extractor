# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import smtplib

class OlxPipeline(object):
    def process_item(self, item, spider):
        price = item["price"]
        price = price.replace(".", "")
        price = price.replace("R$", "")
        price = price.replace(" ", "")

        if int(item["year"]) >= 2006 and int(price) <= 10500:
            car_msg = "Anuncio: " + item["title"]
            car_msg = car_msg + "Preco: " + item["price"]
            car_msg = car_msg + "Ano: " + item["year"]
            car_msg = car_msg + "Portas: " + item["ports"]
            self.msg = self.msg + "\n" + car_msg
        return item

    def open_spider(self, spider):
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        #the gmail blocks access from this type of app
        #self.server.login("yourmail@server.com", "password")
        self.msg = "\n"

    def close_spider(self, spider):
        self.server.sendmail("joao@gmail.com", "moab.rodriguess@gmail.com", self.msg)