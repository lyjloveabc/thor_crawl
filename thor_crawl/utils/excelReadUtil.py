# encoding=utf-8
"""
文件或文件内容操作
"""
import logging
import xlrd

logging.basicConfig()
logger = logging.getLogger(__name__)


class ExcelReadUtil(object):
    __FIRST_SHEET_INDEX = 0

    def __init__(self):
        logger.info(self.__str__() + ' init')

    def __del__(self):
        logger.info(self.__str__() + ' del')

    @staticmethod
    def read_file(file_name, field_index_dict, first_row_flag=False):
        result_list = list()
        data = xlrd.open_workbook(file_name)

        for sheet in data.sheets():
            rows = sheet.nrows
            if first_row_flag:
                ran = range(rows)
            else:
                ran = range(1, rows) if sheet == data.sheets()[ExcelReadUtil.__FIRST_SHEET_INDEX] else range(rows)

            for i in ran:
                try:
                    row_data = dict()
                    for k, v in field_index_dict.items():
                        row_data[k] = sheet.row_values(i)[v]

                    result_list.append(row_data)
                except ValueError as e:
                    print(e)
        logger.info(file_name, '::', len(result_list))
        return result_list

    @staticmethod
    def read_file_return_map(file_name, field_index_dict, key, first_row_flag=False):
        result_dict = dict()
        data = xlrd.open_workbook(file_name)

        for sheet in data.sheets():
            rows = sheet.nrows
            if not first_row_flag:
                ran = range(1, rows) if sheet == data.sheets()[ExcelReadUtil.__FIRST_SHEET_INDEX] else range(rows)
            else:
                ran = range(rows)

            for i in ran:
                try:
                    row_data = dict()
                    for k, v in field_index_dict.iteritems():
                        row_data[k] = sheet.row_values(i)[v]

                    result_dict[row_data[key]] = row_data
                except ValueError as e:
                    print(e)
        logger.info(file_name, '::', len(result_dict))
        return result_dict

    @staticmethod
    def read_file_return_id_val(file_name, field_index_dict, key, val, first_row_flag=False):
        result_dict = dict()
        data = xlrd.open_workbook(file_name)

        for sheet in data.sheets():
            rows = sheet.nrows
            if not first_row_flag:
                ran = range(1, rows) if sheet == data.sheets()[ExcelReadUtil.__FIRST_SHEET_INDEX] else range(rows)
            else:
                ran = range(rows)

            for i in ran:
                try:
                    row_data = dict()
                    for k, v in field_index_dict.iteritems():
                        row_data[k] = sheet.row_values(i)[v]

                    result_dict[str(int(row_data[key]))] = row_data[val]
                except ValueError as e:
                    print(e)
        logger.info(file_name, '::', len(result_dict))
        return result_dict

    @staticmethod
    def to_export_txt(data, columns, file_result):
        split_str = str('#=#')
        row_index = 1

        with open(file_result, 'a') as f:
            for temp in data:
                line_str = str(row_index) + split_str
                for i in range(len(columns)):
                    val = temp[columns[i]]
                    if type(val) == float:
                        val = str(int(val))
                    line_str += val + split_str
                f.write((line_str[:-len(split_str)] + '\n').encode('utf-8'))
                row_index += 1


if __name__ == '__main__':
    pass
