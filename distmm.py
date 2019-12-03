import mincemeat
from mincemeat import Protocol
import socket
import time
import sys
import logging
import logging.handlers
import multiprocessing
from multiprocessing import Pool, Process
import optparse
import collections
import fileiter
import pickle
from mincemeatpy.registry import Registry
import re
import string

MINIMUM_CLIENT_SLEEP_SECONDS = 1
DEFAULT_HOSTNAME = 'localhost'
DEFAULT_PASSWORD = 'changeme'
VERSION = '0.0.1'
DEFAULT_PORT = mincemeat.DEFAULT_PORT
READ_STEP = 500
DELIMITER = ' '


class Client(mincemeat.Client):

    def __init__(self, id=None):
        mincemeat.Client.__init__(self)
        self.key = ''
        self.input_file = ''
        self.command = b''
        if id is not None:
            self.id = id

    def validate(self, command, data):
        task_id, input_file = data
        self.key = ''
        self.command = command
        self.input_file = input_file
        if command == b'map':
            logging.info("Validate map task")
            self.key = Registry.get_instance().generate_key(self.mapfn, input_file)
        else:
            logging.info("Validate reduce task for %s" % input_file[0])
            # self.key = ''
            self.key = Registry.get_instance().generate_key_from_files(self.reducefn, input_file)
        self.send_command(b'keyurl', (task_id, (self.key, None)))

    def start_map(self, command, data):
        logging.info("Mapping %s at client %s" % (str(data[0]), self.id))
        file = dict(enumerate(fileiter.read(data[1], READ_STEP)))
        results = {}
        ''' running map func on assigned split '''
        for key, lines in file.items():
            self.call_mapfn(results, (key, lines))

        output_file = "%s_map_output" % data[0]
        pickle.dump(results, open(output_file, 'wb'))
        logging.info("generate map results at %s" % output_file)
        self.send_command(b'mapdone', (data[0], (self.key, [output_file])))

    def call_mapfn(self, results, data):
        for k, v in self.mapfn(data[0], data[1]):
            if k not in results:
                results[k] = []
            results[k].append(v)
        if self.collectfn:
            for k in results:
                results[k] = [self.collectfn(k, results[k])]
        ''' TODO: add partition function '''

    def start_reduce(self, command, data):
        logging.info("Reducing %s at client %s" % (str(data[0]), self.id))
        input_files = data[1]
        results = {}
        for file in input_files:
            input_file = pickle.load(open(file, 'rb'))
            for k, v in input_file.items():
                if k not in results:
                    results[k] = v
                results[k].extend(v)

        output_file = "%s_reduce_output" % data[0]
        file = open(output_file, 'w')
        for k, v in results.items():
            file.write("%s, %s\n" % (k, str(self.call_reducefn((k, v)))))
        file.close()
        self.send_command(b'reducedone', (data[0], (self.key, output_file)))

    def call_reducefn(self, data):
        return self.reducefn(data[0], data[1])

    def start_task(self, command, data):
        task_id, url = data
        if url is None:
            commands = {
                b'map': self.start_map,
                b'reduce': self.start_reduce
            }
            commands[self.command](self.command, (task_id, self.input_file))
        else:
            commands = {
                b'map': b'mapdone',
                b'reduce': b'reducedone'
            }
            if self.command == b'map':
                url = [url]
            self.send_command(commands[self.command], (task_id, (self.key, url)))
            
    def process_command(self, command, data=None):
        commands = {
            b'mapfn': self.set_mapfn,
            b'collectfn': self.set_collectfn,
            b'reducefn': self.set_reducefn,
            b'map': self.validate,
            b'reduce': self.validate,
            b'url': self.start_task
        }

        if command in commands:
            commands[command](command, data)
        else:
            Protocol.process_command(self, command, data)

    def run(self, options):

        client_sleep_seconds = None
        if options.client_sleep_seconds is not None:
            client_sleep_seconds = float(options.client_sleep_seconds)

        while True:
            try:
                if type(options.password) == str:
                    options.password = bytes(options.password, "utf-8")
                self.password = options.password
                self.conn(options.hostname, options.port)
                break
            except socket.error:
                exc_info = sys.exc_info()
                logging.debug("%s:{hostname=%s, port=%s}:%s",
                              exc_info[0],
                              options.hostname,
                              options.port,
                              exc_info[1])

                if client_sleep_seconds is None:
                    time.sleep(MINIMUM_CLIENT_SLEEP_SECONDS)
                    break
                else:
                    time.sleep(client_sleep_seconds)
                print('socket error')
                self.__init__()
            except KeyboardInterrupt:
                break
            except:
                exc_info = sys.exc_info()
                logging.exception("%s:%s", exc_info[0], exc_info[1])
                break


def run_client(queue=None, options=None):
    h = logging.handlers.QueueHandler(queue)
    root = logging.getLogger()
    root.addHandler(h)
    if options.verbose:
        root.setLevel(logging.INFO)
    if options.loud:
        root.setLevel(logging.DEBUG)
    if options.quiet:
        root.setLevel(logging.FATAL)
    while True:
        try:
            client = Client(0)
            client.run(options)
        except KeyboardInterrupt:
            break

        except:
            exc_info = sys.exc_info()
            logging.exception("%s:%s", exc_info[0], exc_info[1])
            break

        finally:
            print('end client')
            if not options.run_forever:
                break


def client_options_parser():
    parser = optparse.OptionParser(usage='%prog [options]', version='%%prog %s' % VERSION)
    parser.add_option('-p', '--password', dest='password', default=DEFAULT_PASSWORD, help='password')
    parser.add_option('-H', '--hostname', dest='hostname', default=DEFAULT_HOSTNAME, help='hostname')
    parser.add_option('-P', '--port', dest='port', type='int', default=DEFAULT_PORT, help='port')
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true')
    parser.add_option('-V', '--loud', dest='loud', action='store_true')
    parser.add_option('-q', '--quiet', dest='quiet', action='store_true')
    parser.add_option('-n', '--number_of_clients', dest='number_of_clients', default='1',
                      help='number of client processes')
    parser.add_option('-s', '--sleep', dest='client_sleep_seconds', default=None, help='client sleep seconds')
    parser.add_option('-t', '--client_timeout', dest='client_timeout_seconds', default=None,
                      help='worker timeout seconds')
    parser.add_option('-8', '--run_forever', dest='run_forever', action='store_true')
    parser.add_option('-i', '--input_filename', dest='input_filename', default='', help='input filename')

    return parser


def run_clients(queue, options=None):

    parser = client_options_parser()
    (default_options, args) = parser.parse_args([])

    if options is not None:
        try:
            default_options.__dict__.update(options.__dict__)
        except:
            default_options.__dict__.update(options)

    options = default_options

    number_of_clients = int(options.number_of_clients)

    pool = Pool(processes=number_of_clients)

    try:
        for i in range(number_of_clients):
            pool.apply_async(run_client, kwds=dict(options=options, queue=queue))

    except KeyboardInterrupt:
        exc_info = sys.exc_info()
        logging.debug("%s:%s", exc_info[0], exc_info[1])
        pool.terminate()
        pool.join()

    except:
        exc_info = sys.exc_info()
        logging.exception("%s:%s", exc_info[0], exc_info[1])
        pool.terminate()

    else:
        pool.close()

    finally:
        print('end pool')
        pool.join()


def map_default(k, v):
    yield k, v


def reduce_default(k, vs):
    if len(vs) == 1:
        return vs[0]
    else:
        return vs


class Server(mincemeat.Server):

    def __init__(self, datasource=None):
        mincemeat.Server.__init__(self)
        self.datasource = datasource
        self.mapfn = map_default
        self.reducefn = reduce_default

def run_server(options):

    parser = client_options_parser()
    (default_options, args) = parser.parse_args([])

    if options is not None:
        try:
            default_options.__dict__.update(options.__dict__)
        except:
            default_options.__dict__.update(options)

    options = default_options

    logging.debug(options)

    ''' initialize server data and assign map/reduce function '''
    datasource = None
    if isinstance(options.datasource, collections.Mapping):
        datasource = options.datasource
    else:
        datasource = dict(enumerate(options.datasource))

    server = None
    if 'server' in options.__dict__:
        server = options.server(datasource)
    else:
        server = Server(datasource)

    if 'mapfn' in options.__dict__:
        server.mapfn = options.mapfn

    if 'reducefn' in options.__dict__:
        server.reducefn = options.reducefn
    if 'cache' in options.__dict__:
        server.cache_on = options.cache
    return server.run_server(password=options.password)


def listener_configurer():
    root = logging.getLogger()
    h = logging.FileHandler('debug.log', 'a')
    f = logging.Formatter('%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
    h.setFormatter(f)
    root.addHandler(h)


def listener_process(queue, configurer):
    configurer()
    while True:
        try:
            record = queue.get()
            if record is None:  # We send this as a sentinel to tell the listener to quit.
                break
            logger = logging.getLogger(record.name)
            logger.handle(record)  # No level or filter logic applied - just do it!
        except Exception:
            import sys, traceback
            print('Whoops! Problem:', file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

if __name__ == '__main__':

    parser = client_options_parser()
    (options, args) = parser.parse_args()

    if options.verbose:
        logging.basicConfig(level=logging.INFO)
    if options.loud:
        logging.basicConfig(level=logging.DEBUG)
    if options.quiet:
        logging.basicConfig(level=logging.FATAL)

    if len(args) > 0:
        options.hostname = args[0]

    logging.debug('options: %s', options)
    queue = multiprocessing.Manager().Queue(-1)
    listener = Process(target=listener_process, args=(queue, listener_configurer))
    listener.start()
    # p = Process(target=run_clients, args=(queue, options))
    # p.start()
    # p.join()
    run_clients(queue, options)
    queue.put_nowait(None)
    listener.join()
    print('end')
