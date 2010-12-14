# default config
import os

usereadline = True
usecolor = True
usecolorprompts = True
editor = os.environ.get('EDITOR', 'vim')
savefile = '%s/.jpython/saves'  % os.environ["HOME"]
aliases = {'ls':'ls --color=auto'}
namespace = {}
importall = []
importlist = []
histfile="%s/.pyhistory" % os.environ["HOME"]
