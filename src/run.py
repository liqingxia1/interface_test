from src.operating_xlsx import OperatingXLSX
from src.perform_test import PerformTest
from report_test.html import get_report
import os


REQ_WAY_COLUMN = 4
FILE_PATH = os.path.abspath(os.path.dirname(os.getcwd()))
ELSX_PATH = FILE_PATH + "/file/Interface_test_cases.xlsx"
TEST_REPORT_PATH = FILE_PATH + "/file/test_report.html"



if __name__ == '__main__':
    op_xlsx = OperatingXLSX(ELSX_PATH)
    test_set = op_xlsx.get_xlsx()
    test_results = []
    rsps = []
    for i in test_set:
        test_result,rsp = PerformTest().request_post_get(test_set[i], test_set[i][REQ_WAY_COLUMN])
        test_results.append(test_result)
        rsps.append(rsp)



    op_xlsx.wirt_xlsx(test_set=test_set,rsp_data=rsps,test_results=test_results)
    get_report(test_results, TEST_REPORT_PATH)