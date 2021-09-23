# http requests
import requests

# Web Scraping
from bs4 import BeautifulSoup

# Send the mail
import smtplib

# Email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# import datetime
import datetime
now = datetime.datetime.now()

# Email content placeholder

content = ""


# Extracting Hacker News Stories

def extract_news(url):
    print(f"Extracting Hacker News Stories......")
    cnt = ""
    cnt += ('<b>Hacker News Top Stories:</b>\n' + "<br>" + "-"*50+"<br>")
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    for i, tag in enumerate(soup.find_all('td', attrs={'class': 'title', 'valign': ''})):
        cnt += ((str(i+1)+' :: ' + tag.text + "\n" + '<br>')
                if tag.text != "More" else "")

        # print(tag.prettify)  find all(('span),attrs={'class':'sitestr'}))
    return(cnt)


cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>-------<br>')
content += ('<br><br>End of Message')


# Send the email

print('Composing Email...')


# Update your email details

SERVER = 'smtp.gmail.com'                  # Your smtp Server
PORT = 587                                 # Your Port Number
FROM = ''                                  # Your email id
TO = ""                                   # to email ids or can be a list
PASS = ""                                  # Your email id password


# fp = open(file_name, 'rb')
# Create a text/plain message
# msg = MIMEText('')

msg = MIMEMultipart()

msg['Subject'] = 'Top News Stories HN [Automated Email]' + \
    " " + str(now.day) + "-" + str(now.month)+"-"+str(now.year)
msg['Form'] = FROM
msg["To"] = TO


msg.attach(MIMEText(content, 'html'))
# fp.close()

print('Initiating Server...')

server = smtplib.SMTP(SERVER, PORT)
server.set_debuglevel(1)
server.ehlo()
server.starttls()

server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent...')

server.quit()
