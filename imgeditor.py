import datetime, myspath as spath
import pyexiv2 as exiv
import sys

tdelta = datetime.datetime(2009,12,28,8,54) - datetime.datetime(2009,1,6,9,38)

print tdelta

firstpath = spath.path('/data/wendell/pix/Berlin/J-Belgium')
firstfile = firstpath.getfiles().next()
firstimg = exiv.Image(str(f))
firstimg.readMetadata()
n=0

key = 'Exif.Photo.DateTimeOriginal' # 'Exif.Image.DateTime'

for f in firstpath.getfiles():
    n += 1
    if f[-1][-4:].lower() != '.jpg':
        continue
    img = exiv.Image(str(f))
    img.readMetadata()
    odate = img[key]
    print odate, n
    if odate < datetime.datetime(2009,12,26):
        img[key] = odate + tdelta
        img.writeMetadata()
        print f[-1], img[key]
        sys.stdout.flush()
    
