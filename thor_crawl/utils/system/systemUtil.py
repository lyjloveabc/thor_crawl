"""
系统工具
"""
import os
import logging

from thor_crawl.utils.constant.constant import Constant
from thor_crawl.utils.constant.resultCode import ResultCode


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


if __name__ == '__main__':
    SystemUtil.batch_rename_file('/Users/luoyanjie/PycharmProjects/thor_crawl')
