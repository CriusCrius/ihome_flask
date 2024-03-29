


# 主帐号
accountSid = '8aaf07086a43ad03016a582c2ea31652'

# 主帐号Token
accountToken = '1548573782d6430aab9bca1053b4b4b2'

# 应用Id
appId = '8aaf07086a43ad03016a582c2ef91659'

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com'

# 请求端口
serverPort = '8883'

# REST版本号
softVersion = '2013-12-26'


# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为列表 例如：['12','34']，如不需替换请填 ''
# @param $tempId 模板Id


class CCP(object):
    """自己封装的发送短信的辅助类"""
    # 用来保存对象的类属性
    instance = None

    def __new__(cls):
        # 判断CCP类有没有已经创建好的对象，如果没有，创建一个对象，并且保存
        # 如果有，则将保存的对象直接返回
        if cls.instance is None:
            obj = super(CCP, cls).__new__(cls)

            # 初始化REST SDK
            from ihome.libs.yuntongxun.CCPRestSDK import REST
            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)

            cls.instance = obj

        return cls.instance

    def send_template_sms(self, to, datas, temp_id):

        result = self.rest.sendTemplateSMS(to, datas, temp_id)
        status_code = result.get("statusCode")
        if status_code == "000000":
            # 表示发送短信成功
            print("++++++发送短信成功+++++++")
            return 0
        else:
            # 发送失败
            return -1
