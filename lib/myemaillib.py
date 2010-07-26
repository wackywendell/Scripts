import imaplib, smtplib
import email
from contextlib import contextmanager


service = 'GMail'
username = 'wackywendell'

keyring = 'default'
pword = ''

#import gobject, gnomekeyring
#gobject.set_application_name('myemaillib')
#keyids = gnomekeyring.list_item_ids_sync('default')
if False:
    for i in keyids:
        attrs = gnomekeyring.item_get_attributes_sync(keyring,i)
        #print i, attrs
        if ('service' in attrs and 'username' in attrs and
            attrs['service'] == service and attrs['username'] == username):
            print 'FOUND'
            itm = gnomekeyring.item_get_info_sync(keyring, i)
            print itm.get_display_name()
            pword = itm.get_secret()
            print len(pword)

def getimap(uname=username, password=pword):
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(uname, password)
    imap.select('INBOX')
    return imap

def getheader(imap, num):
    response, retval = imap.fetch(num,'(BODY.PEEK[HEADER])')
    msg = retval[0][1]
    msg = email.message_from_string(msg)
    return msg

def getsmtp(uname=username, password=pword):
    smtp = smtplib.SMTP_SSL('smtp.gmail.com',465)
    smtp.login(uname, password)
    return smtp
    
@contextmanager
def mysmtp(uname=username, password=pword):
    smtp = smtplib.SMTP_SSL('smtp.gmail.com',465)
    smtp.login(uname, password)
    yield smtp
    smtp.quit()


#del pword
#print 'password length:', len(pword)
