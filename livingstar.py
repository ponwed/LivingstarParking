# -*- coding: utf-8 -*-
#!/usr/bin/python
import smtplib
import conf
import re
from datetime import datetime
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from re import findall
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
        
def send_email(_msg, _to, _subject):
	msg = MIMEMultipart()
	msg['From'] = conf.fromaddr
	msg['To'] = _to
	msg['Subject'] = _subject
	 
	body = _msg
	msg.attach(MIMEText(body, 'plain'))
	 
	server = smtplib.SMTP(conf.mailsrv, 587)
	server.starttls()
	server.login(conf.fromaddr, conf.mailpwd)
	text = msg.as_string()
	server.sendmail(conf.fromaddr, _to, text)
	server.quit()

# Login to site
driver = webdriver.Chrome()
driver.get('https://minasidor.bostjarnan.se/mina-sidor/logga-in');
name_input = driver.find_element_by_name('ctl00$ctl01$DefaultSiteContentPlaceHolder1$Col2$LoginControl1$txtUserID')
pwd_input = driver.find_element_by_name('ctl00$ctl01$DefaultSiteContentPlaceHolder1$Col2$LoginControl1$txtPassword')
name_input.send_keys(conf.username)
pwd_input.send_keys(conf.password)
pwd_input.send_keys(Keys.RETURN)

# Get main div with the text we're after
content_div = driver.find_element_by_id('ctl00_ctl01_DefaultSiteContentPlaceHolder1_Col1_divRental')
string_content = content_div.text
driver.quit()

# Check for strings matching "parkering"
parking_matches = findall(r"[pP]ark.*", string_content)

# Check for strings matching "lägenheter"
match_pattern = re.compile(r"[lL]ägenheter.*", re.UNICODE)
apartment_matches = match_pattern.findall(string_content.encode('utf-8'))

# More than one match should indicate availible parking spaces
if len(parking_matches) > 1:
	send_email("Logga in och kolla tillgänglig parkering", conf.toaddr, "Ledig parkering!")
	
if len(apartment_matches) > 0:
	send_email("Logga in och kolla tillgänglig lägenhet", conf.toaddr2, "Ledig lägenhet!")
	
# Write a textfile for logging purposes
f = open("/home/pi/bin/livingstar_parking/last_run", "w")
f.write(datetime.now().strftime("%Y-%m-%d %H:%M"))
f.write(string_content.encode('utf-8'))
f.close()

