import tornado.ioloop
import tornado.web
import dbFactory
import redisFactory
import counter
import constants
import json

class ListItemHandler(tornado.web.RequestHandler):
    dbFactory.initDbSession()
    redisConnection = redisFactory.getRedisInstance()

    def get(self):
        itemId = self.get_argument(constants.ID_FIELD_NAME, constants.ID_FIELD_DEFAULT)

        items = []
        if itemId == "-1":
            idList = self.redisConnection.lrange("item_ids", 0, -1)

            for iD in idList:
                item = self.redisConnection.hgetall(iD)
                items.append(item)

            self.write(json.dumps(items))
        else:
            items = self.redisConnection.hgetall(itemId)
            self.write(items)
        

    def post(self):
    	itemData = self.get_argument(constants.ITEM_FIELD_NAME, constants.ITEM_FIELD_DEFAULT)
        itemId = self.get_argument(constants.ID_FIELD_NAME, constants.ID_FIELD_DEFAULT)
        item = {constants.ID_FIELD_NAME: itemId, constants.ITEM_FIELD_NAME: itemData}
        self.redisConnection.hmset(itemId, item)
        self.write(item)

    def put(self):
        counter.list_counter.incrCounter()
    	itemData = self.get_argument(constants.ITEM_FIELD_NAME, constants.ITEM_FIELD_DEFAULT)
        item = {constants.ID_FIELD_NAME: counter.list_counter.count, constants.ITEM_FIELD_NAME: itemData}
        self.redisConnection.hmset(counter.list_counter.count, item)
        self.redisConnection.rpush("item_ids", counter.list_counter.count)
        self.write(item)

    def delete(self):
        itemData = self.get_argument(constants.ID_FIELD_NAME, constants.ID_FIELD_DEFAULT)
        self.redisConnection.hdel(itemData, [constants.ID_FIELD_NAME, constants.ITEM_FIELD_NAME])
        self.redisConnection.lrem("item_ids", 0, itemData)
        self.write("1")    	
