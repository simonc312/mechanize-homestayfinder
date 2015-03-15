import mechanize
import re
import logging
import sys
import cookielib

MSG = '''Hi, 
Enter you message body here
Best,
Anon'''
EMAIL = "spammer@gmail"

br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
# Follows refresh 0 but not hangs on refresh > 0
#br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_equiv(True)
#br.set_handle_gzip(True)
br.set_handle_robots(False)
br.set_debug_http(True)

br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6)Gecko/20070725 Firefox/2.0.0.6')]
logger = logging.getLogger("mechanize")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)
#Disclaimer These links were functioning as of 3/14/15 paths could have been modified since
homeurl = "http://homestayfinder.com/mobile/homestay-family-search.aspx"
response = br.open(homeurl)
country_list = br.links(url_regex="homestay-host-family")
for country in country_list:
	country_name = country.text.replace(' ','%20')
	response1 = br.follow_link(country)
	city_list = br.links(url_regex="homestay-host-family/"+country_name)
	for city in city_list:
		print city.text
		response1 = br.follow_link(city)
		host_list = br.links(url_regex="homestay-host-family")
		for host in host_list:
			response2 = br.follow_link(host)
			br.select_form(nr=0)
			br["Message"]=MSG
			br["Email"]=EMAIL
			br["ConfirmEmail"]=EMAIL
			response2 = br.submit()

