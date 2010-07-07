#!/usr/bin/env python

"""Unpack a MIME message into a directory of files."""

import os
import sys
import email
import errno
import mimetypes
import mailbox

from optparse import OptionParser

def main():
    parser = OptionParser(usage="""\
Unpack attachments into a directory of files.

Usage: %prog [options] msgfile
""")
    parser.add_option('-d', '--directory',
                      type='string', action='store',
                      help="""Unpack the MIME message into the named
                      directory, which will be created if it doesn't already
                      exist.""")
    opts, args = parser.parse_args()
    if not opts.directory:
        parser.print_help()
        sys.exit(1)
    
    try:
        msgfile = args[0]
    except IndexError:
        parser.print_help()
        sys.exit(1)
    
    dir = opts.directory
    
    try:
        os.mkdir(dir)
    except OSError, e:
        # Ignore directory exists error
        if e.errno <> errno.EEXIST:
            raise


    fp = mailbox.mbox(msgfile)

    mcounter = 1
    for msg in fp:
        if 'porter' in msg.get('From','').lower():
            pcounter = 1
            for part in msg.walk():
                # multipart/* are just containers
                tp = part.get_content_maintype()
                if tp == 'multipart' or tp == 'text':
                    continue
                # Applications should really sanitize the given filename so that an
                # email message can't be used to overwrite important files
                fn = part.get_filename()
                if not fn:
                    try:
                        ext = mimetypes.guess_extension(part.get_type())
                    except AttributeError, e:
                        ext = None
                    if not ext:
                        # Use a generic bag-of-bits extension
                        ext = '.bin'
                    fn = 'part-%s' % ext
                filename = ('%02d-%02d-%s' % (mcounter, pcounter, fn))
                pcounter += 1
                f = open(os.path.join(dir, filename), 'wb')
                f.write(part.get_payload(decode=True))
                f.close()
            mcounter += 1

if __name__ == '__main__':
    main()
