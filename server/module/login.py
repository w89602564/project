# -*- coding: utf-8 -*-
# 此项目主要参考链接【http://cuiqingcai.com/1076.html，感谢作者的分享

__author__ = 'JustFantasy'

import urllib
import urllib2
# import urllib2.urlopen
# import urlparse
import http.cookiejar
import re

# 模拟登录淘宝类
# 登录淘宝流程
# 1、请求地址https://login.taobao.com/member/login.jhtml获取到token
# 2、请求地址https://passport.alibaba.com/mini_apply_st.js?site=0&token=1L1nkdyfEDIA44Hw1FSDcnA&callback=callback 通过token换取st
# 3、请求地址https://login.taobao.com/member/vst.htm?st={st}实现登录

UA = '110#ftwkAUkfkqXN84dqhwY8Muy22Mnlcsa84NT3AL8UcPeWkvuIsKk22PeIT1UQckTW4KjkR9BKSPItfrXOhwjkmgfy8AmXkkgvPeqw+Gs2kkiFtEnOmUMBmD0E833B2Va7/ejc7HmfhKhgNPGXCKrkhn7ymwrw8TUt5OJfDhQq5EN8Gvq9eadfrLBg7F3687eYlUUNm0xGribQsAkwsBQuqojVj9cwkP5ysLgwqTa4wcjOQxRhDO4kXOGw72UBEXT3D5bys9ZJkccQs3ciD5kkGOmQubZle978sLvwsTQ29zgSgqhwzJ0JuLmwOKrtFlHK2iy2NKRcOiChYe4UmmFOHIDv1GLbYItOl3NDws5tZOETKVqseEnQ4/tgWi+lQyE6to8Z0yKvIkc8cIeQ1RN8rHbbe70Ec8kPNAseyaGDMwnzWPWSbOhc6KetxkqrO22uSjIlvwvm4vIsIIM+ctMwfzcxuiKgQ+/2uSJbjuvu8ABibfzfnq7i8gi/X88HfmR6ZdC9BI1+tz86QAiX7g/OYf9tQBIUS6QE7NG5b/tsA3/7kEUVBspmBI3YrrAbe/s421c0BEBKI+0Dxxu59vx5SRO3eHFueIlnuNsKQDQReTuGHIvmUyI/H6GwgWr5V/6l3MIpIqawJ/p0JtvTImjL228JOlvWwxuRum/7739TiH+sCo2pgKSu0RA/kkyzAzdmNtT+gYQQuC/I3sKjyllwdy3PjP7tXwyp9I9Fwr0q5YyUf2V4Ud0YyT4qwGojVSEdu+JZ//TKvMZRREDRpY4SRodkkCwrSPIRSFQvaw8BNpVIpv+SnVZnHKs/i1fhva9Ul68Q5HzRXKFyMnop19wiz7WZk62rnkNPffFqCkERJnGi7qjzKyMJ4EAQZitHY+ukCLqswLLDtlLqSmkbfKbNjZkaW8H5wcRCbjHaZMFQUOkvi8dkx4TU7sk+3xnjwU75+bT7oWks68M3O2qG4kftYk5evX6b/FxSd4ZLfUMbHVdrXSd+lrccOl1dF4n7j8C61q9J1Su2J8x6Lyp9uKkI4mV0GY6iOlknsYGGmJ2aXox28HiIxoVQ2ZizItD9WASoLblrdnbZVfcR/olBgQd8Mz6QuoQ7FZRHa4zftTyQjeUKoiQegtyQRxn0ay7vBhGijIMAAb7iXZZ2KtkK0iOyJ7rIaolPNWqoYAHOPebI0FGmK8OxEu8fM8HbtoKbb7/pPIvbwsKtTELIjmRrNhADV/ogv8z3H+C4nIh8tw6chGzgWlmxV+TacSk='
USER = u'10金六'.encode(encoding='GBK')
PWD = '33c2a759b398b78df812f0a52b87337fe76dbfaf3f03f3dec6c9a41e445fb19500ea04b3a59e7d02a2b226e8126948cd035227f38699c4c99318931efbea2beec5a5690f557f99dd46d8c3f58ff7d74ee93e20cce902f53a70387a9e4624c5adb7b2051b3c56567b4e6366c3d38e8271b4a8ea549690c2eaaa0647a6c6e906eb'

class Taobao:

	# 初始化方法
	def __init__(self):
		# 登录的URL，获取token
		self.request_url = 'https://login.taobao.com/member/login.jhtml'
		# 通过st实现登录的URL
		self.st_url = 'https://login.taobao.com/member/vst.htm?st={st}'
		# 用户中心地址
		self.user_url = 'https://i.taobao.com/my_taobao.htm'
		# 代理IP地址，防止自己的IP被封禁
		self.proxy_ip = 'http://120.193.146.97:843'
		# 登录POST数据时发送的头部信息
		self.request_headers =  {
			'Host':'login.taobao.com',
			'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
			'Referer' : 'https://login.taobao.com/member/login.jhtml?tpl_redirect_url=https%3A%2F%2Fwww.tmall.com%2F&style=miniall&enup=true&newMini2=true&full_redirect=true&sub=true&from=tmall&allp=assets_css%3D3.0.10/login_pc.css&pms=1535693359739',
			'Content-Type': 'application/x-www-form-urlencoded',
			'Connection' : 'Keep-Alive'
		}

		# 用户名
		self.username = USER
		# ua字符串，经过淘宝ua算法计算得出，包含了时间戳,浏览器,屏幕分辨率,随机数,鼠标移动,鼠标点击,其实还有键盘输入记录,鼠标移动的记录、点击的记录等等的信息
		self.ua = UA
		# 密码，在这里不能输入真实密码，淘宝对此密码进行了加密处理，256位，此处为加密后的密码
		self.password2 = PWD
		self.post = {
			'ua': self.ua,
			'TPL_checkcode': '',
			'CtrlVersion': '1,0,0,7',
			'TPL_password': '',
			'TPL_redirect_url': 'https://www.tmall.com',
			'TPL_username': self.username,
			'loginsite': '0',
			'newlogin': '0',
			'from': 'tmall',
			'fc': 'default',
			'style': 'miniall',
			'css_style': '',
			'tid': 'XOR_1_000000000000000000000000000000_625C4720470A0A050976770A',
			'support': '000001',
			'loginType': '4',
			'minititle': '',
			'minipara': '',
			'umto': 'NaN',
			'pstrong': '3',
			'llnick': '',
			'sign': '',
			'need_sign': '',
			'isIgnore': '',
			'full_redirect': '',
			'popid': '',
			'callback': '',
			'guf': '',
			'not_duplite_str': '',
			'need_user_id': '',
			'poy': '',
			'gvfdcname': '10',
			'gvfdcre': '',
			'from_encoding ': '',
			'sub': '',
			'TPL_password_2': self.password2,
			'loginASR': '1',
			'loginASRSuc': '1',
			'allp': '',
			'oslanguage': 'zh-CN',
			'sr': '1368*912',
			'osVer': '',
			'naviVer': 'firefox|35'
		}


		# 将POST的数据进行编码转换
		self.post_data = urllib.urlencode(self.post).encode(encoding='GBK')
		# 设置代理
		# self.proxy = urllib2.urlopen.ProxyHandler({'http': self.proxy_ip})
		# 设置cookie
		save_file = 'cookie.txt'
		self.cookie = http.cookiejar.LWPCookieJar(save_file)
		# 设置cookie处理器
		self.cookieHandler = urllib2.HTTPCookieProcessor(self.cookie)
		# 设置登录时用到的opener，它的open方法相当于urllib2.urlopen
		# self.opener = urllib2.urlopen.build_opener(self.cookieHandler, self.proxy, urllib2.urlopen.HTTPHandler)
		self.opener = urllib2.build_opener(self.cookieHandler, urllib2.HTTPHandler)
		# 赋值J_HToken
		self.J_HToken = ''
		# 登录成功时，需要的Cookie
		self.newCookie = http.cookiejar.CookieJar()
		# 登陆成功时，需要的一个新的opener
		self.newOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.newCookie))

	# 利用st码进行登录
	# 这一步我是参考的崔庆才的个人博客的教程，因为抓包的时候并没有抓取到这个url
	# 但是如果不走这一步，登录又无法成功
	# 区别是并不需要传递user_name字段，只需要st就可以了
	def login_by_st(self, st):
		st_url = self.st_url.format(st=st)
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
			'Host': 'login.taobao.com',
			'Connection': 'Keep-Alive'
		}
		request = urllib2.Request(st_url, headers=headers)
		response = self.newOpener.open(request)
		content = response.read().decode('gbk')

		#检测结果，看是否登录成功
		pattern = re.compile('top.location.href = "(.*?)"', re.S)
		match = re.search(pattern, content)
		if match:
			self.cookie.save(ignore_discard=True, ignore_expires=True)
			cookie = {}
			for item in self.cookie:
				cookie[item.name] = item.value
			print('登录网址成功')
			return cookie
		else:
			print('登录失败')


	# 程序运行主干
	def main(self):
		try:
			# 请求登录地址， 此时返回的页面中有两个js的引入
			# 位置是页面的前两个JS的引入，其中都带有token参数
			request = urllib2.Request(self.request_url, self.post_data, self.request_headers)
			response = self.opener.open(request)
			# response = urllib2.urlopen(self.request_url, self.post_data, self.request_headers)
			data = response.read()
			content = data.decode('gbk')

			# 抓取页面中的两个获取st的js
			pattern = re.compile('<script src=\"(.*)\"><\/script>')
			match = pattern.findall(content)

			# [
			# 'https://passport.alibaba.com/mini_apply_st.js?site=0&token=1f2f3ePAx5b-G8YbNIlDCFQ&callback=callback',
			# 'https://passport.alipay.com/mini_apply_st.js?site=0&token=1tbpdXJo6W1E4bgPCfOEiGw&callback=callback',
			# 'https://g.alicdn.com/kissy/k/1.4.2/seed-min.js',
			# 'https://g.alicdn.com/vip/login/0.5.43/js/login/miser-reg.js?t=20160617'
			# ]
			# 其中第一个是我们需要请求的JS，它会返回我们需要的st
			#print(match)


			# 如果匹配到了则去获取st
			if match:
				# 此时可以看到有两个st， 一个alibaba的，一个alipay的，我们用alibaba的去实现登录
				# request = urllib2.urlopen.Request(match[0])
				# response = urllib2.urlopen.urlopen(request)
				request = urllib2.Request(match[0])
				response = self.opener.open(request)
				content = response.read().decode('gbk')

				# {"code":200,"data":{"st":"1lmuSWeWh1zGQn-t7cfAwvw"} 这段JS正常的话会包含这一段，我们需要的就是st
				print (content)

				# 正则匹配st
				pattern = re.compile('{"st":"(.*?)"}')
				match = pattern.findall(content)

				# 利用st进行登录
				if match:
					return self.login_by_st(match[0])
				else:
					print ('无法获取到st，请检查')
					return

				# 请求用户中心，查看打印出来的内容，可以看到用户中心的相关信息
				# response = self.newOpener.open(self.user_url)
				# page = response.read().decode('utf-8')
				# print(page)

		except Exception as e:
			print ('请求失败，错误信息：', e)


def start(url):
	taobao = Taobao()
	return taobao.main()



DATA = '''

























<!DOCTYPE html>
<html>
<head>
 <meta http-equiv="X-UA-Compatible" content="IE=Edge">
 <meta charset="gbk"/>
			<meta name="spm-id" content="a220l.1"/>
  <title>确认订单 - Tmall.com天猫-理想生活上天猫</title>
  <link rel="shortcut icon" href="//img.alicdn.com/tfs/TB1XlF3RpXXXXc6XXXXXXXXXXXX-16-16.png" type="image/x-icon"/>
  <script>
 window.g_config = window.g_config || {};
 window.g_config.devId = "pc";
 window.g_config.headerVersion = '1.0.0';
		   window.g_config.loadModulesLater = true;
 window.g_config.sl = 'vm';
 </script>
		
 <script>
 window.g_config = window.g_config || {};
 window.g_config.appId = 15;
 window.g_config.toolbar = false;
 window.g_config.removeSubNav = true;
 window.g_config.removeMallBar = true;
 window.g_config.buyOrderConfig = {
 buInfo: 'tmall'
 };
 g_hb_monitor_st = +new Date;
 </script>
	   <!-- globalmodule version: 3.0.83 -->
<link rel="stylesheet"
 href="//g.alicdn.com/??mui/global/3.0.31/global.css"/>
<script src="//g.alicdn.com/??kissy/k/1.4.14/seed-min.js,mui/seed/1.4.8/seed.js,mui/globalmodule/3.0.83/seed.js,mui/btscfg-g/3.0.0/index.js,mui/bucket/3.0.4/index.js,mui/globalmodule/3.0.83/global-mod-pc.js,mui/globalmodule/3.0.83/global-mod.js,mui/global/3.0.31/global-pc.js,mui/global/3.0.31/global.js"></script>
<script src="//g.alicdn.com/secdev/pointman/js/index.js" app="tmall"></script>
<script>
   TB.environment.isApp = true;
   TB.environment.passCookie = true;
 </script>

   
   <link rel="stylesheet" href="//g.alicdn.com/tp/buy/1.0.23/AIO-tmall.css"/>
   <base target="_blank"/>
</head>
<body class="$bodyClass"><script>
with(document)with(body)with(insertBefore(createElement("script"),firstChild))setAttribute("exparams","category=&userid=1846524763&aplus&yunid=&e361ee93ed6e3&trid=9dff284115361646569703507e&asid=AVu7D24xA5BbidhddwAAAAA97/AZeFqUqQ==",id="tb-beacon-aplus",src=(location>"https"?"//g":"//g")+".alicdn.com/alilog/mlog/aplus_v2.js")
</script>

			<div id="mallPage"
 class="  tmall- page-not-market ">
  <style>
button {
  border-radius: 0;
}
</style>
<!--from fragment-->
<div id="site-nav" data-spm="a2226mz">
	<div id="sn-bg">
		<div class="sn-bg-right">
		</div>
	</div>
	<div id="sn-bd">
		<b class="sn-edge"></b>
		<div class="sn-container">
			<p id="login-info" class="sn-login-info"></p>
			<ul class="sn-quick-menu">
				<li class="sn-mytaobao menu-item j_MyTaobao">
					<div class="sn-menu">
						<a class="menu-hd"
						   href="//i.taobao.com/my_taobao.htm"
						   target="_top" rel="nofollow">我的淘宝<b></b></a>
						<div class="menu-bd">
							<div class="menu-bd-panel" id="myTaobaoPanel">
								<a href="//trade.taobao.com/trade/itemlist/list_bought_items.htm?t=20110530"
								   target="_top" rel="nofollow">已买到的宝贝</a>
								<a href="//trade.taobao.com/trade/itemlist/list_sold_items.htm?t=20110530"
								   target="_top" rel="nofollow">已卖出的宝贝</a>
							</div>
						</div>
					</div>
				</li>
				<li class="sn-seller-center hidden j_SellerCenter">
					<a target="_top" href="//mai.taobao.com/seller_admin.htm">商家中心</a>
				</li>
				<li class="sn-cart"><i class="mui-global-iconfont">&#xf0148;</i>
					<a class="sn-cart-link" href="//cart.tmall.com/cart/myCart.htm?from=btop" target="_top"
					   rel="nofollow">购物车
					</a>
				</li>
				<li class="sn-favorite menu-item">
					<div class="sn-menu">
						<a class="menu-hd"
						   href="//shoucang.taobao.com/shop_collect_list.htm?scjjc=c1"
						   target="_top" rel="nofollow">收藏夹<b></b></a>

						<div class="menu-bd">
							<div class="menu-bd-panel">
								<a href="//shoucang.taobao.com/item_collect.htm" target="_top"
								   rel="nofollow">收藏的宝贝</a>
								<a href="//shoucang.taobao.com/shop_collect_list.htm" target="_top"
								   rel="nofollow">收藏的店铺</a>
							</div>
						</div>
					</div>
				</li>
				<li class="sn-separator"></li>
				<li class="sn-mobile">
					<i class="mui-global-iconfont">&#x3448;</i>
					<a title="天猫无线" target="_top" class="sn-mobile-link" href="//pages.tmall.com/wow/portal/act/app-download?scm=1027.1.1.1">手机版</a>
				</li>
				<li class="sn-home">
					<a href="//www.taobao.com/">淘宝网</a>
				</li>
				<li class="sn-seller menu-item">
					<div class="sn-menu J_DirectPromo">
						<a class="menu-hd" href="//mai.taobao.com" target="_top">商家支持<b></b></a>
						<div class="menu-bd sn-seller-lazy">
						</div>
					</div>
				</li>
				<li class="sn-sitemap">
					<div class="sn-menu">
						<h3 class="menu-hd"><i class="mui-global-iconfont">&#xe601;</i><span>网站导航</span><b></b></h3>
						<div class="menu-bd sn-sitemap-lazy sn-sitemap-bd" data-spm="a2228l4">
						</div>
					</div>
				</li>
			</ul>
		</div>
	</div>
</div>

  <div id="header"
 class=" header-order-app"
 data-spm="a2226n0">
 <div class="headerLayout">
 <div class="headerCon ">
 <h1 id="mallLogo" >
  <span class="mlogo" >
   <a href="//www.tmall.com/" title="天猫Tmall.com"><s></s>天猫Tmall.com</a>
   </span>
  <span class="slogo">
 <a href=""></a>
 </span>
</h1>

 <div class="header-extra">
	   </div>
 </div>
 </div>
 </div>

  <div id="content">

 






















<div class="jet" id="App"></div>
<form  action="/auction/confirm_order.htm?x-itemid=576146218296&amp;x-uid=1846524763"  target="_self" method="post"
 id="multiFormSubmit">
 <input name='_tb_token_' type='hidden' value='e361ee93ed6e3'>
  <input type="hidden" id="F_tb_token" value="e361ee93ed6e3">
 <input type="hidden" name="action" value="order/multiTerminalSubmitOrderAction"/>
 <input type="hidden" name="event_submit_do_confirm" value="1"/>
 <input type="hidden" name="input_charset" value="utf-8"/>
 <input type="hidden" name="praper_alipay_cashier_domain"/>
 <input type="hidden" id="authYiYao" name="authYiYao" value=""/>
 <input type="hidden" id="authHealth" name="authHealth" value=""/>
 <input type="hidden" id="F_nick" name="F_nick" value=""/>
</form>
<script>var orderData = {"endpoint":{"mode":"pc","osVersion":"PC","protocolVersion":"2.0","ultronage":"true"},"data":{"address_1":{"fields":{"addAddressAPI":"/auction/add_buyer_address.htm?_input_charset=utf-8","addrMakerUrl":"//member1.taobao.com/member/fresh/deliver_address_frame.htm?sign=_a2_wr_qwv6w_f_rd_zu8cp_i_w_zj9_x_jms_k_g_z_y7_z_d_l0v_p_ec_v_ai_i%252F0_dd0_j_g_u4v_a%253D%253D&from=tmall&reurl=%2F%2Fbuy.tmall.com%2Forder%2FaddressProxy.htm&version=1.0.10&sign_type=TEP&tid=1846524763","agencyReceive":1,"agencyReceiveH5Url":"//stationpicker-i56.m.taobao.com/inland/showStationInPhone.htm","defaultAddressAPI":"/auction/update_address_selected_status.htm?_input_charset=utf-8","h5SupportIframe":true,"linkAddressId":0,"managerAddressUrl":"//member1.taobao.com/member/fresh/deliver_address.htm","mdSellerId":"1883687207","options":[{"enableMDZT":false,"icon":{"url":""},"deliveryAddressId":1504333636,"needUpdate4Address":false,"addressDetail":"福建省 泉州市 惠安县 三小对面德惠小区2号楼701","cityName":"泉州","enableStation":false,"areaName":"惠安","enforceUpdate4Address":true,"updateAddressTip":"","stationId":0,"townName":"螺城","mobile":"18065327866","fullName":"何国静","divisionCode":"350521","storeAddress":true,"townDivisionId":350521100,"postCode":"362100","countryName":"","provinceName":"福建","addrMakerUrl":"//member1.taobao.com/member/fresh/deliver_address_frame.htm?sign=_a2_wr_qwv6w_f_rd_zu8cp_i_w_zj9_x_jms_k_g_z_y7_z_d_l0v_p_ec_v_ai_i%252F0_dd0_j_g_u4v_a%253D%253D&from=tmall&reurl=%2F%2Fbuy.tmall.com%2Forder%2FaddressProxy.htm&id=1504333636&version=1.0.10&sign_type=TEP&tid=1846524763","lgShopId":0,"defaultAddress":false},{"enableMDZT":false,"icon":{"url":""},"deliveryAddressId":8570929038,"needUpdate4Address":true,"addressDetail":"恒泰蓝湾售楼部 ","cityName":"淮安","enableStation":false,"areaName":"盱眙","enforceUpdate4Address":true,"updateAddressTip":"","stationId":0,"mobile":"15851704755","fullName":"赵建娣 ","divisionCode":"320830","storeAddress":true,"townDivisionId":0,"postCode":"000000","countryName":"","provinceName":"江苏","lgShopId":0,"defaultAddress":false},{"enableMDZT":false,"icon":{"url":""},"deliveryAddressId":8611770224,"needUpdate4Address":false,"addressDetail":"汀江西路2号天士力医药集团股份人力 综合办公楼325","cityName":"天津","enableStation":false,"areaName":"北辰","enforceUpdate4Address":true,"updateAddressTip":"","stationId":0,"townName":"科技园区北区","mobile":"18649013628","fullName":"宋坤钰","divisionCode":"120113","storeAddress":true,"townDivisionId":120113400,"postCode":"000000","countryName":"","provinceName":"天津","lgShopId":0,"defaultAddress":false},{"enableMDZT":false,"icon":{"url":""},"deliveryAddressId":8598130934,"needUpdate4Address":false,"addressDetail":" 新塘久裕村《平地》布匹街A022号 伟业纺织","cityName":"广州","enableStation":false,"areaName":"增城","enforceUpdate4Address":true,"updateAddressTip":"","stationId":0,"townName":"新塘","mobile":"13434399935","fullName":"苏伟东","divisionCode":"440183","storeAddress":true,"townDivisionId":440183101,"postCode":"000000","countryName":"","provinceName":"广东","lgShopId":0,"defaultAddress":false},{"enableMDZT":false,"icon":{"url":""},"deliveryAddressId":7312472270,"needUpdate4Address":false,"addressDetail":"环城南路定安天九文化美食广场菜鸟网络农村物流定安县服务中心(DA0004:15088133977)","cityName":"","enableStation":false,"areaName":"定安","enforceUpdate4Address":true,"updateAddressTip":"","stationId":0,"townName":"定城","mobile":"13066231646","fullName":"吴十金","divisionCode":"469025","storeAddress":true,"townDivisionId":469021100,"postCode":"571200","countryName":"","provinceName":"海南","lgShopId":0,"defaultAddress":false},{"enableMDZT":false,"icon":{"url":""},"deliveryAddressId":8569516368,"needUpdate4Address":false,"addressDetail":"官渡区 盛惠园小区35栋902","cityName":"昆明","enableStation":false,"areaName":"官渡","enforceUpdate4Address":true,"updateAddressTip":"","stationId":0,"townName":"金马","mobile":"18350971531","fullName":"王寒","divisionCode":"530111","storeAddress":true,"townDivisionId":530111004,"postCode":"000000","countryName":"","provinceName":"云南","lgShopId":0,"defaultAddress":false},{"enableMDZT":false,"icon":{"url":""},"deliveryAddressId":7897933149,"needUpdate4Address":false,"addressDetail":"猎德花园5区崇礼楼1605","cityName":"广州","enableStation":false,"areaName":"天河","enforceUpdate4Address":true,"updateAddressTip":"","stationId":0,"townName":"猎德","mobile":"13066231646","fullName":"吴晓流","divisionCode":"440106","storeAddress":true,"townDivisionId":440106013,"postCode":"510510","countryName":"","provinceName":"广东","lgShopId":0,"defaultAddress":false},{"enableMDZT":false,"icon":{"url":""},"deliveryAddressId":8555520983,"needUpdate4Address":false,"addressDetail":"共和新路625弄2号201室丙","cityName":"上海","enableStation":false,"areaName":"静安","enforceUpdate4Address":true,"updateAddressTip":"","stationId":0,"townName":"芷江西路","mobile":"15821869752","fullName":"董家锟  ","divisionCode":"310106","storeAddress":true,"townDivisionId":310108016,"postCode":"000000","countryName":"","provinceName":"上海","lgShopId":0,"defaultAddress":false},{"enableMDZT":false,"icon":{"url":""},"deliveryAddressId":8577090367,"needUpdate4Address":true,"addressDetail":"浙江大学宁波理工学院","cityName":"宁波","enableStation":false,"areaName":"鄞州","enforceUpdate4Address":true,"updateAddressTip":"","stationId":0,"mobile":"15215902736","fullName":"陈晨","divisionCode":"330212","storeAddress":true,"townDivisionId":0,"postCode":"000000","countryName":"","provinceName":"浙江","lgShopId":0,"defaultAddress":false},{"enableMDZT":false,"icon":{"url":""},"deliveryAddressId":5118125487,"needUpdate4Address":false,"addressDetail":"中发西路40号爱乐群有限公司","cityName":"佛山","enableStation":false,"areaName":"顺德","enforceUpdate4Address":true,"updateAddressTip":"","tele":"0799-3428906","stationId":0,"townName":"北滘","mobile":"18925957529","fullName":"李爱梅","divisionCode":"440606","storeAddress":true,"townDivisionId":440606102,"postCode":"528300","countryName":"","provinceName":"广东","lgShopId":0,"defaultAddress":false},{"enableMDZT":false,"icon":{"url":""},"deliveryAddressId":8502774224,"needUpdate4Address":true,"addressDetail":"西北农林科技大学南校区","cityName":"咸阳","enableStation":false,"areaName":"杨陵","enforceUpdate4Address":true,"updateAddressTip":"","stationId":0,"mobile":"18821617685","fullName":"李佳恒  ","divisionCode":"610403","storeAddress":true,"townDivisionId":0,"postCode":"000000","countryName":"","provinceName":"陕西","lgShopId":0,"defaultAddress":false},{"enableMDZT":false,"icon":{"url":""},"deliveryAddressId":1507791453,"needUpdate4Address":false,"addressDetail":"紫阳大道瑶湖高校园区江西科技学院","cityName":"南昌","enableStation":false,"areaName":"青山湖","enforceUpdate4Address":true,"updateAddressTip":"","stationId":0,"townName":"艾溪湖管理处","mobile":"15797684263","fullName":"曾琳芳","divisionCode":"360111","storeAddress":true,"townDivisionId":360111490,"postCode":"511400","countryName":"","provinceName":"江西","lgShopId":0,"defaultAddress":false},{"enableMDZT":false,"icon":{"url":""},"deliveryAddressId":7585863084,"needUpdate4Address":false,"addressDetail":"政府附近定新路47号","cityName":"","enableStation":false,"areaName":"定安","enforceUpdate4Address":true,"updateAddressTip":"","stationId":0,"townName":"新竹","mobile":"17733121060","fullName":"吴十金","divisionCode":"469025","storeAddress":true,"townDivisionId":469021101,"postCode":"571200","countryName":"","provinceName":"海南","lgShopId":0,"defaultAddress":false},{"enableMDZT":false,"icon":{"url":""},"deliveryAddressId":7045881711,"needUpdate4Address":false,"addressDetail":"定新街47号","cityName":"","enableStation":false,"areaName":"定安","enforceUpdate4Address":true,"updateAddressTip":"","stationId":0,"townName":"新竹","mobile":"13337566963","fullName":"陈梅花","divisionCode":"469025","storeAddress":true,"townDivisionId":469021101,"postCode":"571200","countryName":"","provinceName":"海南","lgShopId":0,"defaultAddress":false},{"enableMDZT":false,"icon":{"url":""},"deliveryAddressId":5539154541,"needUpdate4Address":true,"addressDetail":"龙华二横路对面华典大厦一楼银座造型","cityName":"海口","enableStation":false,"areaName":"龙华","enforceUpdate4Address":true,"updateAddressTip":"","stationId":0,"mobile":"18289656514","fullName":"丽娜(陈柳青)","divisionCode":"460106","storeAddress":true,"townDivisionId":0,"postCode":"000000","countryName":"","provinceName":"海南","lgShopId":0,"defaultAddress":false},{"enableMDZT":false,"icon":{"url":""},"deliveryAddressId":1735610320,"needUpdate4Address":false,"addressDetail":"东成街五邑大学(南门)","cityName":"江门","enableStation":false,"areaName":"蓬江","enforceUpdate4Address":true,"updateAddressTip":"","stationId":0,"townName":"仓后","mobile":"13066231646","fullName":"吴小柳","divisionCode":"440703","storeAddress":true,"townDivisionId":440703001,"postCode":"529020","countryName":"","provinceName":"广东","lgShopId":0,"defaultAddress":false},{"enableMDZT":false,"icon":{"url":""},"deliveryAddressId":5443075412,"needUpdate4Address":true,"addressDetail":"渔湖镇揭阳市渔湖试验区京南村京南小学  电话:0663-8301209","cityName":"揭阳","enableStation":false,"areaName":"榕城","enforceUpdate4Address":true,"updateAddressTip":"","stationId":0,"mobile":"13352731209","fullName":"孙树才","divisionCode":"445202","storeAddress":true,"townDivisionId":0,"postCode":"000000","countryName":"","provinceName":"广东","lgShopId":0,"defaultAddress":false},{"enableMDZT":false,"icon":{"url":""},"deliveryAddressId":5125344836,"needUpdate4Address":false,"addressDetail":"友爱路37号雅斯特酒店(南宁友宁店)","cityName":"南宁","enableStation":false,"areaName":"西乡塘","enforceUpdate4Address":true,"updateAddressTip":"","stationId":0,"townName":"北湖","mobile":"18877105744","fullName":"黄江娜","divisionCode":"450107","storeAddress":true,"townDivisionId":450107002,"postCode":"523000","countryName":"","provinceName":"广西","lgShopId":0,"defaultAddress":false}],"postCodeAPI":"/auction/json/get_postcode.do?_input_charset=utf-8","selectedId":1504333636,"showForwardTip":false,"supportFwd":false,"tempAddress":false,"updateAddressAPI":"/auction/update_buyer_address.htm?_input_charset=utf-8","useMDZT":false,"useStation":false},"id":"1","ref":"c67d863","tag":"address","type":"biz"},"agencyPay_1":{"fields":{"checked":false,"disabled":false,"name":"朋友代付(不支持运费险)"},"id":"1","submit":true,"tag":"agencyPay","type":"biz"},"anonymous_1":{"fields":{"checked":true},"id":"1","submit":true,"tag":"anonymous","type":"biz"},"confirmOrder_1":{"fields":{"aliPayUid":"20881121705643200156","bItemDomain":"//detail.tmall.com/item.htm","buyerId":1846524763,"cItemDomain":"//item.taobao.com/item.htm","catInfo":"16:50010850","currencySymbol":"￥","fromBuyNow":true,"fromCart":false,"fromMallMiniCart":false,"fromMallYaoCart":false,"gid":"gid_697530717091","hasHKitem":false,"isShowVillager":false,"joinId":"9ea1de6926790ad8b146a49b99a73f14","mkEmbedTmallH5":false,"offerId":0,"openFrontTrace":true,"orderFromType":"mall_normal","outerShopId":0,"pcSubmitUrl":"/auction/confirm_order.htm?x-itemid=576146218296&x-uid=1846524763","platform":"PC","quoteId":0,"secretKey":"submitref","secretValue":"0a67f6","sellerInfoDomain":"//member1.taobao.com/member/user_profile.jhtml","sessionId":"aa0c4890dde0c29a1105ea5cf855d8f3","sessionUserId":"fb314a9bf4260b80f3eb7c9f17d3b753","shopDomain":"//store.taobao.com/shop/view_shop.htm","siteFrom":"CN","sourceTime":"","sparam1":"eyJsaXN0Ijp7Ijc5NTkwMDYiOnsiYnV5YW1vdW50IjoxLCJkaXNjb3VudFRvdGFsRmVlIjoxOTgwMCwic2VsbGVySWQiOjE4ODM2ODcyMDcsInRvdGFsRmVlIjozODYwMH19LCJsb2dpc1JlY3ZBZGRyIjoi56aP5bu655yBIOazieW3nuW4giDmg6Dlronljr8g5LiJ5bCP5a+56Z2i5b635oOg5bCP5Yy6MuWPt+alvDcwMSIsImxvZ2lzUmVjdk1vYmwiOiIxODA2NTMyNzg2NiIsIm9yZGVyZnJvbXdoZXJlIjoidG1hbGxfcGMiLCJ1bWlkIjoiQ1YxYno1YjZlZDg1YTM1MTA2Y2JiMDAwOTI5NTRlY2Y5In0=","sparam2":"eyJsaXN0Ijp7Ijc5NTkwMDYiOnsiYnV5UXVhbnRpdHkiOjEsImNhdGlkIjo1MDAxMDg1MCwiaXRlbUlkIjo1NzYxNDYyMTgyOTYsIm9sZFN0YXJ0IjoxNTM1MDk2OTI0MDAwLCJvcHRpb25zIjo1NzA0MjUzNDUsIm9yZGVyQ29zdCI6NTgyLCJyZXNydlByaWNlIjozODYwMCwic2t1SWQiOjM5NTY1MDYxMDM2NTcsInRhZ3MiOiI1ODcsOTA3LDExNTQsMTE2MywxNDc4LDE0ODMsMTY3NSwxODAzLDIwNDksMjA1OSwyNDQzLDI1MDcsMjYzNSwzMDE5LDM4NTEsMzkxNSwzOTc0LDQxMDcsNDE2Niw0MTcxLDQzNjMsNDQ5MSw0NTUwLDQ1NTUsNDYxNCw0Njc4LDQ4MTEsNTgzNSw1ODk1LDY0MTEsNjYwMyw3MzcxLDc0MzEsNzk0Nyw4MzI2LDExMDgzLDExMjY2LDExMzM5LDExNTMxLDExNTk1LDEyNDkxLDEzNzA3LDEzNzcxLDE1NTU0LDE1NTYzLDE2Mzk1LDE3NzM5LDE3ODAzLDIxNDQyLDI1MjgyLDI3NTIxLDI4MzUzLDI4ODAyLDI5Njk3LDI5ODg5LDMwMzM3LDMwNDAxLDMwNTkzLDMwNjU3LDMwODQ5LDMwOTc3LDMzMjgxLDMzMzQ1LDM0NDMzLDM1MTM3LDM1NzEzLDM2MTYxLDM2NDE3LDM3NTY5LDM5MjMzLDQwODk3LDQ2ODQ5LDQ4NzA2LDUxMzI5LDUxNTg1LDUxODQxLDUxOTY5LDUzNTY5LDU3MDI2LDU5MDEwLDYwNDE4LDYyMDgyLDY3NTIxLDcwNDAxLDcyMzg2LDczMDg5LDczNjAxLDc0MzY5LDc0NTYxLDc0Njg5LDc0NzUzLDc5NDg5LDgxNzkzLDgyMzA2LDg0NjczLDg0ODAxLDg0ODY1LDg2MDgxLDg3MzYxLDg5NjY1LDkxMjAxLDkxNzEzLDkxNzc3LDk1MTA1LDk1NjE3LDk1NzQ1LDk1ODczLDk2NTEzLDEwMTc2MiwxMDMzNjEsMTAzNDg5LDEwNzg0MiwxMTIzODYsMTQzNzQ2LDE2NjQwMiwyMDIwNTAsMjEyNTQ2LDI0OTg1OCwyNTc3OTQsMjgxNjAyLDI4MTY2NiwyODI1NjIsMjgyODE4LDI4Mjg4MiIsInRpdGxlIjoi6Z+p6K+t55Cz56eL6KOF5oCn5oSf6Zyy6IKp6KOZ5a2QMjAxOOaWsOasvuWls+ijhemfqeeJiOmVv+iilue6ouiJsue9kee6sei/nuiho+ijmeefreijmSIsInZpcnR1YWwiOmZhbHNlfX19","traceId":"9dff284115361646569703507e","umid":"CV1bz5b6ed85a35106cbb00092954ecf9","umidToken":"T2d6955aff5608ec7ab04da637e180d99","unitSuffix":"gtj","userIdStr":"fb314a9bf4260b80f3eb7c9f17d3b753"},"id":"1","ref":"0493832","tag":"confirmOrder","type":"biz"},"ctDeliverySolution_1":{"fields":{"addressId":"1504333636","bind":false,"defaultSelected":false,"disabled":false,"eleRail":false,"selected":false,"supportPostFee":false},"id":"1","ref":"d7770f0","submit":true,"tag":"ctDeliverySolution","type":"biz"},"ctRailSolution_9ea1de6926790ad8b146a49b99a73f14":{"fields":{"deliveryrail":false,"eleRail":false,"feature":"{}","soldRail":false},"id":"9ea1de6926790ad8b146a49b99a73f14","ref":"e77a6d3","submit":true,"tag":"ctRailSolution","type":"biz"},"deliveryMethod_12a473f325ccdbd120a51d91afa3727b":{"fields":{"checked":true,"options":[{"serviceType":"-4","fare":"0.00","signText":"","message":"快递 免邮","hasOption":false,"extra":"","titleText":"普通配送","fareCent":0,"id":"2"}],"secondOption":false,"selectedId":"2"},"hidden":{"extensionMap":{"deliveryId":"12a473f325ccdbd120a51d91afa3727b"}},"id":"12a473f325ccdbd120a51d91afa3727b","ref":"4188366","submit":true,"tag":"deliveryMethod","type":"biz"},"dsDesc_1":{"fields":{"agencyId":0,"agencyReceive":1,"disable":false,"linkAddressId":1504333636,"linkDivisionCode":"350521","linkTownDivisionCode":"350521100","options":[],"selectedId":0,"sellerId":"1883687207","useAgencyType":0},"id":"1","tag":"dsDesc","type":"biz"},"frontTrace_1":{"fields":{"joinId":"697530717091"},"id":"1","submit":true,"tag":"frontTrace","type":"biz"},"itemInfo_9ea1de6926790ad8b146a49b99a73f14":{"fields":{"icons":{"main":[{"text":"","colorCode":null,"title":"消费者保障服务，卖家承诺7天退换","image":"//img.alicdn.com/tps/i3/T1Vyl6FCBlXXaSQP_X-16-16.png","link":"//pages.tmall.com/wow/seller/act/seven-day","href":null,"css":null,"sortNo":10},{"text":"","colorCode":null,"title":"消费者保障服务，卖家承诺如实描述","image":"//img.alicdn.com/tps/i4/T1BCidFrNlXXaSQP_X-16-16.png","link":"//www.taobao.com/go/act/315/xfzbz_rsms.php?ad_id=&am_id=130011830696bce9eda3&cm_id=&pm_id=","href":null,"css":null,"sortNo":11},{"text":"","colorCode":null,"title":"支持信用卡支付","image":"//assets.alicdn.com/sys/common/icon/trade/xcard.png","link":null,"href":null,"css":null}]},"irefer":"detail.tmall.com","isGift":false,"itemInfoId":576146218296,"itemUrl":"//detail.tmall.com/item.htm?id=576146218296","pic":"//img.alicdn.com/bao/uploaded/i2/1883687207/TB284hpscIrBKNjSZK9XXagoVXa_!!1883687207.jpg","price":"386.00","rrefer":"","sellerNick":"韩语琳空间服饰旗舰店","shopUrl":"//store.taobao.com/shop/view_shop.htm?shop_id=107567887","skuId":3956506103657,"skuInfo":[{"forOld":false,"name":"颜色分类","value":"红色"},{"forOld":false,"name":"尺码","value":"S"}],"skuLevelInfo":[],"subtitles":[],"title":"韩语琳秋装性感露肩裙子2018新款女装韩版长袖红色网纱连衣裙短裙"},"id":"9ea1de6926790ad8b146a49b99a73f14","ref":"87bd910","tag":"itemInfo","type":"biz"},"itemPay_9ea1de6926790ad8b146a49b99a73f14":{"fields":{"price":"198.00","quantity":1,"weight":0},"id":"9ea1de6926790ad8b146a49b99a73f14","tag":"itemPay","type":"biz"},"item_9ea1de6926790ad8b146a49b99a73f14":{"fields":{"bizCode":"tmall.general.clothes","cartId":0,"eticketMailType":"post","itemId":576146218296,"shoppingOrderId":0,"skuId":3956506103657,"valid":true,"villagerId":0},"id":"9ea1de6926790ad8b146a49b99a73f14","tag":"item","type":"biz"},"memo_12a473f325ccdbd120a51d91afa3727b":{"fields":{"name":"给卖家留言：","placeHolder":"选填:填写内容已和卖家协商确认","value":""},"id":"12a473f325ccdbd120a51d91afa3727b","ref":"9055a69","submit":true,"tag":"memo","type":"biz"},"ncCheckCode_ncCheckCode1":{"fields":{"nc":"1","token":"df79f320ecb10c171fd409345cfab5d073f00386"},"id":"ncCheckCode1","ref":"cbf3cf8","submit":true,"tag":"ncCheckCode","type":"biz"},"orderInfo_12a473f325ccdbd120a51d91afa3727b":{"fields":{"icon":{"image":"//gw.alicdn.com/tfs/TB1CzD7SXXXXXXJaXXXXXXXXXXX-32-32.png","text":""},"nick":"韩语琳空间服饰旗舰店","sellerInfo":"?encUserNumId=IDX1Td69JipLKXBqrL9zf9r63GGBnp6Cum_bxHbrIzAgpZnPWYSc54qKQyta2vz4Utxy&sign=f42e7f2444b000de595d572c54f5196c","sellerType":"TmallSeller","shopUrl":"//store.taobao.com/shop/view_shop.htm?shop_id=107567887","title":"韩语琳空间服饰旗舰店","uid":"1883687207"},"id":"12a473f325ccdbd120a51d91afa3727b","tag":"orderInfo","type":"biz"},"orderPay_12a473f325ccdbd120a51d91afa3727b":{"fields":{"hasService":false,"isIncTax":false,"isOrderGroup":false,"price":"198.00","quantity":1,"weight":0},"id":"12a473f325ccdbd120a51d91afa3727b","tag":"orderPay","type":"biz"},"order_12a473f325ccdbd120a51d91afa3727b":{"fields":{"inBond":false,"inGroup":false,"sellerId":"1883687207","valid":true},"id":"12a473f325ccdbd120a51d91afa3727b","tag":"order","type":"biz"},"promotion_9ea1de6926790ad8b146a49b99a73f14":{"fields":{"options":[{"gift":"","fullTitle":"已省188元:秋季新品","disCountCent":18800,"discount":"188.00","id":"Tmall$commonItemPromotion-6592285874_44416253748","title":"省188:秋季新品","freedelivery":false,"desc":"<ul><li>秋季新品：省188.00元</li></ul>"}],"orderOutId":"9ea1de6926790ad8b146a49b99a73f14","outId":"9ea1de6926790ad8b146a49b99a73f14","promotionType":"item","selectedId":"Tmall$commonItemPromotion-6592285874_44416253748","title":"商品优惠"},"id":"9ea1de6926790ad8b146a49b99a73f14","quark":-18800,"submit":true,"tag":"promotion","type":"biz"},"quantity_9ea1de6926790ad8b146a49b99a73f14":{"fields":{"editable":true,"max":26,"min":1,"quantity":1,"step":1,"title":"购买数量"},"id":"9ea1de6926790ad8b146a49b99a73f14","tag":"quantity","type":"biz"},"realPay_1":{"fields":{"mallTotalPrice":19800,"microPurchaseTotalPrice":0,"originPrice":"386.00","price":"198.00","quantity":1,"tmallHkTotalPrice":0,"weight":0},"id":"1","quark":19800,"tag":"realPay","type":"biz"},"stepbar_1":{"fields":{"current":0,"options":["拍下商品","付款到支付宝","确认收货","评价"],"stepBarType":"MALL_BUY_NOW"},"id":"1","tag":"stepbar","type":"biz"},"submitOrder_1":{"fields":{"isTmallHKPresellOrder":false,"isTmallHKPresellSelf":false,"needUpdate4Address":false,"submitOrderType":"UNITY","submitTitle":"提交订单","tmallPointStatus":"0"},"id":"1","status":"normal","submit":true,"tag":"submitOrder","type":"biz"},"urlTransfer_1":{"fields":{},"id":"1","tag":"urlTransfer","type":"biz"}},"linkage":{"common":{"compress":true,"queryParams":"^^$$Z212c21e06fe561f8ac193953fc8868bae|null{$_$}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","submitParams":"^^$$Z2c799e3e3743facfe98493fa4def4f1c4|null{$_$}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","validateParams":"^^$$dc18eafee0f7bf086988bb0bc5892343{$_$}H4sIAAAAAAAAAIVQzWrCQBh8lz3LoiYxwVtMDBSsBGqFnsrn5lOD+8fuSmvFN+hj9FL6XKWv0S+VUnsovc3MfjszzJGtHSh8MG5XAyF/paxk4yOzEsLaOLU4WOy4kOD9nE7ZmAmjOMh2BSvgwUGDXMgWdeDKNCi5N3snkNcXDssh6zF9/l0XhI1rWg2UNDj1mIUN/pUTwKzAcILW6C6jOZBPK7jCABdyhyQ+8snt3ZDX34Znb7IKCqQk2qAXRN9fXj+e34grcDsMpPz0W1zns9mvikPqKI0A2T0/be+LOSNl79Hl3rcb/f8+fgsOG24deioLoTWa225vXkKAJR03X/Ofd0Jsii2KXUFzsvEapMceQy3cwYab4Fq9oZB+WU3TUToZZWWVFFGW5VEV5XGSlv2siAf9PE3SbFpOq2QyjaMyZqfTJ9ZTq8rtAQAA"},"input":["ctRailSolution_9ea1de6926790ad8b146a49b99a73f14","ctDeliverySolution_1","memo_12a473f325ccdbd120a51d91afa3727b"],"request":["promotion_9ea1de6926790ad8b146a49b99a73f14","deliveryMethod_12a473f325ccdbd120a51d91afa3727b","address_1","agencyPay_1","quantity_9ea1de6926790ad8b146a49b99a73f14"],"signature":"2047da3f586e7149d839e324e8a44389","url":"/auction/json/async_linkage.do?_input_charset=utf-8"},"hierarchy":{"component":["item","quantity","address","realPay","ctRailSolution","deliveryMethod","stepbar","memo","itemInfo","orderPay","ctDeliverySolution","frontTrace","confirmOrder","urlTransfer","itemPay","ncCheckCode","orderInfo","submitOrder","dsDesc","anonymous","promotion","order","agencyPay"],"root":"confirmOrder_1","structure":{"confirmOrder_1":["stepbar_1","address_1","dsDesc_1","order_12a473f325ccdbd120a51d91afa3727b","agencyPay_1","anonymous_1","realPay_1","submitOrder_1","frontTrace_1","urlTransfer_1","ncCheckCode_ncCheckCode1","ctDeliverySolution_1"],"item_9ea1de6926790ad8b146a49b99a73f14":["itemInfo_9ea1de6926790ad8b146a49b99a73f14","quantity_9ea1de6926790ad8b146a49b99a73f14","promotion_9ea1de6926790ad8b146a49b99a73f14","itemPay_9ea1de6926790ad8b146a49b99a73f14","ctRailSolution_9ea1de6926790ad8b146a49b99a73f14"],"order_12a473f325ccdbd120a51d91afa3727b":["orderInfo_12a473f325ccdbd120a51d91afa3727b","item_9ea1de6926790ad8b146a49b99a73f14","deliveryMethod_12a473f325ccdbd120a51d91afa3727b","memo_12a473f325ccdbd120a51d91afa3727b","orderPay_12a473f325ccdbd120a51d91afa3727b"]}},"reload":true} ;</script>
<div class="loading-mask"></div>
<div class="loading">
 <p class="bg q"></p>

 <p class="bg z"></p>
</div>
<!–[if lte IE 8]>
<script src="//g.alicdn.com/tp/buy/1.0.23/lib/es5-shim.js"></script>
<script src="//g.alicdn.com/tp/buy/1.0.23/lib/es5-sham.js"></script>
<script src="//g.alicdn.com/tp/buy/1.0.23/lib/console-polyfill.js"></script>
<![endif]->
<script src="//g.alicdn.com/tp/buy/1.0.23/AIO.js"></script>

<script>
 var UA_Opt = {};
 UA_Opt.LogVal = "ua_log", UA_Opt.SendMethod = 8, UA_Opt.MaxMCLog = 150, UA_Opt.MaxKSLog = 150, UA_Opt.MaxMPLog = 150, UA_Opt.MaxGPLog = 5, UA_Opt.MaxTCLog = 150, UA_Opt.GPInterval = 50, UA_Opt.MPInterval = 50, UA_Opt.MaxFocusLog = 150, UA_Opt.Token = (new Date).getTime() + ":" + Math.random(), UA_Opt.isSendError = 1, UA_Opt.GetAttrs = ["href", "src"], UA_Opt.Flag = 1966079;
</script>
<script src="//af.alicdn.com/js/uac.js"></script>
<div id="_umfp" style="display:inline;width:1px;height:1px;overflow:hidden">
 <img src="https://ynuf.alipay.com/service/clear.png?xt=T2d6955aff5608ec7ab04da637e180d99&xa=buy_confirm_order"/>
</div>
<script>
 var container = document.getElementById("_umfp");
 window._um_config = {
 timeout: 3e3,
 timestamp: "26766504535A5E46574C6579",
 token: "T2d6955aff5608ec7ab04da637e180d99",
 serviceUrl: "https://ynuf.alipay.com/service/um.json",
 appName: "buy_confirm_order",
 containers: {flash: container, dcp: container}
 };
</script>
<input type="hidden" id="tbToken" name="_tb_token_" value="e361ee93ed6e3"/>



   </div>         <div id="footer" data-spm="a2226n1" class="">
   
   <div id="tmall-ensure">
   <a href="//pages.tmall.com/wow/seller/act/newpinzhibaozhang"></a>
 <a href="//www.tmall.com/wow/seller/act/seven-day"></a>
 <a href="//www.tmall.com/wow/seller/act/special-service"></a>
   <a href="//service.tmall.com/support/tmall/tmallHelp.htm"></a>
	 </div>
   <div id="tmall-desc">
   <div class="mui-global-fragment-load" data-fragment="tmbase/mui_footer_desc"></div>
   </div>
 <div id="tmall-copyright">
 <div class="mui-global-fragment-load" data-fragment="tmbase/mui_footer_link"></div>
 </div>
	 <div id="server-num">buy2010150202070.unsz.su18</div>
</div>
</div>

 <div class="tc-reporter"><span>

<a target="_blank" id="ue-entrance" data-spm="a220l.12.5.99" href="&#x2F;&#x2F;www.tmall.com&#x2F;wh&#x2F;tmall&#x2F;lost&#x2F;act&#x2F;buytrade20150616?acm=lb-zebra-26053-322551.1003.8.449644&amp;spm=0.0.0.0.qlWgDg&amp;scm=1003.8.lb-zebra-26053-322551.ITEM_14432082759631_449644" >给下单页面提建议</a>  
<s></s></span>
</div>
<script>
 var en = document.getElementById("ue-entrance");
 var data = (window.orderData && window.orderData.data) ? window.orderData.data : "";
 if (data && en) {
 for (i in data) {
 if (data[i].tag == "frontTrace") {
 var jId = data[i].fields.joinId;
 en.href += "&joinId=" + jId
 }
 }
 }
</script>
<div id="server-num">buy2010150202070.unsz.su18 9dff284115361646569703507e</div>

<script src="//g.alicdn.com/mui/??bat/4.0.35/index.js,tes/4.2.17/index.js"></script>
</body>
</html>
'''

if __name__ == '__main__':
	pattern = re.compile('<script>var orderData =(.*);<\/script>')
	match = pattern.findall(DATA)
	import json
	
	print (json.loads(match[0]))