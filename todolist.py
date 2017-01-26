import tornado.ioloop
import tornado.web
import dbFactory
import redisFactory
from listitemhandler_db import ListItemHandler as ListItemHandler

def make_app():
    return tornado.web.Application(handlers = [
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': './static'}),
            (r'/item', ListItemHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    print "Server started on port 8888. Waiting for requests"
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()