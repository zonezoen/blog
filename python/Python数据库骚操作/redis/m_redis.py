import redis
import time

# 连接
# 普通连接
# r = redis.StrictRedis(host='localhost', port=6378, db=0)
# r = redis.StrictRedis(host='localhost', port=6378, password="your password", db=0)
print()
# 连接池
"""
redis-py使用connection pool来管理对一个redis server的所有连接，避免每次建立、释放连接的开销。默认，每个Redis实例都会维护一个自己的连接池。
可以直接建立一个连接池，然后作为参数Redis，这样就可以实现多个Redis实例共享一个连接池
"""
pool = redis.ConnectionPool(host='localhost', port=6378,
                            decode_responses=True)  # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
r = redis.Redis(connection_pool=pool)

# 设置过期时间为 1 秒
r.set('foo', 'zone', ex=1)
# 效果同上
r.setex('foo', 'zone', 1)
# 效果同上
r.psetex('foo', 1000, 'zone')

print(r.get('foo'))

# 休眠两秒后，再打印输出
time.sleep(2)
print(r.get('foo'))
#
# # nx,如果设置为True，则只有name不存在时，当前set操作才执行 （新建）
# # 如果键 foo 不存在，那么输出是True；如果键fruit已经存在，输出是None
# print(r.set('foo', 'abc', nx=True))
# # 效果同上
# print(r.setnx('foo', 'abc'))
#
# # xx，如果设置为True，则只有name存在时，当前set操作才执行 （修改）
# # 如果键 foo 已经存在，那么输出是True；如果键fruit不存在，输出是None
# print(r.set('foo', 'abc', xx=True))
#
# # 批量设置值
# r.mget({'k1': 'v1', 'k2': 'v2'})
# r.mset(k1="v1", k2="v2")  # 这里k1 和k2 不能带引号 一次设置对个键值对
#
# # 批量获取
# print(r.mget("k1", "k2"))  # 一次取出多个键对应的值
# print(r.mget("k1"))
#
# # 设置新值，并获取原来的值
# r.set("name", "handsome boy")
# print(r.getset("name", "zone"))  # 设置的新值是barbecue 设置前的值是beef

# 获取子序列,一个汉字3个字节 1个字母一个字节
# r.set("name", "zonezone")
# print(r.getrange('name', 0, 3))
# # 获取所有字节
# print(r.getrange('name', 0, -1))


# 修改字符串内容
# r.set("name", "zonezone")
# r.setrange("name", 4, " is a boy")
# print(r.get("name"))

# 返回相应 key 的字符串长度
# r.set("name", "zonezone")
# print(r.strlen("name"))


# 自增 name 对应的值
# r.set("age", 123)
# print(r.get("age"))
# r.incr("age", amount=1)
# print(r.get("age"))


# 自增 name 对应的值
# r.set("age", 123.0)
# print(r.get("age"))
# r.incrbyfloat("age", amount=0.2)
# print(r.get("age"))

# 自减
# r.set("age", 123)
# r.decr("age", amount=1) # 递减1
# print(r.get("age"))


# 追加内容
# r.set("name", "关注 ")
# print(r.get("name"))
# r.append("name","公众号【zone7】")
# print(r.get("name"))


#
# r.hset("hash1", "k1", "v1")
# r.hset("hash1", "k2", "v2")
# print(r.hkeys("hash1"))  # 取hash中所有的key
# print(r.hget("hash1", "k1"))  # 单个取hash的key对应的值
# print(r.hmget("hash1", "k1", "k2"))  # 多个取hash的key对应的值
# r.hsetnx("hash1", "k2", "v3")  # 只能新建
# print(r.hget("hash1", "k2"))


# 批量增加
# r.hmset("hash2", {"k1": "v1", "k2": "v2"})
# 批量获取
# print(r.hmget("hash2", "k1", "k2"))

# 删除键值对
# r.hset("hash1", "name", "zone")
# print(r.hget("hash1", "name"))
# r.hdel("hash1", "name")
# print(r.hget("hash1", "name"))


# 自增自减
# r.hset("hash1", "age", 123)
# r.hincrby("hash1", "age", amount=-1)
# print(r.hget("hash1", "age"))
# r.hincrby("hash1", "age", amount=1)  # 不存在的话，value默认就是1
# print(r.hget("hash1", "age"))


# 自增自减
# r.hset("hash1", "age", 123.0)
# r.hincrbyfloat("hash1", "age", amount=-0.3)
# print(r.hget("hash1", "age"))
# r.hincrbyfloat("hash1", "age", amount=0.5)  # 不存在的话，value默认就是1
# print(r.hget("hash1", "age"))

# ===============================================
# 增加
# r.lpush("left_list", 11, 22, 33)
# print(r.lrange('left_list', 0, -1))
#
# r.rpush("right_list", 11, 22, 33)
# print(r.lrange("right_list", 0, 3))
#
# print(r.llen("right_list"))  # 列表长度

# 添加
# r.lpushx("left_list", 2222)
# print(r.lrange('left_list', 0, -1))
#
# r.rpushx("right_list", 1111)
# print(r.lrange('right_list', 0, -1))


# 新增
# 往列表中左边第一个出现的元素"11"前插入元素"00"
# r.linsert("left_list", "before", "11", "00")
# print(r.lrange("left_list", 0, -1))

# 修改
# r.lset("left_list", 0, "关注公众号【zone7】")    # 把索引号是0的元素修改成 关注公众号【zone7】
# print(r.lrange("left_list", 0, -1))

# 删除
# r.lrem("left_list", "33", 1)    # 将列表中左边第一次出现的"33"删除
# print(r.lrange("left_list", 0, -1))

# 删除并返回
# print(r.lpop("left_list"))  # 删除列表最左边的元素，并且返回删除的元素
# print(r.lrange("list2", 0, -1))


# =============================== set ======================================
# 增加
# r.sadd("set1", 1, 2, 3, 4)
# # 获取集合长度
# print(r.scard("set1"))
# # 获取集合中所有元素
# print(r.smembers("set1"))


# # 删除
# print(r.srem("set1", 1))
# print(r.smembers("set1"))


# 交集
# r.sadd("set2", 1, 2, 3, 4)
# r.sadd("set3", 3, 4, 5, 6)
# print(r.sinter("set2", "set3"))
# print(r.sinterstore("set4", "set2", "set3"))
# print(r.smembers("set4"))


# 并集
# print(r.sunion("set2", "set3"))

# print(r.sunionstore("set4", "set2", "set3")) # 取2个集合的并集
# print(r.smembers("set4"))

# 移动
# r.smove("set2", "set3", 3)
# print(r.smembers("set2"))
# print(r.smembers("set3"))

# 判断集合中是否存在某元素
# print(r.sismember("set2", 3))
# print(r.sismember("set3", 1))

# =============================== zset ======================================
# 增加
# r.zadd("zset1", n1=123, n2=234)
# print(r.zrange("zset1", 0, -1))   # 获取有序集合中所有元素
# 效果同上
# r.zadd("zset1", 'n1', 123, 'n2', 234)


# 获取 set 的长度
# print(r.zcard("zset1")) # 集合长度

# 只获取元素，不显示分数
# print(r.zrevrange("zset1", 0, -1))
# 获取有序集合中所有元素和分数,分数倒序
# print(r.zrevrange("zset1", 0, -1, withscores=True))


# 统计范围内元素个数
# for i in range(1, 30):
#     key = 'n' + str(i)
#     r.zadd("zset2", key, i)
# print(r.zrange("zset2", 0, -1, withscores=True))
# print(r.zcount("zset2", 1, 9))

# # 每次将n1的分数自增5
# r.zincrby("zset2", "n1", amount=5)
# print(r.zrange("zset2", 0, -1, withscores=True))

# 获取值的索引号
# print(r.zrank("zset2", "n2"))

# 删除
# 删除 n2
# r.zrem("zset2", "n2")
# print(r.zrange("zset2", 0, -1))

# 根据索引删除
# r.zremrangebyrank("zset2", 0, 1)
# print(r.zrange("zset2", 0, -1))

# 查找 n5 的值
# print(r.zscore("zset2", "n5"))
