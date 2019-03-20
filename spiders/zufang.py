# -*- coding: utf-8 -*-
import scrapy
from lianjia.items import LianjiaItem


class ZufangSpider(scrapy.Spider):
    name = 'zufang'
    allowed_domains = ['sz.lianjia.com']
    start_url = 'https://sz.lianjia.com/zufang/'
    page_titles = 30
    Item = LianjiaItem()

    def start_requests(self):
        """
        开始页
        :return:
        """
        yield scrapy.Request(url=self.start_url, callback=self.parse_district)

    def parse_district(self, response):
        """
        解析深圳各个区
        :param response:
        :return:
        """
        districts = response.xpath('//li[contains(@data-id, "2300")]')
        for dis in districts:
            url = dis.xpath('./a/@href').get()
            district = dis.xpath('./a/text()').get()
            if url:
                yield scrapy.Request(url=response.urljoin(url), callback=self.parse_bizcircle, meta={'district':district})

    def parse_bizcircle(self, response):
        """
        解析各个区中的商圈
        :param response:
        :return:
        """
        bizcircles = response.xpath('//li[@class="filter__item--level3  "]')
        for biz in bizcircles:
            district = response.meta['district']
            url = biz.xpath('./a/@href').get()
            bizcircle = biz.xpath('./a/text()').get()
            if url:
                yield scrapy.Request(url=response.urljoin(url), callback=self.parse_page, meta={'bizcircle':bizcircle, 'district':district})


    def parse_page(self, response):
        """
        根据租房总量算出页数 page=int(total/30)
        :param response:
        :return:
        """
        title_num = response.xpath('//span[@class="content__title--hl"]/text()').get()
        max_page = int(int(title_num)/self.page_titles+1)
        for page in range(1, max_page+1):
            bizcircle = response.meta['bizcircle']
            district = response.meta['district']
            yield scrapy.Request(url=response.url+'pg{}'.format(page), callback=self.parse_content, meta={'bizcircle': bizcircle, 'district': district})

    def parse_content(self, response):
        """
        解析租房数据
        :param response:
        :return:
        """
        contents = response.xpath('//div[@class="content__list--item"]')
        for content in contents:
            url = response.urljoin(content.xpath('.//p[@class="content__list--item--title twoline"]/a/@href').get())
            title = content.xpath('.//p[@class="content__list--item--title twoline"]/a/text()').get().strip()
            district = response.meta['district']
            bizcircle = response.meta['bizcircle']
            area = content.xpath('.//p[@class="content__list--item--des"]//text()').re_first('(\d+㎡)')
            price = content.xpath('.//span[@class="content__list--item-price"]/em/text()').get().strip()
            apartment = content.xpath('.//p[@class="content__list--item--des"]//text()').re_first('(\d室\d厅\d卫)')
            company = content.xpath('.//p[@class="content__list--item--brand oneline"]//text()').get()
            if company:
                company = company.strip()
            for field in self.Item.fields:
                try:
                    self.Item[field] = eval(field)
                    yield self.Item
                except:
                    print('Field is not Defined: ' + field)








