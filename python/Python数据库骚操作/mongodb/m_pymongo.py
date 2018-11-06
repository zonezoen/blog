from pymongo import MongoClient

client = MongoClient()
import pprint

# 普通连接
# client = MongoClient('localhost', 27017)
# client = MongoClient('mongodb://localhost:27017/')
#
# 密码连接
client = MongoClient('mongodb://username:password@localhost:27017/dbname')
db = client.zfdb
# db = client['zfdb']

# 增
test = db.test
person = {'name': 'zone', 'sex': 'boy'}
person_id = test.insert_one(person).inserted_id
print(person_id)

# 批量插入
persons = [{'name': 'zone', 'sex': 'boy'}, {'name': 'zone1', 'sex': 'boy1'}]
result = test.insert_many(persons)
print(result.inserted_ids)

# 删
result1 = test.delete_one({'name': 'zone'})
pprint.pprint(result1)
# 改
res = test.update_one({'name': 'zone'}, {'$set': {'sex': 'girl girl'}})
print(res.matched_count)

test.update_many({'name': 'zone'}, {'$set': {'sex': 'girl girl'}})

# 查
pprint.pprint(test.find_one())
# pprint.pprint(test.find_one({'name': 'zone'}))

# 查找多条记录
pprint.pprint(test.find())

# 添加查找条件
pprint.pprint(test.find({"sex": "boy"}).sort("name"))

# 统计
pprint.pprint(test.count_documents({"name": "zone"}))
#
#
