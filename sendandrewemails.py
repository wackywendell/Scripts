from myemaillib import getimap, getheader
import dateutil.parser as dateparser

imap = getimap()

msgnums = []
answer, result = imap.search(None,'FROM','PINKHAM')
if answer == 'OK' and result != ['']:
	msgnums.extend(result[0].split(' '))
answer, result = imap.search(None,'FROM','WIRESAP')
if answer == 'OK' and result != ['']:
	msgnums.extend(result[0].split(' '))

hdrs = [getheader(imap,n) for n in msgnums]

dates = [dateparser.parse(h['Date']) for h in hdrs]

#imap.close()
#imap.logout()
