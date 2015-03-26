
bind = "127.0.0.1:11610"

worker_class = "thriftpy_gevent"

thrift_client_timeout = 5

thrift_transport_factory = "thriftpy.protocol:TCyBinaryProtocolFactory"

thrift_protocol_factory = "thriftpy.transport:TCyBufferedTransportFactory"