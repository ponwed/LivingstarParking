import smtplib
import conf
from datetime import datetime
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from re import findall
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
        
def send_email(_msg):
	msg = MIMEMultipart()
	msg['From'] = conf.fromaddr
	msg['To'] = conf.toaddr
	msg['Subject'] = "Parkeringsrapport"
	 
	body = _msg
	msg.attach(MIMEText(body, 'plain'))
	 
	server = smtplib.SMTP(conf.mailsrv, 587)
	server.starttls()
	server.login(conf.fromaddr, conf.mailpwd)
	text = msg.as_string()
	server.sendmail(conf.fromaddr, conf.toaddr, text)
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
matches = findall(r"[pP]ark.*", string_content)

# More than one match should indicate availible parking spaces
if len(matches) > 1:
	send_email("Logga in och kolla tillganglig parkering")
	
# Write a textfile for logging purposes
f = open("last_run", "w")
f.write(datetime.now().strftime("%Y-%m-%d %H:%M"))
f.close()

