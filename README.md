### FreeTest是什么
FreeTest 是一个免费提供验证码服务的开源项目。
目前服务器部署在Amazon EC2免费一年的云服务器上，域名[http://ft.kyle.net.cn/](http://ft.kyle.net.cn/) ， 主域名是我的博客。

### 开发环境：
* 操作系统：Windows、Linux平台
* python环境：python 2.7
* 依赖工具：Redis, Flask, sqlite3, Image, qiniu


### 使用方法：
1. 申请appid 和 appkey

	此功能还在开发中，先写死一对公用的
	```
	ft_app_id = 1000
	ft_app_secret = "825911868364338FD368FCC9ABC891F2"
	```
	
2. 接口说明

	*//获取验证码url和token*
	POST /getcode
	
	*//参数说明*
	**appid** 即第一步中申请的appid
	**type**  验证码验证方式，目前仅支持1
	**sign**  参数签名,大小写不敏感，由"appid;type;secret"md5哈希得到
	eg. md5("1000;1;825911868364338FD368FCC9ABC891F2")
		  
	*举例说明：*
	请求 POST http://ft.kyle.net.cn/getcode?appid=1000&type=1&sign=4896E104C73A7C31EC40FE9762D24B59
	返回 {"status":0, "url":"orrt14ehj.bkt.clouddn.com/ft-1-a094fc94-e09a-4a69-b2f1-b94bb9f7b77f.png", "token":"94bdcb44-5b64-481f-96f1-70b02c8e19ee"}
	
	
	*//验证是否正常输入验证码*
	POST /verify?appid=1000&token=xxxxx&value=abcd&sign=xxx  
	
	**appid** 即第一步中申请的appid
	**token** getcode接口返回的token字符串
	**value**  用户输入的验证码
	**sign**   参数签名，大小写不敏感 由"appid;token;value;secret"md5哈希得到
		 eg. md5("1000;94bdcb44-5b64-481f-96f1-70b02c8e19ee;abcd;825911868364338FD368FCC9ABC891F2")

	*举例说明：*
	请求 POST http://ft.kyle.net.cn/verify?appid=1000&token=94bdcb44-5b64-481f-96f1-70b02c8e19ee&value=abcd&sign=dd9fe3162bc1bff35b4b1c4630ad744b
	返回 {"status":0, "errmsg":"OK"}

3. 客户端接入
	ajax 方式：
	$.ajax({
		type:"post",
		url:"http://ft.kyle.net.cn/getcode",
		data:{"appid":1000, "type":1, "sign":"4896E104C73A7C31EC40FE9762D24B59"},
		success:function(res){
			json_obj = JSON.parse(res)
			$("#codeimg").attr("src", "http://" +json_obj.url);
		}
	});
	注意 **ft_app_secret** 不能暴露出来，sign可以事先算好了放在HTML前端，也可以由自己服务器发起getcode请求，然后再将验证码url和token发给前端页面。

4. 服务器接入 
	


