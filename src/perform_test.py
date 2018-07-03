import requests

class PerformTest():

    def __init__(self):
        self.case_name_column = 2
        self.url_column = 3
        self.req_way_column = 4
        self.cont_type_column = 5
        self.data_column = 6
        self.exp_result_column = 7

    def request_post_get(self, case, request_way):
        '''
        判断当前的请求是get还是post
        :param case: 请求的case集合
        :param request_way: 请求的方式
        '''
        data = case[self.data_column]
        data = data.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ','')
        if request_way == 'get':
            return PerformTest().get_methods(case, data)
        elif request_way == 'post':
            return PerformTest().post_methods(case, data)
        else:
            print("不支持的请求格式")

    def post_methods(self, case , data):
        """取url、Content-Type、data后发送post请求，并将预期结果与返回结果传到assert_rsp中"""
        post_url = case[self.url_column]
        headers = {"Content-Type": case[self.cont_type_column]}
        r = requests.post(post_url, data=data, headers=headers)
        results = PerformTest().assert_rsp(case[self.exp_result_column], r , case[self.case_name_column])
        return results

    def get_methods(self, case , params):
        """取url与params后发送get请求，并将结果预期结果与返回结果传到assert_rsp中"""
        post_url = case[self.url_column]
        r = requests.get(post_url,params)
        results = PerformTest().assert_rsp(case[self.exp_result_column], r ,case[self.case_name_column])
        return results


    def assert_rsp(self,expectation  ,rsp ,case_name):
        """
         获取预期结果与返回的结果，进行断言，判断是否测试通过
        :param expectation: 期望结果列表
        :param rsp: 返回的data数据
        :return:
            test_results: test_results[result] pass/ fall 测试结果； test_results[assertion] 断言结果; test_results[casename] 用例名称
            rsp.text: 请求url返回的data数据
        """
        assertion_results = {}
        test_results = {}
        test_results['result'] = 'pass'
        test_results['casename'] = case_name
        expectation.replace(' ', '')
        """判断页面请求是否成功，返回200;若成功，则将cede赋值为200，且进行期望结果与返回结果的断言"""
        if rsp.status_code == 200:
            assertion_results['code'] = 200
            """
            因json格式的数据无法用in判断，固判断rsp中的header类型是否为json类型，若为json类型，则转换为json数据，以key做断言
            每次将断言的值与key以字典的形式存入到assertion_results；test_results[assertion]中存放所有的断言结果；assertion[result]中存放测试结果
            若断言失败则将test_results['result']的值（测试结果）改为fall；但不会退出，依旧会继续断言后面的数据
            """
            if 'application/json' in rsp.headers['Content-Type']:
                responses = rsp.json()
                expectation = eval(expectation)
                for key in expectation:
                    if responses[key] == expectation[key]:
                        assertion_results[key] = responses[key]
                    else:
                        assertion_results[key] = 'fall'
                        test_results['result'] = 'fall'
            elif 'text/html' in rsp.headers['Content-Type']:
                expectations = expectation.split()
                for i in expectations:
                    if i in rsp.text:
                        assertion_results[i] = 'pass'
                    else:
                        assertion_results[i] = 'fall'
                        test_results['result'] = 'fall'
            else:
                print("responses返回的类型暂不支持分析")
        else :
            assertion_results['code'] = "fall"
            test_results['result'] = 'fall'
        test_results['assertion'] = assertion_results
        return test_results, rsp.text




