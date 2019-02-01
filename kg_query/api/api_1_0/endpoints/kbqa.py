import logging
import os

from api.api_1_0.restplus import api
from flask_restplus import Resource
from api.api_1_0.module import jena_sparql_endpoint, question2sparql
from api.api_1_0.parsers import question_args
from api.api_1_0.serializers import answer
from flask import request

log = logging.getLogger(__name__)

ns = api.namespace("v_0_0_1", description="问答")


def get_absolute_path(relative_filename):
    """
    根据相对路径获取绝对路径
    :param relative_filename:
    :return:
    """
    os.path.normpath(os.path.join(os.path.dirname(__file__), relative_filename))


# 连接Fuseki服务器。
fuseki = jena_sparql_endpoint.JenaFuseki()
# 初始化自然语言到SPARQL查询的模块，参数是外部词典列表。
ab_path = os.getcwd()
q2s = question2sparql.Question2Sparql(["{}/external_dict/movie_title.txt".format(ab_path),
                                       "{}/external_dict/person_name.txt".format(ab_path)])


@ns.route("/answer")
class InvoiceCheck(Resource):
    @api.expect(question_args)
    @api.marshal_with(answer)
    def get(self):
        args = question_args.parse_args(request)
        question = args.get("question")
        my_query = q2s.get_sparql(question)
        if my_query is not None:
            result = fuseki.get_sparql_result(my_query)
            value = fuseki.get_sparql_result_value(result)

            # 判断结果是否是布尔值，是布尔值则提问类型是"ASK"，回答“是”或者“不知道”。
            if isinstance(value, bool):
                if value is True:
                    return {"status": 1, "answer": "Yes"}
                else:
                    return {"status": 1, "answer": "I don\'t know. :("}
            else:
                # 查询结果为空，根据OWA，回答“不知道”
                if len(value) == 0:
                    return {"status": 1, "answer": "I don\'t know. :("}
                elif len(value) == 1:
                    return {"status": 1, "answer": value[0]}
                else:
                    output = ''
                    for v in value:
                        output += v + u'、'
                    return {"status": 1, "answer": output[0:-1]}
        else:
            # 自然语言问题无法匹配到已有的正则模板上，回答“无法理解”
            return {"status": 1, "answer": "I don\'t know. :("}
