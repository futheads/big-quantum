from flask_restplus import reqparse

name = reqparse.RequestParser()

question_args = reqparse.RequestParser()
question_args.add_argument("question", type=str, required=True, help="问题")
