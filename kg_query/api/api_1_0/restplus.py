import logging

from flask_restplus import Api
import config

log = logging.getLogger(__name__)

api = Api(version="1.0", title="Big Quantum API", description="基于知识图谱的问答系统")


@api.errorhandler
def default_error_handler(e):
    log.exception(e)
    if not config.FLASK_DEBUG:
        return {"status": 0, "message": "系统异常，请联系管理员"}, 500
    else:
        pass
