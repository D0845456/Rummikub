# -!- coding:utf-8 -!-
'''
Created on 2021年~12月11日
@author: Johnson
'''

from game import Game
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
PORT = 8888


class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass
# end of class
def main():
    obj = Game()
    server = ThreadXMLRPCServer(('localhost',PORT))
    server.register_instance(obj)
    print('Listen on port %d' % PORT)
    try:
        print('Use Control-C to exit!')
        server.serve_forever()
    except KeyboardInterrupt:
        print('Server exit')
# end of main
    
if __name__ == '__main__':
    main()
