from subprocess import Popen, PIPE

def raisewin(pid):
    wmproc = Popen("wmctrl -lp", shell=True,stdout=PIPE)
    wmoutb = wmproc.communicate()[0]
    wmout = wmoutb.decode()
    #print(type(wmout), "wmout:",wmout)
    wmoutlines = wmout.split('\n')
    #print(type(wmoutlines), "wmoutlines:",wmoutlines)
    for l in wmoutlines:
        fields = [f for f in l.split(" ") if f]
        #print(fields)
        if len(fields) < 3:
            continue
        print(fields[2],pid)
        if int(fields[2]) == int(pid):
            print("RUNNING, raising...", pid, fields[0])
            wmp = Popen("wmctrl -ia "+fields[0], shell=True)
            wmp.wait()