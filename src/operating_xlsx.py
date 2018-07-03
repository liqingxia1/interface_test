import xlrd
import xlwt
from xlutils.copy import copy
import os


class OperatingXLSX:
    def __init__(self, file_path):
        self.file_path = file_path
        self.rsp_data = 8
        self.assret_result = 9
        self.result = 10


    def get_xlsx(self):
        """
        读取xlsx中的测试用例，去掉了title与最后三列的读取，若格式变动，脚本需要修改
        :return:  返回测试集合
        """

        # 打开 xls 文件
        data = xlrd.open_workbook(self.file_path )
        table = data.sheets()[0]  # 通过索引顺序获取

        nrows = table.nrows  # 获取该sheet中的有效行数
        ncols = table.ncols  # 获取列表的有效列数
        cases_id = 0         # 用例id
        test_set = {}        # 用例存放集合
        cases = []           # 用例临时存放数组

        # print(nrows,ncols)    # 输出有效的行与列

        # 读取行与列的内容，去掉title所以nrows-1并且i+1; 去掉了最后三列，所以ncols-3
        for i in range(nrows-1):
            i = i+1
            for j in range(ncols-3):
                cases.append(table.cell_value(i, j))             # 循环读取这一行的数据，并将数据存入临时存放数组中
            test_set[cases_id] = cases                           # 将临时数据存放到字典中，cases_id从1开始
            cases_id+=1
            cases = []                                           # 将临时存放数组中的数据清空
        return test_set                                         # 将用例的集合返回

    def wirt_xlsx(self, test_set, rsp_data, test_results):
        """
        :param test_set: 测试集合
        :param rsp_data: 请求url返回的数据
        :param test_results: test_results[result] pass/ fall 测试结果; test_results[assertion] 断言结果; test_results[casename] 用例名称
        :return:
        """

        old_excel = xlrd.open_workbook(self.file_path, formatting_info=True)
        new_excel = copy(old_excel)
        ws = new_excel.get_sheet(0)

        # 设置写入数据的字体格式
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = "宋体"
        font.height = 250
        style.font = font

        # 设置写入数据的边框格式
        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        style.borders = borders

        # 将数据写入到xlsx文件中
        for index in test_set:
            table_cell = index + 1
            print(test_results[index]['result'])
            ws.write(table_cell, self.rsp_data, rsp_data[index], style)
            ws.write(table_cell, self.result, test_results[index]['result'], style)
            ws.write(table_cell, self.assret_result, str(test_results[index]['assertion']), style)
        new_excel.save(self.file_path)


