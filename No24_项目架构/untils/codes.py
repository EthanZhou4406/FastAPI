from enum import Enum

class RespCode(Enum):
    """
    系统回复状态码
    """
     # 系统级别
    OK = ("000000", "交易成功！")
    SYSTEM_ERROR = ("999999", "System Error")

    # 系统请求交互
    SESSION_FAILURE = ("100000", "会话失效！")
    SQL_INJECTION = ("110000", "参数不合法，有SQL注入风险！")
    REQ_SYS_EMPTY = ("100001", "请求失败，reqSys 不能为空！")
    REQ_SYS_NOT_EXIST = ("100002", "请求失败，reqSys 不存在！")
    SERVICE_ID_EMPTY = ("100003", "请求失败，serviceId 不能为空！")
    SERVICE_ID_NOT_EXIST = ("100004", "请求失败，serviceId 不存在！")
    REQ_DATA_EMPTY = ("100005", "请求失败，reqData 不能为空")
    REQ_DATA_PARAM_ERROR = ("100006", "请求失败，reqData 中存在参数错误！")
    REQ_FILE_TYPE_ERROR = ("100007", "请求失败,上传文件类型有误！")
    REQ_FILE_SIZE_ERROR = ("100008", "请求失败,上传文件太大！")
    REQ_DATA_NOT_EMPTY = ("100009", "请求失败，数据库存在相同数据！")

    # 用户登录级别
    USER_PARAM_NOT_EXIST = ("200001", "登录失败，用户名和密码不能为空！")
    USER_NOT_EXIST = ("200002", "登录失败，用户不存在！")
    USER_PWD_ERROR = ("200003", "登录失败，用户名或密码错误！")
    WXID_DIFF = ("200004", "登陆校验成功，但与上次登录的微信号不一致！")
    LOGIN_FAIL_COUNT_LIMIT = ("200005", "登陆失败，当日登录失败次数达到上限！")
    USER_NOT_OPEND = ("200006", "账号未开通！")
    # 用户权限级别
    USER_NO_PERMISSION = ("210001", "用户无权限！")
    USER_STATUS_ERROR = ("210002", "用户状态异常！")
    USER_IS_EXIST = ("210003", "新增用户信息失败，用户名已存在！")

    # 新增数据
    NO_DATA__FOUND = ("400001", "插入数据成功，查无记录！")
    DUPLICATED_DATA = ("400002","数据已存在，请勿重复记录")
    INVALID_DATA =("400003","录入数据不规范")

    # 可靠性分配任务
    WORK_VERSION_IS_USED = ("500001", "存在相同序号和版本的任务")

    # 图片验证码
    CODE_EMPTY = ("600001","验证码为空")
    CODE_ERROR = ("600002","验证码不正确")

    # 邮件发送失败
    EMAIL_ERROR = ("700001","邮件发送失败，请联系管理员")
    @property
    def code(self):
        """获取状态码"""
        return self.value[0]

    @property
    def msg(self):
        """获取状态码信息"""
        return self.value[1]

