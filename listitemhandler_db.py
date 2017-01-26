import tornado.ioloop
import tornado.web
import dbFactory
import redisFactory
import counter
import constants
import json
from dbFactory import TodoItem as TodoItem

class ListItemHandler(tornado.web.RequestHandler):
    session = dbFactory.initDbSession()

    def get(self):
        s = self.session()
        itemId = self.get_argument(constants.ID_FIELD_NAME, constants.ID_FIELD_DEFAULT)

        itemsOp = []

        if itemId == "-1":
            items = s.query(TodoItem).all()

            for item in items:
                i = {constants.ID_FIELD_NAME: item.id, constants.ITEM_FIELD_NAME: item.item}
                itemsOp.append(i)

            self.write(json.dumps(itemsOp))
        else:
            item = s.query(TodoItem).filter_by(id = itemId).first()
            if item != None:
                i = {constants.ID_FIELD_NAME: item.id, constants.ITEM_FIELD_NAME: item.item}
                self.write(json.dumps(i))
            else:
                self.write({})
        
    def post(self):
    	self.write("-1")

    def put(self):
        s = self.session()
        itemData = self.get_argument(constants.ITEM_FIELD_NAME, constants.ITEM_FIELD_DEFAULT)
        todo_item = TodoItem()
        todo_item.item = itemData
        s.add(todo_item)
        s.commit()
        item = {constants.ID_FIELD_NAME: todo_item.id, constants.ITEM_FIELD_NAME: itemData}
        self.write(item)

    def delete(self):
          s = self.session()
          itemId = self.get_argument(constants.ID_FIELD_NAME, constants.ID_FIELD_DEFAULT)
          item = s.query(TodoItem).filter_by(id = itemId).first()

          if item != None:
              s.delete(item)
              s.commit()
              self.write("1")
          else:
              self.write("-1")  
