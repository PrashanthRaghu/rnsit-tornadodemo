from tornado import websocket, web, ioloop
from connectionManager import connection_manager

class ChatHandler(websocket.WebSocketHandler):
	def check_origin(self, origin):
		return True

	def open(self):
		print "connection opened by client", self

	def on_close(self):
		print "closed"
	
	def on_message(self, message):
		messageText = message.split(",")

		if messageText[0] == "1":
			userid = messageText[0]
			connection_manager.connections[messageText[1]] = self
		elif messageText[0] == "2":
			to_send_id = messageText[1]
			to_send_socket = connection_manager.connections[messageText[1]]
			to_send_socket.write_message(messageText[2])

app = web.Application([
    (r'/ws', ChatHandler),
])

if __name__ == "__main__":
	app.listen(8090)
	print "Websocket server started on port 8090"
	ioloop.IOLoop.instance().start()