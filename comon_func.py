#!/usr/bin/python
#coding=utf-8

import errno


def timeout(p):
        print "enter into timeout"
        if p.poll() is None:
            try:
                p.kill()
                print 'Error: process taking too long to complete--terminating'
            except OSError as e:
                if e.errno != errno.ESRCH:
                    raise



