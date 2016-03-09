# BeautifulSoup for getting the html
from bs4 import BeautifulSoup as bs
# urllib2 for reading the page
import urllib2
# time for the delay
import time
# smtplib for sending the email
import smtplib
# MIMEText for constructing the message
from email.mime.text import MIMEText
# getpass for getting the password
import getpass

# get search query and emails
search_query = raw_input('Enter search term: ')
send_mail = raw_input('Enter sender address: ')
send_pass = getpass.getpass('Enter sender password (hidden) ')
rec_mail = raw_input('Enter recipient address: ')

# connect to the email server
s = smtplib.SMTP('smtp.gmail.com', port=587)
s.starttls()
s.ehlo()
# print connection status
# script will stop if connection is unsuccessful
print s.login(send_mail, send_pass)

# create the url
url = 'http://www.thegradcafe.com/survey/index.php?q=' + search_query.replace(' ', '+')
# headers required to bypass stuff to get the html
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'none','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}

# the result number of the most recent post
scb_old = 0

# continue forever
while (1):
    # request the page using headers
    req = urllib2.Request(url, headers=hdr)
    # open the page
    page = urllib2.urlopen(req)
    # throw the page into BeautifulSoup to get the html
    soup = bs(page.read(), 'html.parser')
    # print soup

    # find the tag of the most recent result
    new_result = soup.find('tr', {'class':'row0'})
    # print new_result
    # turn the new result block into a string for parsing
    new_res_str = str(new_result)

    # get the posting number of the newest result
    scb_str = new_res_str[new_res_str.find('showControlsBox'):-1]
    scb_num = scb_str[scb_str.find(',')+1:scb_str.find(')')]
    # get the result status (not implemented)
    res = scb_str[0:scb_str.find('span')]
    
    # if this is the first time through the loop, init scb_old
    if (scb_old == 0):
        scb_old = scb_num
        continue
        
    # check if the result is new
    # if new, send the email
    if (scb_old != scb_num):
        msg = MIMEText(scb_num)
        msg['Subject'] = 'thegradcafe.com: New admission result for search term \"' + search_query + '\"'
        msg['From'] = send_mail
        msg['To'] = rec_mail
        print 'Sending mail...'
        s.sendmail(send_mail, [rec_mail], msg.as_string())
        print 'Sent mail.'
    # otherwise let the user know that it's still checking
    else:
        print 'Checking...'
        
    # update scb_old
    scb_old = scb_num
    # sleep for a bit
    time.sleep(60)