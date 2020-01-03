import requests

from anjuke.settings import DEFAULT_REQUEST_HEADERS


def main():
    session = requests.session()
    # session.headers.update(DEFAULT_REQUEST_HEADERS)
    headers = {
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'cookie': 'sessid=B6305D5E-A8B0-E771-D19F-0BE4E3188E06; aQQ_ajkguid=126FAD93-73B6-90BF-EB8A-F1F4A68B5D60; lps=http%3A%2F%2Fnb.anjuke.com%2F%7C; twe=2; ANJUKE_BUCKET=pc-home%3AErshou_Web_Home_Home-a; _ga=GA1.2.2119016282.1577793913; _gid=GA1.2.1817212992.1577793913; 58tj_uuid=153d294f-082f-4bd7-b780-34f08b1ee29b; als=0; wmda_uuid=a4254b140cdcef09613f3c0e3ca384c6; wmda_new_uuid=1; wmda_visited_projects=%3B6145577459763; ctid=32; app_cv=unknown; ajk_member_verify=2Av8tX2ayJE228YodNFH92NgiqO7fuYsEl9x0w0kWTY%3D; ajk_member_verify2=MTgwNjc2MTc0fDBpSjQ2Snl8MQ%3D%3D; ajkAuthTicket=TT=52d8a5a74d7158eb19ad7d33d1e5ffc9&TS=1577850043276&PBODY=j9h7f7sYIC1dGiG9zQl8q8gm2CBLw89Sy1WiKiLk5Qni7swqd6aXnw6FjGZhPgjuYw8eiUOCo9o2H6QQxUSzhv0LAv5JfY1CeYBJZd7cnYfAz1qoz1ePXZD_n5062wp-4vxwaAx_bF6_-dY9x7EsmzRNt4o2GaE0jBBEFGpR0_s&VER=2; ctid=32; ajk_member_id=180676174; ajk_view_visit={%22timeStamp%22:%222020/1/1%22%2C%22rent_view%22:5}; init_refer=; new_uv=4; new_session=0; ajkAuthTicket=TT=52d8a5a74d7158eb19ad7d33d1e5ffc9&TS=1577871339984&PBODY=LNiV85O0rz8gLDPnrUZCFQrqMYtJCL6vlqHOHW6hEn1_3XDMRG4xXyLH_wd-bxf4f-oMH20ZPmKOJYimkLj3jKiVXalPAOIJwCr3q7GiqKMIN55a4kjTH_C56RLUrDeziC6vjoIrcpaxjGGXhgklRdI-ZKxSn2GUnHbDuxVm0Gg&VER=2; wmda_session_id_6145577459763=1577871342008-0d4386de-3e8e-c9e0; xzfzqtoken=%2BkPtMSra8OjtBCGrltVL%2F9id1BCIwR8OKRZPUdVThHVllYwulDoCpoDyfe5FAQSyin35brBb%2F%2FeSODvMgkQULA%3D%3D',
        'pragma': 'no-cache',
        'referer': 'https://m.anjuke.com/nb/community/?from=anjuke_home',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    url = 'https://m.anjuke.com/nb/community/o2/?from=anjuke_home&p=53'

    response = session.get(url=url, headers=headers).json()
    print(response)


def parse():
    import re
    from parsel import Selector
    with open('test/1.html', 'r', encoding='utf-8') as f:
        text = f.read()
    result = re.search(r'<i class="label">所属商圈：</i>\s*(.*?)\s*</span>', text, re.S)
    if result:
        print(result.group(1))


if __name__ == '__main__':
    parse()
