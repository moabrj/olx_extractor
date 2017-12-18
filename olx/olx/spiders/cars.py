# -*- coding: utf-8 -*-
import scrapy

class CarsSpider(scrapy.Spider):
    name = 'cars'
    allowed_domains = ['ba.olx.com.br']
    start_urls = ['http://ba.olx.com.br/regiao-de-feira-de-santana-e-alagoinhas/veiculos-e-pecas/carros/']

    total_pages = 1 #add upper page limit

    def parse(self, response):
        items = response.xpath('//ul[@id="main-ad-list"]/li[not(contains(@class, "list_native"))]')
        for item in items:
            url = item.xpath('./a/@href').extract_first()
            yield scrapy.Request(url=url, callback=self.parse_detail)
        next_page = response.xpath(
            '//div[contains(@class, "module_pagination")]/a[@rel = "next"]/@href'
        ).extract_first()

        if next_page and self.total_pages > 0:
            yield scrapy.Request(
                url=next_page, callback=self.parse
            )
            self.total_pages = self.total_pages - 1


    def parse_detail(self, response):
        title = response.xpath(
            '//div/h1[contains(@class, "OLXad-title")]/text()'
        ).extract_first()
        price = response.xpath(
            '//div[contains(@class, "OLXad-price-box")]/span/text()'
        ).extract_first()
        year = response.xpath(
            '//span[contains(text(), "Ano:")]/following-sibling::strong/a/@title'
        ).extract_first()
        mileage = response.xpath(
            '//span[contains(text(), "Quilometragem:")]/following-sibling::strong/text()'
        ).extract_first()
        ports = response.xpath(
            '//span[contains(text(), "Portas:")]/following-sibling::strong/text()'
        ).extract_first()
        fuel = response.xpath(
            '//span[contains(text(), "Combustível:")]/following-sibling::strong/a/@title'
        ).extract_first()
        extras = response.xpath(
            '//ul[contains(@class, "OLXad-features-list")]/li/text()'
        ).extract()

        yield {
            'title': title,
            'price': price,
            'year': year,
            'mileage': mileage,
            'ports': ports,
            'fuel': fuel,
            'extras': extras
        }
