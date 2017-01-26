import tornado.ioloop
import tornado.web
import dbFactory
import redisFactory
import counter
import constants
import json
from dbFactory import TodoItem

class ListItemHandler(tornado.web.RequestHandler):
    session = dbFactory.initDbSession()
    redisConnection = redisFactory.getRedisInstance()

    def get(self):
        s = self.session()
        itemId = self.get_argument(constants.ID_FIELD_NAME, constants.ID_FIELD_DEFAULT)

        url = self.request.uri

        response = self.redisConnection.get(url)

        if response == None:
            items = []
            if itemId == "-1":
                idList = self.redisConnection.lrange("item_ids", 0, -1)

                for iD in idList:
                    item = self.redisConnection.hgetall(iD)

                    if item == {}:
                        print "From DB"
                        item = s.query(TodoItem).filter_by(id = itemId).first()
                        i = {constants.ID_FIELD_NAME: item.id, constants.ITEM_FIELD_NAME: item.item}
                        self.redisConnection.hmset(item.id, i)
                        item = i
                    else:
                        print "From Cache"

                    items.append(item)

                result = json.dumps(items)
                self.redisConnection.setex(url, 30, result)
                self.write(result)
            else:
                items = self.redisConnection.hgetall(itemId)

                if items == {}:
                    print "from DB"
                    item = s.query(TodoItem).filter_by(id = itemId).first()
                    i = {constants.ID_FIELD_NAME: item.id, constants.ITEM_FIELD_NAME: item.item}
                    self.redisConnection.hmset(item.id, i)
                    self.write(i)
                    self.redisConnection.setex(url, 30, i)
                else:
                    print "from cache"
                    self.write(items)
                    self.redisConnection.setex(url, 30, items)
        else:
            print "From url cache"
            self.write(response)
        

    def post(self):
        itemData = self.get_argument(constants.ITEM_FIELD_NAME, constants.ITEM_FIELD_DEFAULT)
        itemId = self.get_argument(constants.ID_FIELD_NAME, constants.ID_FIELD_DEFAULT)
        
        s = self.session()
        item = s.query(TodoItem).filter_by(id = itemId).first()

        if item != None:
            item.item = itemData
            s.add(item)
            s.commit()
            i = {constants.ID_FIELD_NAME: item.id, constants.ITEM_FIELD_NAME: item.item}
            self.redisConnection.hmset(itemId, i)
            self.write(i)
        else:
            self.write("-1")


    def put(self):
        s = self.session()
        itemData = self.get_argument(constants.ITEM_FIELD_NAME, constants.ITEM_FIELD_DEFAULT)
        todo_item = TodoItem()
        todo_item.item = itemData
        s.add(todo_item)
        s.commit()
        item = {constants.ID_FIELD_NAME: todo_item.id, constants.ITEM_FIELD_NAME: todo_item.item}
        self.redisConnection.hmset(todo_item.id, item)
        self.redisConnection.rpush("item_ids", todo_item.id)
        self.write(item)

    def delete(self):
        s = self.session()
        itemId = self.get_argument(constants.ID_FIELD_NAME, constants.ID_FIELD_DEFAULT)

        item = s.query(TodoItem).filter_by(id = itemId).first()

        if item != None:
            self.redisConnection.hdel(item.id, [constants.ID_FIELD_NAME, constants.ITEM_FIELD_NAME])
            self.redisConnection.lrem("item_ids", 1, item.id)
            s.delete(item)
            self.write("1")     
