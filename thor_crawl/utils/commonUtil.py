"""
通用、未分类，工具
"""


class CommonUtil:
    @staticmethod
    def get_extract(xpath_site, is_only=True):
        """ 当取出的长度大于0, 取出其值. isOnly True; 只取第一个. False:取所有. """
        extract_group = xpath_site.extract()
        if len(extract_group) > 0:
            if is_only:
                return extract_group[0].strip()
            else:
                return extract_group
        return ''
