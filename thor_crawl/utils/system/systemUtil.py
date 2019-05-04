"""
系统工具
"""
import os
import logging

import time

from thor_crawl.utils.constant.constant import Constant
from thor_crawl.utils.constant.resultCode import ResultCode
from thor_crawl.utils.email.emailUtil import EmailUtils


class SystemUtil:
    def __init__(self):
        pass

    @staticmethod
    def batch_rename_file(path=os.getcwd(), extension=None, go_deep=True):
        """
        批量修改文件名
        extension: 扩展名列表，只要在这个列表里面的才会被修改文件名
        go_deep: 是否深入下一级目录修改文件名
        """
        # 获取指定目录下的所有文件和目录名
        file_name_group = os.listdir(path)

        for file_name in file_name_group:
            # 连接目录与文件名或目录
            old_full_file_name = os.path.join(path, file_name)

            if extension is None or Constant.DOT not in old_full_file_name or old_full_file_name.split(Constant.DOT)[1] in extension:
                is_file = os.path.isfile(old_full_file_name)
                is_dir = os.path.isdir(old_full_file_name)

                if is_file:
                    base_name = os.path.basename(old_full_file_name)
                    new_full_file_name = os.path.join(os.path.dirname(old_full_file_name), base_name[0].lower() + base_name[1:])
                    os.rename(old_full_file_name, new_full_file_name)
                elif is_dir and go_deep:
                    SystemUtil.batch_rename_file(path=old_full_file_name)
                else:
                    logging.error(ResultCode.CONDITION_NOT_CONFORM)

    @staticmethod
    def dict_value_handle(dict_data):
        """
        把dict里面的None值数据转化为空字符串，双引号转化为单引号，[]转化为空字符串
        :param dict_data: 原始数据
        :return: 转化后的数据
        """
        for key, value in dict_data.items():
            value_str = str(dict_data[key])

            if dict_data[key] is None:
                dict_data[key] = Constant.STR_EMPTY
            if '\'' in value_str:
                dict_data[key] = value_str.replace('\'', '"')
            if '[]' in value_str:
                dict_data[key] = value_str.replace('\'', '"')
        return dict_data

    @staticmethod
    def say(content="主人救命啊！", circle_num=1):
        for n in range(0, circle_num):
            if n > 0:
                time.sleep(10)
            os.system('say ' + content + '')


if __name__ == '__main__':
    # SystemUtil.batch_rename_file('/Users/luoyanjie/PycharmProjects/thor_crawl')
    # SystemUtil.say()
    EmailUtils.send_mail("he", "1111")
