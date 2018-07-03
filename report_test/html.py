#coding:utf-8
"""
- 使用bottle来动态生成html
    - https://www.reddit.com/r/learnpython/comments/2sfeg0/using_template_engine_with_python_for_generating/

"""
import datetime

_author_ = "LiaoPan"
_time_  = "2016.6.17"

from bottle import template
import webbrowser
"""
template_demo 我们需要展示的html内容;定义想要生成的Html的基本格式
使用%来插入python代码;{{}}插入变量
"""

template_demo="""
       <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>自动化测试报告</title>
            <link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
            <h1 style="font-family: Microsoft YaHei">自动化测试报告</h1>
            <p class='attribute'><strong>测试用例 : </strong>{{cases}}条</p>
            <p class='attribute'><strong>执行通过 : </strong>{{passing_rate}}条</p>
            <p class='attribute'><strong>执行失败 : </strong>{{fall_rate}}条</p>
            <p class='attribute'><strong>通过率 : </strong>{{success_rate}}%</p>
            <p class='attribute'><strong>测试结果 : </strong>{{test_result}}</p>
            <p class='attribute'><strong>测试时间 : </strong>{{nowTime}}</p>
            <style type="text/css" media="screen">
        body  { font-family: Microsoft YaHei,Tahoma,arial,helvetica,sans-serif;padding: 20px;}
        </style>
        </head>
        <body>
            <table id='result_table' class="table table-condensed table-bordered table-hover">
                <colgroup>
                    <col align='left' />
                    <col align='right' />
                    <col align='right' />
                    <col align='right' />
                </colgroup>
                <tr id='header_row' class="text-center success" style="font-weight: bold;font-size: 14px;">
                    <th>测试编号</th>
                    <th>用例名称</th>
                    <th>断言结果</th>
                    <th>执行结果</th>
                </tr>
                % for id,casename,assreq_result,run_result in items:
                <tr class='failClass warning'>
                    <td>{{ id }}</td>
                    <td>{{ casename }}</td>
                    <td>{{ assreq_result }}</td>
                    <td>{{ run_result }}</td>
                </tr>
                % end 
            </table>
        </body>
        </html>
"""

def get_report(test_results, filepath):
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
    articles = []
    j = 0
    case_numbers =  len(test_results)
    passing_rate = 0
    fall_rate = 0
    for i in test_results:
        if i['result'] == 'fall':
            fall_rate += 1
        else :
            passing_rate += 1
        print(i)
        article = (j, i['casename'], str(i['assertion']), str(i['result']))
        j+=1
        articles.append(article)

    success_rate = int(passing_rate/case_numbers * 100)
    if success_rate > 90:
        test_result = 'pass'
    else :
        test_result = 'fall'
    html = template(template_demo, items=articles, nowTime=nowTime, success_rate=success_rate, test_result=test_result, fall_rate=fall_rate, passing_rate=passing_rate, cases = case_numbers)

    with open(filepath, 'wb') as f:
        f.write(html.encode('utf-8'))

    # 使用浏览器打开html
    webbrowser.open(filepath)

