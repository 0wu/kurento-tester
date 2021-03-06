#!/usr/bin/env python
import numpy

for i in range(4):
    timing_arr = numpy.load('timing%d.npz' % i)/1000;

    sender = timing_arr[:,0];
    receiver= timing_arr[:,1];
    delay = timing_arr[:,2];

    import matplotlib
    matplotlib.use('Agg')

    import pylab as p
    p.subplot(1,2,1);
    p.plot(sender, receiver,'.-')
    maxt = numpy.nanmax(sender)
    #p.axis([0,maxt,0,maxt]);
    p.ylim([0, maxt]);
    p.xlim([0, maxt]);
    p.title('receiver vs sender');
    p.xlabel('sender(s)')
    p.ylabel('receiver(s)')

    p.subplot(1,2,2);
    p.plot(sender,delay,'.-');
    p.xlabel('time(s)')
    p.ylabel('delay')

    p.title('delay')
    p.savefig("timing%d.png" % i)

    print((numpy.diff(receiver[400:])==0).sum())
