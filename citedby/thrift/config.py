import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1

bind = "127.0.0.1:11610"

daemon = True

pidfile = "citedby_thrift.pid"

loglevel = 'info'

worker_class = "thriftpy_gevent"

thrift_client_timeout = 10

thrift_transport_factory = "thriftpy.transport:TCyBufferedTransportFactory"

thrift_protocol_factory = "thriftpy.protocol:TCyBinaryProtocolFactory"