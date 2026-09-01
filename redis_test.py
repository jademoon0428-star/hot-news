import redis

# 连接 Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# 存储数据
r.set('name', 'Python')
r.set('age', 3)

# 读取数据
name = r.get('name')
age = r.get('age')

print(f"姓名: {name}")
print(f"年龄: {age}")

# 获取所有键
print("\n所有键:")
for key in r.keys('*'):
    print(f"  {key}: {r.get(key)}")