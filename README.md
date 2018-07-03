# interface_test
接口自动化测试（读取excel文档中的用例，进行接口自动化测试，自动填写结果并生成测试报告）



目录结构：
--file 
----Interface_test_cases.xlsx     用例编写模板
----test_report.html              执行后的html测试报告
--report_test
----html.py                       生成html测试报告；html页面显示模板
--src
----operating_xlsx.py             执行xlsx文档的读与写操作
----perform_test.py               执行接口请求的测试
----run.py                        主方法，执行run即执行测试


