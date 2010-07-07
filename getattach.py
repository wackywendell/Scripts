

def getattach(msg):
    for part in msg.walk():
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
        yield (tp, fn, part.get_payload(decode=True))
