package main

import (
	// "bytes"
	// "encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"net"
	"net/http"
	"time"
)

var (
	Conf     Config
	UrlLogin = "https://login.yota.ru/UI/Login?goto=https://my.yota.ru:443/selfcare/loginSuccess&gotoOnFail=https://my.yota.ru:443/selfcare/loginError&org=customer&ForceAuth=true&old-token=%s&IDToken2=%s&IDToken1=6035498867"
)

func httpDial(network, addr string) (net.Conn, error) {
	return net.DialTimeout(network, addr, timeout)
}

var transport = http.Transport{Dial: httpDial, DisableKeepAlives: true}
var timeout = time.Duration(500) * time.Millisecond
var http_client = http.Client{Transport: &transport, Timeout: timeout}

func main() {
	flag.Parse()
	conf_file := flag.String("conf", "settings.conf", "")
	Conf = Config{}
	Conf.Configuration_filename = *conf_file
	Conf.Configuration = map[string]string{}

	UserName := Conf.GetConfString("UserName", "")
	UserPass := Conf.GetConfString("UserPass", "")
	UrlLogin = fmt.Sprintf(UrlLogin, UserName, UserPass)

	// payloads := map[string]interface{}{
	// 	"goto":       "https://my.yota.ru:443/selfcare/loginSuccess",
	// 	"gotoOnFail": "https://my.yota.ru:443/selfcare/loginError",
	// 	"org":        "customer",
	// 	"ForceAuth":  true,
	// 	"old-token":  UserName,
	// 	"IDToken2":   UserPass,
	// 	"IDToken1":   "6035498867",
	// }
	
	response, err := http_client.Get(string(UrlLogin))
	if err != nil {
		fmt.Println("ERR RESP = ", err)
		return
	}
	defer response.Body.Close()
	body, _ := ioutil.ReadAll(response.Body)
	fmt.Println("BODY = ", body)
}
