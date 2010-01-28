#!/usr/bin/env python

# Server PlaniFI
# Alberto Bertogli (albertogli@telpin.com.ar)
#
# Exporta por XML-RPC la funcionalidad necesaria para el PlaniFI de forma
# centralizada.


import SimpleXMLRPCServer
import signal

import config
import for_export
import session


need_check = 0
def handle_sigalrm(signum, frame):
    #session.check_sessions()
    need_check = 1
    signal.alarm(10)

server = SimpleXMLRPCServer.SimpleXMLRPCServer((config.addr, config.port))
for i in for_export.list:
    server.register_function(i)

signal.signal(signal.SIGALRM, handle_sigalrm)
signal.alarm(10)

while 1:
    try:
        server.handle_request()
        if need_check:
            session.check_sessions()
            need_check = 0
    except:
        pass

