import gobject, gnomekeyring
import imaplib
import email
gobject.set_application_name('myemaillib')

service = 'GMail'
username = 'wackywendell'

keyring = 'default'
keyids = gnomekeyring.list_item_ids_sync('default')
pword = ''
for i in keyids:
	attrs = gnomekeyring.item_get_attributes_sync(keyring,i)
#	print attrs
	if ('service' in attrs and 'username' in attrs and
		attrs['service'] == service and attrs['username'] == username):
#		print 'FOUND'
		itm = gnomekeyring.item_get_info_sync(keyring, i)
#		print itm.get_display_name()
		pword = itm.get_secret()
#		print len(pword)

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

del pword
#print 'password length:', len(pword)
