### FreeTest是什么
FreeTest 是一个免费提供验证码服务的开源项目。
目前服务器部署在阿里云ECS，网速和性能都有保障，域名[https://freetest.net.cn/](https://freetest.net.cn/) 。

### 测试Demo
[https://api.freetest.net.cn/demo](https://api.freetest.net.cn/demo) 

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

	*//获取验证码 url 和 token* <br>
	POST /getcode
	
	*//参数说明* <br>
	**appid** 即第一步中申请的appid <br>
	**type**  验证码验证方式，目前仅支持1 <br>
	**sign**  参数签名,大小写不敏感，由"appid;type;secret"md5哈希得到 eg. md5("1000;1;825911868364338FD368FCC9ABC891F2")
		  
	*举例说明：*<br>
	请求 POST https://api.freetest.net.cn/getcode?appid=1000&type=1&sign=4896E104C73A7C31EC40FE9762D24B59 <br>
	返回 {"status":0, "url":"ftstore.kyle.net.cn/ft-1-a094fc94-e09a-4a69-b2f1-b94bb9f7b77f.png", "token":"94bdcb44-5b64-481f-96f1-70b02c8e19ee"}
	
	
	*//验证是否正常输入验证码* <br>
	POST /verify
	
	**appid** 即第一步中申请的appid <br>
	**token** getcode接口返回的token字符串 <br>
	**value**  用户输入的验证码 <br>
	**sign**   参数签名，大小写不敏感 由"appid;token;value;secret"md5哈希得到 eg. md5("1000;94bdcb44-5b64-481f-96f1-70b02c8e19ee;abcd;825911868364338FD368FCC9ABC891F2")

	*举例说明：* <br>
	请求 POST https://api.freetest.net.cn/verify?appid=1000&token=94bdcb44-5b64-481f-96f1-70b02c8e19ee&value=abcd&sign=dd9fe3162bc1bff35b4b1c4630ad744b <br>
	返回 {"status":0, "errmsg":"OK"}

3. 客户端接入
	```
	ajax接入示例：
	$.ajax({
		type:"post",
		url:"https://api.freetest.net.cn/getcode",
		data:{"appid":1000, "type":1, "sign":"4896E104C73A7C31EC40FE9762D24B59"},
		success:function(res){
			json_obj = JSON.parse(res)
			$("#codeimg").attr("src", "https://" +json_obj.url);
		}
	});
	```
	注意 
	* **ft_app_secret** 不能暴露出来，sign可以事先算好了放在HTML前端，也可以由自己服务器发起getcode请求，然后再将验证码url和token发给前端页面。 详细代码请参考 [Demo](https://github.com/kylescript/FreeTest/blob/master/demo/demo.html)
	* getcode接口返回url不带http头， 根据自己的页面需求自行拼接http或者https头。
	* api.freetest.net.cn请求支持http和https，可根据自己需求自行调整。
4. 服务器接入 
	
	```
	python 接入示例
	
	# 用户服务器接口示例
	@app.route('/usercheck', methods=['GET', 'POST'])
	@crossdomain(origin='*')
	def usercheck():
	    if request.method != 'POST':
		return '{"status":-1, "errmsg":"the request type is not POST!"}'
	    token = request.args.get('token')
	    if token is None:
		token = request.form.get('token')
	    phone = request.args.get('phone')
	    if phone is None:
		phone = request.form.get('phone')
	    password = request.args.get('pass')
	    if password is None:
		password = request.form.get('pass')
	    ft_value = request.args.get('value')
	    if ft_value is None:
		ft_value = request.form.get('value')

	    if token is None or phone is None or password is None or ft_value is None:
		return '{"status":-1, "errmsg":"missing token, phone, pass or value param."}'
	    calc_md5 = hashlib.md5("1000;" +
				   str(token) + ";" +
				   str(ft_value) + ";" +
				   ft_app_secret).hexdigest().upper()
	    ft_param = "appid=1000&token=%s&value=%s&sign=%s" % (token, ft_value, calc_md5)
	    req = requests.post("https://api.freetest.net.cn/verify", params=ft_param)
	    if req.status_code == 200:
		json_obj = req.json()
		# 验证码验证成功！
		if json_obj.get('status') == 0:
			# 这里验证phone和pass，验证通过后就算登录成功啦！
			return '{"status":0, "errmsg":"OK"}'
		return '{"status":-1, "errmsg":"FAILED"}'


	# 用户服务器接口示例
	@app.route('/loginok', methods=['GET', 'POST'])
	@crossdomain(origin='*')
	def loginok():
	    return 'LOGIN SUCCESSFULLY!'
	```
	
