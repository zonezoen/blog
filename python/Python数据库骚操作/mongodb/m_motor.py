import pymongo
import motor.motor_asyncio
import pprint
# 普通连接
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
# 副本集连接
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://host1,host2/?replicaSet=my-replicaset-name')
# 密码连接
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://username:password@localhost:27017/dbname')
# 获取数据库
db = client.zfdb
# db = client['zfdb']
# 获取 collection
collection = db.test
# collection = db['test']

import asyncio

loop = asyncio.get_event_loop()


# 增
# async def do_insert():
#      document = {'name': 'zone','sex':'boy'}
#      result = await db.test_collection.insert_one(document)
#      print('result %s' % repr(result.inserted_id))
#
# loop.run_until_complete(do_insert())


# 批量增加
# async def do_insert():
#     result = await db.test_collection.insert_many(
#         [{'name': i, 'sex': str(i + 2)} for i in range(20)])
#     print('inserted %d docs' % (len(result.inserted_ids),))
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(do_insert())

# 查找单条记录
# async def do_find_one():
#     document = await db.test_collection.find_one({'name': 'zone'})
#     pprint.pprint(document)
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(do_find_one())



print()
# 查找多条记录
# async def do_find():
#     cursor = db.test_collection.find({'name': {'$lt': 5}}).sort('i')
#     for document in await cursor.to_list(length=100):
#         pprint.pprint(document)
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(do_find())



# 查找多条记录，按一条一条返回
# async def do_find():
#     c = db.test_collection
#     async for document in c.find({'name': {'$lt': 2}}):
#         pprint.pprint(document)
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(do_find())


# 添加筛选条件，排序、跳过、限制返回结果数
# async def do_find():
#     cursor = db.test_collection.find({'name': {'$lt': 4}})
#     # Modify the query before iterating
#     cursor.sort('name', -1).skip(1).limit(2)
#     async for document in cursor:
#         pprint.pprint(document)
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(do_find())


# 统计
# async def do_count():
#     n = await db.test_collection.count_documents({})
#     print('%s documents in collection' % n)
#     n = await db.test_collection.count_documents({'name': {'$gt': 1000}})
#     print('%s documents where i > 1000' % n)
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(do_count())


# 替换，除了 id 以外，其他都完全替代掉
# async def do_replace():
#     coll = db.test_collection
#     old_document = await coll.find_one({'name': 'zone'})
#     print('found document: %s' % pprint.pformat(old_document))
#     _id = old_document['_id']
#     result = await coll.replace_one({'_id': _id}, {'sex': 'hanson boy'})
#     print('replaced %s document' % result.modified_count)
#     new_document = await coll.find_one({'_id': _id})
#     print('document is now %s' % pprint.pformat(new_document))
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(do_replace())


# 更新
# async def do_update():
#     coll = db.test_collection
#     result = await coll.update_one({'name': 0}, {'$set': {'sex': 'girl'}})
#     print('更新条数： %s ' % result.modified_count)
#     new_document = await coll.find_one({'name': 0})
#     print('更新结果为： %s' % pprint.pformat(new_document))
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(do_update())


# 删除
# async def do_delete_many():
#     coll = db.test_collection
#     n = await coll.count_documents({})
#     print('删除前有 %s 条数据' % n)
#     result = await db.test_collection.delete_many({'name': {'$gte': 10}})
#     print('删除后 %s ' % (await coll.count_documents({})))
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(do_delete_many())





