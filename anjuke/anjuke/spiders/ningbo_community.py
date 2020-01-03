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
    first_url = None

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
        if json_data['status'] != 'ok':
            self.logger.debug('爬取第{}页失败'.format(response.meta.get('page', 1)))
            return

        data = json_data['data']
        page = response.meta.get('page', 1)

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

        if self.first_url is None:
            self.first_url = data[0]['url']
        if self.first_url != data[0]['url'] or page == 1:
            page += 1
            link = response.meta['link']
            url = '%s?p=%d' % (link, page)
            yield scrapy.Request(
                url=url,
                dont_filter=True,
                meta={'page': page, 'link': link, 'block_name': response.meta['block_name']}
            )

    def parse_detail(self, response):
        """
        解析详细页面的函数
        """
        # 正则表达式匹配到的坐标
        lat_lon_pattern = r'lng=(.*?)&lat=(.*?)&'
        lat_lon = re.search(lat_lon_pattern, response.text)
        item = response.meta['item']

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
            url='https://m.anjuke.com/ajax/new/trendency/price/all?comm_id=%s' % item['comm_id'],
            headers={
                ':authority': 'm.anjuke.com',
                ':method': 'GET',
                ':path': '/ajax/new/trendency/price/all?comm_id=%s' % item['comm_id'],
                ':scheme': 'https',
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
