#!/usr/bin/env python2
import Quartz, json
wl = Quartz.CGWindowListCopyWindowInfo( Quartz.kCGWindowListOptionAll, Quartz.kCGNullWindowID)
wl = sorted(wl, key=lambda k: k.valueForKey_('kCGWindowOwnerPID'))
procs = []
for v in wl:
    if v.valueForKey_('kCGWindowOwnerName') in ['alacritty']:
        proc = {
          'name': v.valueForKey_('kCGWindowOwnerName'),
          'pid': v.valueForKey_('kCGWindowOwnerPID'),
          'window': v.valueForKey_('kCGWindowNumber'),
          'layer': v.valueForKey_('kCGWindowLayer'),
          'mem_usage': v.valueForKey_('kCGWindowMemoryUsage'),
          'location': dict(v.valueForKey_('kCGWindowBounds')),
        }
        if proc["location"]["Y"] > 0 and proc["location"]["X"] > 0  and proc["location"]["Width"] > 0  and proc["location"]["Height"] > 0: 
            pass
        if True:
            procs.append(proc)
        if False:
            print(json.dumps(dict(v)))
            print(v.valueForKey_('kCGWindowName'))
            print(v.valueForKey_('kCGWindowOwnerName'))

print(json.dumps(procs))
