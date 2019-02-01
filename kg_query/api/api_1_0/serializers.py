from flask_restplus import fields
from api.api_1_0.restplus import api

common = api.model("结果状态", {
    "status": fields.Integer(required=True, description="请求状态，1：成功，0：失败")
})

answer = api.inherit("问题答案", common, {
    "answer": fields.String(required=True)
})
