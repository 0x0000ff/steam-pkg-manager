#!/usr/bin/python3
import vdf

t = vdf.load(open('template.vdf'))
d = vdf.binary_load(open('shortcuts.vdf', mode='br'))
print(d.items())
if ('shortcuts' not in d or len(d['shortcuts']) < 1 ):
    b=vdf.binary_dump(t, open('shortcuts.vdf', mode='bw'))
else:
    e = t['shortcuts']['0']
    d['shortcuts'][str(len(d['shortcuts']))] = e
    print (d.items())
    print (len(d['shortcuts']))
    b=vdf.binary_dump(d, open('shortcuts.vdf', mode='bw'))
#len doesn't count from zero    
#install to .opt or .var
#move artwork to grid folder. Make sure it is named apropriately
#Figure out assignment of appid numbers