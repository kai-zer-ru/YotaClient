import urllib
import urllib2
import cookielib
import json
# urlLogin = "https://login.yota.ru/UI/Login?goto=https://my.yota.ru:443/selfcare/loginSuccess&gotoOnFail=https://my.yota.ru:443/selfcare/loginError&org=customer&ForceAuth=true&old-token=%s&IDToken2=%s&IDToken1=6035498867"
urlLogin = "https://login.yota.ru/UI/Login"
ConfFile = "settings.conf"
Conf = {}

SpeedConf = {}

def ReadConf():
	global Conf
	myfile = open(ConfFile, "r")
	# print myfile.readlines()
	for line in myfile.readlines():
		params_string = line.replace("\n", "")
		params = params_string.split("=")
   		Conf[params[0]] = params[1]

def GetConfParam(key, default_value = ""):
	global Conf
	if key in Conf:
		return Conf[key]
	return default_value

def GetConfIntParam(key, default_value = 0):
	global Conf
	if key in Conf:
		return Conf[key]
	return default_value

def Auth():
	UserLogin = GetConfParam('UserLogin')
	UserPass  = GetConfParam('UserPass')
	cookie = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
	urllib2.install_opener(opener)
	headers = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686; ru; \
                    rv:1.9.2.6) Gecko/20100628 Ubuntu/10.04 (lucid) \
                    Firefox/3.6.6",
                   "Accept": "text/html,application/xhtml+xml,application\
                   /xml;q=0.9,*/*;q=0.8"}
	values = {
		"goto":       "https://my.yota.ru:443/selfcare/loginSuccess",
		"gotoOnFail": "https://my.yota.ru:443/selfcare/loginError",
		"org":        "customer",
		"ForceAuth":  True,
		"old-token":  UserLogin,
		"IDToken2":   UserPass,
		"IDToken1":   "6035498867",
	}
	params_auth = urllib.urlencode(values)
	request_auth = urllib2.Request(urlLogin, params_auth, headers)
	page_auth = urllib2.urlopen(request_auth).read()
	return page_auth

def GetListOfParams(page_auth):
	list_of_params = page_auth[page_auth.find("var sliderData = ") + len("var sliderData = "):]
	list_of_params = list_of_params[:list_of_params.find("};")+1]
	list_of_params = list_of_params.replace("<div class=\\\"max-value\\\">", "").replace("<\\/div>", "").replace("<strong>", "").replace("<\\/strong>","").replace("<span>","").replace("<\\/span>","")
	list_of_params = json.loads(list_of_params)
	return list_of_params

def main ():
	global urlLogin, Conf, SpeedConf
	ReadConf()
	page_auth = Auth()
	list_of_params = GetListOfParams(page_auth)
	productId = list_of_params.keys()[0]
	Conf['productId'] = productId
	list_of_params = list_of_params[productId]

	steps, offerCode, currentProduct, SpeedConf = GetSpeedConf(list_of_params)
	Conf['steps'] = steps
	Conf['offerCode'] = offerCode
	print currentProduct

def GetSpeedConf(list_of_params):
	steps = list_of_params['steps']
	offerCode = list_of_params['offerCode']
	TempSpeedConf = {}
	for step in steps:
		TempSpeedConf[step['amountNumber']] = {
			'priceName':    step['priceName'],
			'remainNumber': step['remainNumber'],
			'speedNumber':  step['speedNumber'],
			'speedString':  step['speedString'],
			'amountNumber': step['amountNumber'],
			'position':     step['position'],
			'amountString': step['amountString']
		}
	currentProduct = list_of_params['currentProduct']
	TempSpeedConf['current'] = {}
	TempSpeedConf['current']['priceName'] = currentProduct['priceName']
	TempSpeedConf['current']['amountNumber'] = currentProduct['amountNumber']
	TempSpeedConf['current']['speedNumber'] = currentProduct['speedNumber']
	TempSpeedConf['current']['speedString'] = currentProduct['speedString']
	TempSpeedConf['current']['amountString'] = currentProduct['amountString']
	TempSpeedConf['current']['remainNumber'] = TempSpeedConf[TempSpeedConf['current']['amountNumber']]['remainNumber']
	TempSpeedConf['current']['position'] = TempSpeedConf[TempSpeedConf['current']['amountNumber']]['position']
	currentProduct = TempSpeedConf['current']
	return steps, offerCode, currentProduct, TempSpeedConf

def CheckCurrent(price, page_speed):
	NewSpeedConf = SpeedConf[str(price)]
	list_of_params = GetListOfParams(page_speed)
	productId = list_of_params.keys()[0]
	list_of_params = list_of_params[productId]
	steps, offerCode, currentProduct, TempSpeedConf = GetSpeedConf(list_of_params)
	print currentProduct['amountNumber']
	print NewSpeedConf['amountNumber']
	print currentProduct




def set_speed(price):
	global SpeedConf 
	# print SpeedConf
	NewSpeedConf = SpeedConf[str(price)]

	data = {
		"product": Conf['productId'],
		"offerCode": Conf['offerCode'],
		"areOffersAvailable": "false",
		"period": SpeedConf['current']['remainNumber'],
		"status": "custom",
		"autoprolong": "1",
		"isSlot": "false",
		"finished": "false",
		"blocked": "false",
		"freeQuotaActive": "false",
		"pimpaPosition": NewSpeedConf['position'],
		"specialOffersExpanded": "true",
		"resourceId": "88310529",
		"currentDevice": "1",
		"username": "",
		"isDisablingAutoprolong": "false"
	}
	cookie = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
	urllib2.install_opener(opener)
	headers = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686; ru; \
                    rv:1.9.2.6) Gecko/20100628 Ubuntu/10.04 (lucid) \
                    Firefox/3.6.6",
                   "Accept": "text/html,application/xhtml+xml,application\
                   /xml;q=0.9,*/*;q=0.8"}
	params_speed = urllib.urlencode(data)
	request_speed = urllib2.Request("https://my.yota.ru/selfcare/devices/changeOffer", params_speed, headers)
	page_speed = urllib2.urlopen(request_speed).read()
	print page_speed
	CheckCurrent(price, page_speed)

main()
set_speed("800")