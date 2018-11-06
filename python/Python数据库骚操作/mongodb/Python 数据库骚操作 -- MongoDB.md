![zone7](https://github.com/zonezoen/blog/blob/master/img/zone_qrcode.jpg)
- 前言
- MongoDB GUI 工具
- PyMongo（同步）
- Motor（异步）
- 后记
## 前言
最近这几天准备介绍一下 Python 与三大数据库的使用，这是第一篇，首先来介绍 MongoDB 吧，，走起！！
## MongoDB GUI 工具
首先介绍一款 MongoDB 的 GUI 工具 Robo 3T，初学 MongoDB 用这个来查看数据真的很爽。可以即时看到数据的增删改查，不用操作命令行来查看。
![](https://upload-images.jianshu.io/upload_images/2470773-c894c48f7b021cec.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![操作界面图](https://upload-images.jianshu.io/upload_images/2470773-9a90f9c518379317.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## PyMongo（同步）
可能大家都对 PyMongo 比较熟悉了，这里就简单介绍它的增删改查等操作。
#### 连接
```
# 普通连接
client = MongoClient('localhost', 27017)
client = MongoClient('mongodb://localhost:27017/')
#
# 密码连接
client = MongoClient('mongodb://username:password@localhost:27017/dbname')
db = client.zfdb
# db = client['zfdb']

test = db.test
```
#### 增
```
# 增加一条记录
person = {'name': 'zone','sex':'boy'}
person_id = test.insert_one(person).inserted_id
print(person_id)
```
```
# 批量插入
persons = [{'name': 'zone', 'sex': 'boy'}, {'name': 'zone1', 'sex': 'boy1'}]
result = test.insert_many(persons)
print(result.inserted_ids)
```

#### 删
```
# 删除单条记录
result1 = test.delete_one({'name': 'zone'})
pprint.pprint(result1)
```
```
# 批量删除
result1 = test.delete_many({'name': 'zone'})
pprint.pprint(result1)
```

#### 改
```
# 更新单条记录
res = test.update_one({'name': 'zone'}, {'$set': {'sex': 'girl girl'}})
print(res.matched_count)
```
```
# 更新多条记录
test.update_many({'name': 'zone'}, {'$set': {'sex': 'girl girl'}})
```

#### 查
```
# 查找多条记录
pprint.pprint(test.find())

# 添加查找条件
pprint.pprint(test.find({"sex": "boy"}).sort("name"))
```

#### 聚合
如果你是我的老读者，那么你肯定知道我之前的骚操作，就是用爬虫爬去数据之后，用聚合统计结合可视化图表进行数据展示。
```
aggs = [
    {"$match": {"$or" : [{"field1": {"$regex": "regex_str"}}, {"field2": {"$regex": "regex_str"}}]}}, # 正则匹配字段
    {"$project": {"field3":1, "field4":1}},# 筛选字段 
    {"$group": {"_id": {"field3": "$field3", "field4":"$field4"}, "count": {"$sum": 1}}}, # 聚合操作
]

result = test.aggregate(pipeline=aggs)
```
例子：以分组的方式统计 sex 这个关键词出现的次数，说白了就是统计有多少个男性，多少个女性。
```
test.aggregate([{'$group': {'_id': '$sex', 'weight': {'$sum': 1}}}])
```
聚合效果图：（[秋招季，用Python分析深圳程序员工资有多高？]([https://mp.weixin.qq.com/s/n7lA03Axbfe5DvoccDqIBQ](https://mp.weixin.qq.com/s/n7lA03Axbfe5DvoccDqIBQ)
)文章配图）
![Python 工作年限要求](https://upload-images.jianshu.io/upload_images/2470773-14c5d4b68fb04657.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![Python 学历要求](https://upload-images.jianshu.io/upload_images/2470773-30f7bbaaf255b98a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


## Motor（异步）
Motor 是一个异步实现的 MongoDB 存储库 Motor 与 Pymongo 的配置基本类似。连接对象就由 MongoClient 变为 AsyncIOMotorClient 了。下面进行详细介绍一下。
#### 连接
```
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
```
#### 增加一条记录
添加一条记录。
```
async def do_insert():
     document = {'name': 'zone','sex':'boy'}
     result = await db.test_collection.insert_one(document)
     print('result %s' % repr(result.inserted_id))
loop = asyncio.get_event_loop()
loop.run_until_complete(do_insert())
```
![增加一条记录](https://upload-images.jianshu.io/upload_images/2470773-66962a51b9df313d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


#### 批量增加记录
添加结果如图所暗示。
```
async def do_insert():
    result = await db.test_collection.insert_many(
        [{'name': i, 'sex': str(i + 2)} for i in range(20)])
    print('inserted %d docs' % (len(result.inserted_ids),))

loop = asyncio.get_event_loop()
loop.run_until_complete(do_insert())

```
![批量增加记录](https://upload-images.jianshu.io/upload_images/2470773-9127fd11f6daca27.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### 查找一条记录
```
async def do_find_one():
    document = await db.test_collection.find_one({'name': 'zone'})
    pprint.pprint(document)

loop = asyncio.get_event_loop()
loop.run_until_complete(do_find_one())
```
![查找一条记录](https://upload-images.jianshu.io/upload_images/2470773-157dccac8e51ed9f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
#### 查找多条记录
查找记录可以添加筛选条件。
```
async def do_find():
    cursor = db.test_collection.find({'name': {'$lt': 5}}).sort('i')
    for document in await cursor.to_list(length=100):
        pprint.pprint(document)

loop = asyncio.get_event_loop()
loop.run_until_complete(do_find())

# 添加筛选条件，排序、跳过、限制返回结果数
async def do_find():
    cursor = db.test_collection.find({'name': {'$lt': 4}})
    # Modify the query before iterating
    cursor.sort('name', -1).skip(1).limit(2)
    async for document in cursor:
        pprint.pprint(document)

loop = asyncio.get_event_loop()
loop.run_until_complete(do_find())
```
![查找多条记录](https://upload-images.jianshu.io/upload_images/2470773-372d8b8816641696.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### 统计
```
async def do_count():
    n = await db.test_collection.count_documents({})
    print('%s documents in collection' % n)
    n = await db.test_collection.count_documents({'name': {'$gt': 1000}})
    print('%s documents where i > 1000' % n)

loop = asyncio.get_event_loop()
loop.run_until_complete(do_count())
```
![统计](https://upload-images.jianshu.io/upload_images/2470773-202e86f61958a745.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### 替换
替换则是将除 id 以外的其他内容全部替换掉。
```
async def do_replace():
    coll = db.test_collection
    old_document = await coll.find_one({'name': 'zone'})
    print('found document: %s' % pprint.pformat(old_document))
    _id = old_document['_id']
    result = await coll.replace_one({'_id': _id}, {'sex': 'hanson boy'})
    print('replaced %s document' % result.modified_count)
    new_document = await coll.find_one({'_id': _id})
    print('document is now %s' % pprint.pformat(new_document))

loop = asyncio.get_event_loop()
loop.run_until_complete(do_replace())
```
![替换](https://upload-images.jianshu.io/upload_images/2470773-c8896430dd532c63.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### 更新
更新指定字段，不会影响到其他内容。
```
async def do_update():
    coll = db.test_collection
    result = await coll.update_one({'name': 0}, {'$set': {'sex': 'girl'}})
    print('更新条数： %s ' % result.modified_count)
    new_document = await coll.find_one({'name': 0})
    print('更新结果为： %s' % pprint.pformat(new_document))

loop = asyncio.get_event_loop()
loop.run_until_complete(do_update())
```
![更新](https://upload-images.jianshu.io/upload_images/2470773-13e166ec966342e7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### 删除
删除指定记录。
```
async def do_delete_many():
    coll = db.test_collection
    n = await coll.count_documents({})
    print('删除前有 %s 条数据' % n)
    result = await db.test_collection.delete_many({'name': {'$gte': 10}})
    print('删除后 %s ' % (await coll.count_documents({})))

loop = asyncio.get_event_loop()
loop.run_until_complete(do_delete_many())
```
![删除](https://upload-images.jianshu.io/upload_images/2470773-c48a1775b9cb8abc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 后记
MongoDB 的骚操作就介绍到这里，后面会继续写 MySQL 和 Redis 的骚操作。尽请期待。