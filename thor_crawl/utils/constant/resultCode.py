"""
错误码
"""


class BaseResultCode:
    """ 基础错误码类 """

    def __init__(self, code='111111', msg='success', *args, **kwargs):
        self.code = code
        self.msg = msg


class ResultCode:
    """ 错误码枚举 """
    # 通用成功、失败
    SUCCESS = BaseResultCode()
    DEFAULT_ERROR = BaseResultCode('000000', 'failure')

    # 业务
    CONDITION_NOT_CONFORM = BaseResultCode('000001', '条件不匹配')
