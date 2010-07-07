import subprocess, time
import ssmtplib

## Open Postcast server in a new thread, and wait for it
##postcastthread = os.spawnl(os.P_NOWAIT, r'C:\Program Files\PostCast Server\postcastserver.exe', r'postcastserver.exe')
def prompt(prompt):
    return raw_input(prompt).strip()

fromaddr = "wws@dartmouth.edu"
toaddrs = "wws@dartmouth.edu"
msg = "smtp test"
username = 'W. Wendell Smith'
pw = prompt("password: ")

##fromaddr = prompt("From: ")
##toaddrs  = prompt("To: ").split()
##print "Enter message, end with ^D (Unix) or ^Z (Windows):"

# Add the From: and To: headers at the start!
##msg = ("From: %s\r\nTo: %s\r\n\r\n"
##       % (fromaddr, ", ".join(toaddrs)))
##while 1:
##    try:
##        line = raw_input()
##    except EOFError:
##        break
##    if not line:
##        break
##    msg = msg + line

print "Message length is " + repr(len(msg))

smtpserverin = ssmtplib.SMTP_SSL('mailhub.dartmouth.edu', 465)
print 'created smtpserverin'
smtpserverin.login(username, pw)
print 'logged in' 
smtpserverin.set_debuglevel(1)
print 'set debug level'
m = smtpserverin.sendmail(fromaddr, toaddrs, msg)
print 'sent mail:', m
smtpserverin.close()
print 'closed'
