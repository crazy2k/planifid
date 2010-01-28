#!/usr/bin/env python

# PlaniFI server
# ==============
# Exports the necessary functionality for PlaniFI in a centralized way
# via XML-RPC.

import SimpleXMLRPCServer
import signal

import config
import for_export
import session


need_check = 0
def handle_sigalrm(signum, frame):
    need_check = 1
    signal.alarm(10)

server = SimpleXMLRPCServer.SimpleXMLRPCServer((config.addr, config.port))

for f in for_export.list:
    server.register_function(f)

signal.signal(signal.SIGALRM, handle_sigalrm)
signal.alarm(10)

while True:
    try:
        server.handle_request()
        if need_check:
            session.check_sessions()
            need_check = 0
    except KeyboardInterrupt as e:
        break
    except:
        pass

