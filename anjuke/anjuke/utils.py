import re
import base64
import html
from io import BytesIO

from fontTools.ttLib import TTFont


class ParseFont(object):
    def __init__(self, base64_str):
        self.font = TTFont(BytesIO(base64.decodebytes(base64_str.encode())))
        self.c = self.font['cmap'].tables[0].ttFont.tables['cmap'].tables[0].cmap

    def get_page_font(self, source):
        if source is None:
            return
        source = html.unescape(source)
        ret_list = []
        for char in source:
            decode_num = ord(char)
            if decode_num in self.c:
                num = self.c[decode_num]
                num = int(num[-2:]) - 1
                ret_list.append(num)
            else:
                ret_list.append(char)
        ret_str_show = ''.join(map(str, ret_list))
        return ret_str_show


def get_re_result(pattern, source, index=1, *args):
    result = re.search(pattern, source, *args)
    if result:
        return result.group(index).strip()
