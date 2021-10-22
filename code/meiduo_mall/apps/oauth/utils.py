from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from meiduo_mall import settings
from itsdangerous import BadSignature, BadHeader, SignatureExpired, BadTimeSignature
def generic_openid(openid):
    s = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600)
    access_token = s.dumps({'openid': openid})

    # 将byte数据转换为 str
    return access_token.decode()


def check_access_token(token):
    s = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600)
    try:
        result = s.loads(token)
    except Exception:
        return ["token 有误，解析失败"]
    else:
        return result.get('openid')
