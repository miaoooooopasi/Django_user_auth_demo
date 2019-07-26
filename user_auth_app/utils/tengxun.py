from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError


class TengXun(object):
    def __init__(self, appkey):
        self.appkey = appkey

    def send_sms(self, code, mobile):
        # 短信应用SDK AppID
        appid = 1400235576
        # SDK AppID是1400开头

        # 短信应用SDK AppKey
        appkey = self.appkey

        # 需要发送短信的手机号码
        phone_numbers = "{mobile}".format(mobile=mobile)

        # 短信模板ID，需要在短信应用中申请
        template_id = 382462
        # NOTE: 这里的模板ID`7839`只是一个示例，真实的模板ID需要在短信控制台中申请

        # 签名
        sms_sign = "cms"  # NOTE: 这里的签名"腾讯云"只是一个示例，真实的签名需要在短信控制台中申请，另外签名参数使用的是`签名内容`，而不是`签名ID`

        ssender = SmsSingleSender(appid, appkey)
        params = ["{code}".format(code=code), "3"]  # 当模板没有参数时，`params = []`
        try:
            result = ssender.send_with_param(86, phone_numbers, template_id, params, sign=sms_sign, extend="",
                                             ext="")  # 签名参数未提供或者为空时，会使用默认签名发送短信
        except HTTPError as e:
            print(e)
        except Exception as e:
            print(e)

        print('result', result)
        return result


# 脚本自测
if __name__ == "__main__":
    teng_xun = TengXun("eb61539f093f6126d2079c3e56b15376")
    teng_xun.send_sms("2018", "15228390982")
