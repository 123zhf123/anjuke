import re
from json import loads

import scrapy

from anjuke.custom_settings import ningbo_community
from anjuke.items import Anjuke_xq_sale


class NingboCommunity(scrapy.Spider):
    name = 'ningbo_community'

    tag = 'ningbo'
    city = '宁波'
    start_urls = [
        'https://m.anjuke.com/nb/community/o2/'
    ]
    custom_settings = ningbo_community

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                headers={
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'zh-CN,zh;q=0.9',
                    'cache-control': 'no-cache',
                    'cookie': 'sessid=B6305D5E-A8B0-E771-D19F-0BE4E3188E06; aQQ_ajkguid=126FAD93-73B6-90BF-EB8A-F1F4A68B5D60; lps=http%3A%2F%2Fnb.anjuke.com%2F%7C; twe=2; ANJUKE_BUCKET=pc-home%3AErshou_Web_Home_Home-a; _ga=GA1.2.2119016282.1577793913; 58tj_uuid=153d294f-082f-4bd7-b780-34f08b1ee29b; als=0; wmda_uuid=a4254b140cdcef09613f3c0e3ca384c6; wmda_new_uuid=1; wmda_visited_projects=%3B6145577459763; ctid=32; app_cv=unknown; ajk_member_verify=2Av8tX2ayJE228YodNFH92NgiqO7fuYsEl9x0w0kWTY%3D; ajk_member_verify2=MTgwNjc2MTc0fDBpSjQ2Snl8MQ%3D%3D; ajkAuthTicket=TT=52d8a5a74d7158eb19ad7d33d1e5ffc9&TS=1577850043276&PBODY=j9h7f7sYIC1dGiG9zQl8q8gm2CBLw89Sy1WiKiLk5Qni7swqd6aXnw6FjGZhPgjuYw8eiUOCo9o2H6QQxUSzhv0LAv5JfY1CeYBJZd7cnYfAz1qoz1ePXZD_n5062wp-4vxwaAx_bF6_-dY9x7EsmzRNt4o2GaE0jBBEFGpR0_s&VER=2; ctid=32; ajk_member_id=180676174; wmda_uuid=c694c99e2c754b7024780e7671b89ae3; wmda_new_uuid=1; wmda_visited_projects=%3B6289197098934; ajk_view_visit={%22timeStamp%22:%222020/1/2%22%2C%22rent_view%22:1}; _gid=GA1.2.1832719355.1577960385; aQQ_brokerguid=79030027-6355-CD10-1A93-248199C10344; xzfzqtoken=Ti0YRYuzdoOAN39lJXfzYdaDG0ehbSdt79kvO6e7wZYiHzrrK%2BLGsaQGVitLONslin35brBb%2F%2FeSODvMgkQULA%3D%3D; new_uv=13; ajkAuthTicket=TT=52d8a5a74d7158eb19ad7d33d1e5ffc9&TS=1578023291513&PBODY=LLPjPaMq9FbWNfABM2c30DKNzAOjsv-p7NNYYE7K4XgwrAhs0I-3OMe8vf3IbKEpnOdcBdZbX4tvl8VkqeNXwFTZ8Zvq8FXTbqVy6yuusXFQ3jLu5Rm1pIIOQQQ8dLW-7RZv3pqo1ubtyvf4JuUdxNg8tKUyhqt5CwFv4OC9hZc&VER=2',
                    'pragma': 'no-cache',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'none',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
                },
                dont_filter=True
            )

    def parse(self, response):
        for block_id in ['blockinfo-0', 'blockinfo-1', 'blockinfo-4']:
            urls = response.xpath('//div[@id="{}"]/div/a'.format(block_id))
            for url in urls[1:]:
                block_name = url.xpath('./@data-id').get()
                url = url.xpath('./@href').get()
                yield scrapy.Request(
                    url=url,
                    callback=self.parse2,
                    meta={'block_name': block_name, 'link': url},
                    dont_filter=True
                )

    def parse2(self, response):
        json_data = loads(response.text)
        if json_data['code'] != 0:
            self.logger.debug('爬取第{}页失败: {}'.format(response.meta.get('page', 1), json_data['msg']))
            return

        data = json_data['data']
        page = response.meta.get('page', 1)
        self.logger.debug('正在爬取{}的第{}页({})'.format(response.meta['block_name'], page, response.meta['link']))

        for community in data:
            item = Anjuke_xq_sale()
            item['tag'] = self.tag
            item['city'] = self.city
            item['block_name'] = response.meta['block_name']
            item['community_name'] = community['name']
            item['district_name'] = community['area']
            item['addr'] = community['address']
            item['build_time'] = community['build_year']
            item['price'] = community['mid_price']
            item['url'] = community['url']
            item['page'] = page
            yield scrapy.Request(
                url=item['url'],
                callback=self.parse_detail,
                meta={'item': item},
                dont_filter=True
            )

        first_url = response.meta.get('first_url')
        if first_url is None:
            first_url = data[0]['url']
        if len(data) == 0:
            self.logger.debug('空数据({}):\n{}'.format(response.url, json_data))
            return
        if first_url != data[0]['url'] or page == 1:
            page += 1
            link = response.meta['link']
            url = '%s?p=%d' % (link, page)
            yield scrapy.Request(
                url=url,
                dont_filter=True,
                meta={'page': page, 'link': link, 'block_name': response.meta['block_name'], 'first_url': first_url},
                callback=self.parse2
            )

    def parse_detail(self, response):
        """
        解析详细页面的函数
        """
        # 正则表达式匹配到的坐标
        lat_lon_pattern = r'lng=(.*?)&lat=(.*?)&'
        lat_lon = re.search(lat_lon_pattern, response.text)
        item = response.meta['item']

        community_id = re.search(r'&comm_id=(\d+)', response.text)

        # # 请求异常时请自定更新headers中的cookie
        if lat_lon is None:
            self.logger.debug('获取数据失败(%s)' % item['url'])
            yield item
            return

        def get_xpath_string(xpath):
            data = response.xpath(xpath).xpath('string(.)').get()
            if data:
                return data.strip()

        developer = re.search(r'商：</dt>.*?<dd>(.*?)</dd>', response.text, re.S)
        if developer:
            developer = developer.group(1)
        shangquan = re.search(r'<i class="label">所属商圈：</i>\s*(.*?)\s*</span>', response.text, re.S)
        if shangquan:
            shangquan = shangquan.group(1)
        item['shangquan'] = shangquan
        item['developer'] = developer
        item['lon'] = lat_lon.group(1)
        item['lat'] = lat_lon.group(2)
        item['type_'] = get_xpath_string('//div[@class="header-field"]/span')

        yield scrapy.Request(
            url='https://m.anjuke.com/ajax/new/trendency/price/all?comm_id=%s' % community_id,
            headers={
                'accept': 'application/json',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',

                # 请求异常时请自定更新这里headers中的cookie
                'cookie': 'aQQ_ajkguid=B06CB69D-B739-65DA-970C-41BCFF45582C; ctid=81; lps="/jing/community/o2/?p={}|"; sessid=18F25292-AE1C-CA85-06D4-5BF0F8263BDB; wmda_uuid=84bf2aa03eafa86c1d0deead6ff14cee; wmda_session_id_6145577459763=1577324502373-989e0464-f995-b55b; wmda_visited_projects=%3B6145577459763; 58tj_uuid=1def9e55-e491-4aa1-8ac4-2b4e94cffbfe; init_refer=; new_uv=1; new_session=0; xzfzqtoken=EDydIvUR4Q9NVbVoaPJRb8PNRPY92612TUn09XuUrRP%2Fk5el1Wo1uQx1tysV%2Foqein35brBb%2F%2FeSODvMgkQULA%3D%3D'.format(
                    item['page']),
                'referer': item['url'],
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
            },
            callback=self.parse_price,
            meta={'item': item}
        )

    def parse_price(self, response):
        """
        解析价格走势API的函数
        """
        json_data = loads(response.text)
        item = response.meta['item']

        if json_data['status'] != 'ok':
            self.logger.debug('获取数据失败(%s)' % item['url'])
            yield item
            return

        item['price_3year'] = json_data['data']
        yield item
