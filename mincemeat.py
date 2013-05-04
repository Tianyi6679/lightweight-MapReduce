#!/usr/bin/env python


################################################################################
# Copyright (c) 2010 Michael Fairley
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
################################################################################

import asynchat
import asyncore
import pickle
import hashlib
import hmac
import logging
import marshal
import optparse
import os
import random
import socket
import sys
import types
import binascii

VERSION = "0.1.2"


DEFAULT_PORT = 11235



class Protocol(asynchat.async_chat):
    def __init__(self, conn=None):
        if conn:
            asynchat.async_chat.__init__(self, conn)
        else:
            asynchat.async_chat.__init__(self)

        self.set_terminator(b"\n")
        self.buffer = []
        self.auth = None
        self.mid_command = False

    def collect_incoming_data(self, data):
        self.buffer.append(data)

    def send_command(self, command, data=None):
        if not b":" in command:
            command += b":"
        if data:
            pdata = pickle.dumps(data)
            command += bytes(str(len(pdata)), 'utf-8')
            logging.debug( "<- %s" % command)
            self.push(command + b"\n" + pdata)
        else:
            logging.debug( "<- %s" % command)
            self.push(command + b"\n")

    def found_terminator(self):
        if not self.auth == b"Done":
            command, data = (b''.join(self.buffer).split(b":", 1))
            self.process_unauthed_command(command, data)
        elif not self.mid_command:
            logging.debug("-> %s" % b''.join(self.buffer))
            command, length = (b''.join(self.buffer)).split(b":", 1)
            if command == b"challenge":
                self.process_command(command, length)
            elif length:
                self.set_terminator(int(length))
                self.mid_command = command
            else:
                self.process_command(command)
        else: # Read the data segment from the previous command
            if not self.auth == b"Done":
                logging.fatal("Recieved pickled data from unauthed source")
                sys.exit(1)
            data = pickle.loads(b''.join(self.buffer))
            self.set_terminator(b"\n")
            command = self.mid_command
            self.mid_command = None
            self.process_command(command, data)
        self.buffer = []

    def send_challenge(self):
        self.auth = binascii.hexlify(os.urandom(20))
        self.send_command(b":".join([b"challenge", self.auth]))

    def respond_to_challenge(self, command, data):
        mac = hmac.new(self.password, data, hashlib.sha1)
        self.send_command(b":".join([b"auth", binascii.hexlify(mac.digest())]))
        self.post_auth_init()

    def verify_auth(self, command, data):
        mac = hmac.new(self.password, self.auth, hashlib.sha1)
        if data == binascii.hexlify(mac.digest()):
            self.auth = b"Done"
            logging.info("Authenticated other end")
        else:
            self.handle_close()

    def process_command(self, command, data=None):
        commands = {
            b'challenge': self.respond_to_challenge,
            b'disconnect': lambda x, y: self.handle_close(),
            }

        if command in commands:
            commands[command](command, data)
        else:
            logging.critical("Unknown command received: %s" % (command,)) 
            self.handle_close()

    def process_unauthed_command(self, command, data=None):
        commands = {
            b'challenge': self.respond_to_challenge,
            b'auth': self.verify_auth,
            b'disconnect': lambda x, y: self.handle_close(),
            }

        if command in commands:
            commands[command](command, data)
        else:
            logging.critical("Unknown unauthed command received: %s" % (command,)) 
            self.handle_close()
        

class Client(Protocol):
    def __init__(self):
        Protocol.__init__(self)
        self.mapfn = self.reducefn = self.collectfn = None
        
    def conn(self, server, port):
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((server, port))
        asyncore.loop()

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def set_mapfn(self, command, mapfn):
        self.mapfn = types.FunctionType(marshal.loads(mapfn), globals(), 'mapfn')

    def set_collectfn(self, command, collectfn):
        self.collectfn = types.FunctionType(marshal.loads(collectfn), globals(), 'collectfn')

    def set_reducefn(self, command, reducefn):
        self.reducefn = types.FunctionType(marshal.loads(reducefn), globals(), 'reducefn')

    def call_mapfn(self, command, data):
        logging.info("Mapping %s" % str(data[0]))
        results = {}
        for k, v in self.mapfn(data[0], data[1]):
            if k not in results:
                results[k] = []
            results[k].append(v)
        if self.collectfn:
            for k in results:
                results[k] = [self.collectfn(k, results[k])]
        self.send_command(b'mapdone', (data[0], results))

    def call_reducefn(self, command, data):
        logging.info("Reducing %s" % str(data[0]))
        results = self.reducefn(data[0], data[1])
        self.send_command(b'reducedone', (data[0], results))
        
    def process_command(self, command, data=None):
        commands = {
            b'mapfn': self.set_mapfn,
            b'collectfn': self.set_collectfn,
            b'reducefn': self.set_reducefn,
            b'map': self.call_mapfn,
            b'reduce': self.call_reducefn,
            }

        if command in commands:
            commands[command](command, data)
        else:
            Protocol.process_command(self, command, data)

    def post_auth_init(self):
        if not self.auth:
            self.send_challenge()


class Server(asyncore.dispatcher, object):
    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.mapfn = None
        self.reducefn = None
        self.collectfn = None
        self.datasource = None
        self.password = None

    def run_server(self, password=b"", port=DEFAULT_PORT):
        if (type(password) == str):
            password = bytes(password, "utf-8")
        self.password = password
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(("", port))
        self.listen(1)
        try:
            asyncore.loop()
        except:
            self.close_all()
            raise
        
        return self.taskmanager.results

    # def handle_accepted(self):
    def handle_accepted(self, conn, addr):
        # conn, addr = self.accept()
        sc = ServerChannel(conn, self)
        sc.password = self.password

    def handle_close(self):
        self.close()

    def set_datasource(self, ds):
        self._datasource = ds
        self.taskmanager = TaskManager(self._datasource, self)
    
    def get_datasource(self):
        return self._datasource

    datasource = property(get_datasource, set_datasource)


class ServerChannel(Protocol):
    def __init__(self, conn, server):
        Protocol.__init__(self, conn)
        self.server = server

        self.start_auth()

    def handle_close(self):
        logging.info("Client disconnected")
        self.close()

    def start_auth(self):
        self.send_challenge()

    def start_new_task(self):
        command, data = self.server.taskmanager.next_task(self)
        if command == None:
            return
        self.send_command(command, data)

    def map_done(self, command, data):
        self.server.taskmanager.map_done(data)
        self.start_new_task()

    def reduce_done(self, command, data):
        self.server.taskmanager.reduce_done(data)
        self.start_new_task()

    def process_command(self, command, data=None):
        commands = {
            b'mapdone': self.map_done,
            b'reducedone': self.reduce_done,
            }

        if command in commands:
            commands[command](command, data)
        else:
            Protocol.process_command(self, command, data)

    def post_auth_init(self):
        if self.server.mapfn:
            self.send_command(b'mapfn', marshal.dumps(self.server.mapfn.__code__))
        if self.server.reducefn:
            self.send_command(b'reducefn', marshal.dumps(self.server.reducefn.__code__))
        if self.server.collectfn:
            self.send_command(b'collectfn', marshal.dumps(self.server.collectfn.__code__))
        self.start_new_task()
    
class TaskManager:
    START = 0
    MAPPING = 1
    REDUCING = 2
    FINISHED = 3

    def __init__(self, datasource, server):
        self.datasource = datasource
        self.server = server
        self.state = TaskManager.START

    def next_task(self, channel):
        if self.state == TaskManager.START:
            self.map_iter = iter(self.datasource)
            self.working_maps = {}
            self.map_results = {}
            #self.waiting_for_maps = []
            self.state = TaskManager.MAPPING
        if self.state == TaskManager.MAPPING:
            try:
                map_key = next(self.map_iter)
                map_item = map_key, self.datasource[map_key]
                self.working_maps[map_item[0]] = map_item[1]
                return (b'map', map_item)
            except StopIteration:
                if len(self.working_maps) > 0:
                    key = random.choice(list(self.working_maps.keys()))
                    return (b'map', (key, self.working_maps[key]))
                self.state = TaskManager.REDUCING
                self.reduce_iter = iter(self.map_results.items())
                self.working_reduces = {}
                self.results = {}
        if self.state == TaskManager.REDUCING:
            try:
                reduce_item = next(self.reduce_iter)
                self.working_reduces[reduce_item[0]] = reduce_item[1]
                return (b'reduce', reduce_item)
            except StopIteration:
                if len(self.working_reduces) > 0:
                    key = random.choice(list(self.working_reduces.keys()))
                    return (b'reduce', (key, self.working_reduces[key]))
                self.state = TaskManager.FINISHED
        if self.state == TaskManager.FINISHED:
            self.server.handle_close()
            return (b'disconnect', None)
    
    def map_done(self, data):
        # Don't use the results if they've already been counted
        if not data[0] in self.working_maps:
            return

        for (key, values) in data[1].items():
            if key not in self.map_results:
                self.map_results[key] = []
            self.map_results[key].extend(values)
        del self.working_maps[data[0]]
                                
    def reduce_done(self, data):
        # Don't use the results if they've already been counted
        if not data[0] in self.working_reduces:
            return

        self.results[data[0]] = data[1]
        del self.working_reduces[data[0]]

def run_client():
    parser = optparse.OptionParser(usage="%prog [options]", version="%%prog %s"%VERSION)
    parser.add_option("-p", "--password", dest="password", default="", help="password")
    parser.add_option("-P", "--port", dest="port", type="int", default=DEFAULT_PORT, help="port")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true")
    parser.add_option("-V", "--loud", dest="loud", action="store_true")

    (options, args) = parser.parse_args()
                      
    if options.verbose:
        logging.basicConfig(level=logging.INFO)
    if options.loud:
        logging.basicConfig(level=logging.DEBUG)

    client = Client()
    if (type(options.password) == str):
        options.password = bytes(options.password, "utf-8")
    client.password = options.password
    client.conn(args[0], options.port)
                      

if __name__ == '__main__':
    run_client()
