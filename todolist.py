import tornado.ioloop
import tornado.web
import dbFactory
import redisFactory
from listitemhandler_redis import ListItemHandler as ListItemHandler

import sys
def make_app():
    return tornado.web.Application(handlers = [
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': './static'}),
            (r'/item', ListItemHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    port = int(sys.argv[1])
    print "Server started on port", port, ". Waiting for requests"
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()