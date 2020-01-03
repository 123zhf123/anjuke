import re
from json import loads

import scrapy
from scrapy_redis.spiders import RedisSpider

from anjuke.utils import ParseFont, get_re_result
from anjuke.items import AnjukeFyRent2
from anjuke.custom_settings import ningbo_fangyuan


class NingboFangyuan(RedisSpider):
    name = 'ningbo_fangyuan'
    tag = 'ningbo'
    city = '宁波'
    redis_key = 'ningbo:urls'
    custom_settings = ningbo_fangyuan

    price_trend_url = 'https://nb.zu.anjuke.com/v3/ajax/getPriceTrend?comm_id={}&block_id={}&area_id={}&num={}'

    def parse(self, response):
        urls = response.xpath('//div[@class="sub-items sub-level2"]/a')
        for url in urls[1:]:
            link = url.xpath('./@href').get()
            block_name = url.xpath('./text()').get()
            if block_name:
                block_name = block_name.strip()
            yield scrapy.Request(
                url=link,
                dont_filter=True,
                callback=self.parse2,
                meta={'block_name': block_name, 'dont_redirect': True}
            )

    def parse2(self, response):
        houses = response.xpath('//div[@class="list-content"]/div[@class="zu-itemmod"]')
        for house in houses:
            link = house.xpath('./@link').get()
            addr = house.xpath('.//address[@class="details-item"]')
            addr = addr.xpath('string(.)').get()
            if addr:
                addr = addr.replace('&nbsp;', '').split('\n')[-1].strip()
            item = AnjukeFyRent2()
            item['block_name'] = response.meta['block_name']
            item['addr'] = addr
            item['link'] = link
            yield scrapy.Request(
                url=link,
                callback=self.parse_detail,
                meta={'item': item, 'dont_redirect': True}
            )
        next_page = response.xpath('//div[@class="multi-page"]/a[@class="aNxt"]/@href').get()
        if next_page:
            yield scrapy.Request(
                url=next_page,
                callback=self.parse2,
                dont_filter=True,
                meta={
                    'block_name': response.meta['block_name'],
                    'dont_redirect': True
                }
            )

    def parse_detail(self, response):
        item = response.meta['item']
        name = response.xpath('//h3[@class="house-title"]/div/text()').get()
        type_ = get_re_result(r'类型.*?"info">(.*?)</span>.*?</li>', response.text, 1, re.S)
        house_area = get_re_result(r'面积.*?"font-weight: normal;">(.*?)</b>.*?</li>', response.text, 1, re.S)
        house_id = get_re_result(r'fangyuan/(\d+)\?', response.url, 1)

        lon_lat = re.search(r'prop_view_popup#l1=(.*?)&l2=(.*?)&', response.text)
        lon = None
        lat = None
        if lon_lat:
            lat = lon_lat.group(1)
            lon = lon_lat.group(2)

        release_time = response.xpath('//div[@class="right-info"]/b/text()').get()
        community_name = response.xpath('//ul[@class="house-info-zufang cf"]/li[8]/a/text()').get()
        district_name = response.xpath('//ul[@class="house-info-zufang cf"]/li[8]/a[2]/text()').get()
        house_type = response.xpath('//ul[@class="house-info-zufang cf"]/li[2]/span[@class="info"]').get()
        rent_price = response.css('span.price > em > b::text').get()
        base64_str = re.search(r"charset=utf-8;base64,(.*?)'\)", response.text)
        if base64_str:
            base64_str = base64_str.group(1)
            parse_font = ParseFont(base64_str)
            release_time = parse_font.get_page_font(release_time)
            house_area = parse_font.get_page_font(house_area)
            house_type = parse_font.get_page_font(re.sub(r'<.+?>', '', house_type))
            rent_price = parse_font.get_page_font(rent_price)

            item['tag'] = self.tag
            item['city'] = self.city
            item['name'] = name
            item['type_'] = type_
            item['house_area'] = house_area
            item['house_id'] = house_id
            item['lon'] = lon
            item['lat'] = lat
            item['release_time'] = release_time
            item['community_name'] = community_name
            item['district_name'] = district_name
            item['house_type'] = house_type
            item['rent_price'] = rent_price

            comm_id = get_re_result(r'comm_id: \'(\d+)\'', response.text, 1)
            block_id = get_re_result(r'block_id: \'(\d+)\'', response.text, 1)
            area_id = get_re_result(r'area_id: \'(\d+)\'', response.text, 1)
            num = get_re_result(r'num: \'(\d+)\'', response.text, 1)
            if comm_id:
                url = self.price_trend_url.format(
                    comm_id,
                    block_id,
                    area_id,
                    num
                )
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_price_trend,
                    meta={
                        'item': item,
                        'dont_redirect': True
                    },
                    dont_filter=True
                )
            else:
                self.logger.debug('{}缺失comm_id'.format(house_id))
                yield item
        else:
            self.logger.debug('数据缺失')
            yield response.request

    def parse_price_trend(self, response):
        json_data = loads(response.text)
        item = response.meta['item']
        community_price = None
        district_price = None
        if json_data['status'] == 'ok':
            item['origin_price_data'] = json_data['data']
            community_price = {}
            district_price = {}
            for key in json_data['data']:
                line1 = json_data['data'][key]['line1']
                line3 = json_data['data'][key]['line3']
                community_price[key] = line1
                district_price[key] = line3
        else:
            self.logger.debug('{}爬取价格走势信息失败'.format(item['house_id']))

        item['community_price'] = community_price
        item['district_price'] = district_price

        yield item
