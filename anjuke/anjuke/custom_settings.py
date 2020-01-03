ningbo_community = {
    'DEFAULT_REQUEST_HEADERS': {
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'cookie': 'sessid=B6305D5E-A8B0-E771-D19F-0BE4E3188E06; aQQ_ajkguid=126FAD93-73B6-90BF-EB8A-F1F4A68B5D60; lps=http%3A%2F%2Fnb.anjuke.com%2F%7C; twe=2; ANJUKE_BUCKET=pc-home%3AErshou_Web_Home_Home-a; _ga=GA1.2.2119016282.1577793913; 58tj_uuid=153d294f-082f-4bd7-b780-34f08b1ee29b; als=0; wmda_uuid=a4254b140cdcef09613f3c0e3ca384c6; wmda_new_uuid=1; wmda_visited_projects=%3B6145577459763; ctid=32; app_cv=unknown; ajk_member_verify=2Av8tX2ayJE228YodNFH92NgiqO7fuYsEl9x0w0kWTY%3D; ajk_member_verify2=MTgwNjc2MTc0fDBpSjQ2Snl8MQ%3D%3D; ajkAuthTicket=TT=52d8a5a74d7158eb19ad7d33d1e5ffc9&TS=1577850043276&PBODY=j9h7f7sYIC1dGiG9zQl8q8gm2CBLw89Sy1WiKiLk5Qni7swqd6aXnw6FjGZhPgjuYw8eiUOCo9o2H6QQxUSzhv0LAv5JfY1CeYBJZd7cnYfAz1qoz1ePXZD_n5062wp-4vxwaAx_bF6_-dY9x7EsmzRNt4o2GaE0jBBEFGpR0_s&VER=2; ctid=32; ajk_member_id=180676174; wmda_uuid=c694c99e2c754b7024780e7671b89ae3; wmda_new_uuid=1; wmda_visited_projects=%3B6289197098934; ajk_view_visit={%22timeStamp%22:%222020/1/2%22%2C%22rent_view%22:1}; _gid=GA1.2.1832719355.1577960385; aQQ_brokerguid=79030027-6355-CD10-1A93-248199C10344; wmda_session_id_6145577459763=1578014508905-b5bb6680-5dfe-f184; init_refer=https%253A%252F%252Fm.anjuke.com%252Fnb%252Fcommunity%252Fyinzhou%252F; new_uv=11; new_session=0; ajkAuthTicket=TT=52d8a5a74d7158eb19ad7d33d1e5ffc9&TS=1578015723785&PBODY=BiL8EOYT4aIQJftCruxQgksVHeBwb-vt7A7IjFYKj7ZjzlyRjgadUe79cPkYonYSlKXWZlS-G7DMLtMS658BuRzZIs2uJg_PeFZN41DzTAir_iQK2aOQjrETCa3QmPpLcer58OzyPGPTatTp3T6UDg1uNGJDBVjrE-BrIVqYrY0&VER=2; xzfzqtoken=8GDCIu5MHY5VsBw8b2gwHet3WgLfzy24%2F43Z6u0SmE4TKSkFo%2FprHBQEqi3ZC8oyin35brBb%2F%2FeSODvMgkQULA%3D%3D',
        'pragma': 'no-cache',
        'referer': 'https://m.anjuke.com/nb/community/?from=anjuke_home',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    },
    'DOWNLOAD_DELAY': 0.5,
    'HTTPERROR_ALLOWED_CODES': [302],
    # 'SCHEDULER': "scrapy_redis.scheduler.Scheduler",
    # 'DUPEFILTER_CLASS': "scrapy_redis.dupefilter.RFPDupeFilter",
    # 'REDIS_PARAMS': {
    #     'password': '1291988293'
    # }
}

ningbo_fangyuan = {
    'SCHEDULER': "scrapy_redis.scheduler.Scheduler",
    'DUPEFILTER_CLASS': "scrapy_redis.dupefilter.RFPDupeFilter",
    'REDIS_PARAMS': {
        'password': '1291988293'
    },
    'DOWNLOADER_MIDDLEWARES': {
        'anjuke.middlewares.ProxyMiddleware': 300
    },
    'HTTPERROR_ALLOWED_CODES': [302],
    'CONCURRENT_REQUESTS': 8,
    'DOWNLOAD_DELAY': 1
}
