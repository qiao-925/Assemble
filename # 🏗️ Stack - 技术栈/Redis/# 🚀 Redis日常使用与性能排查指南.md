# 🚀 Redis日常使用与性能排查指南

## 📝 草稿内容
常用命令：

- info指令 9大块
- slowlog慢日志命令

使用规范

- key可读性命名
- value的大小控制
    - 对于较大的数据，考虑压缩后存入
- 使用scan代替 keys *

SDK使用规范：

- 使用长连接和连接池
    - 几乎所有主流的 Redis 客户端库（如 Java 的 Jedis/Lettuce、Python 的 redis-py、Go 的 go-redis）都内置了连接池的实现。
    - 连接池本身是线程安全的，应该在整个应用程序的生命周期内被视为一个**单例**或**全局共享资源**。

运维规范：

- 生存密码保护机制，可读开放给开发
- 配置基线告警：节点CPU，内存，带宽等

largekey问题应对

- 监控命令：redis-cli — bigkeys
- 临时处理：删除无用数据unlink命令/拆分大 key
- 业务分析，考虑优化或设计新方案

hotkey问题应对

- 应用层加缓存分担压力 —— 客户端缓存
- Redis 集群节点扩展，负载均衡 —— redis部署方案的升级，使用集群
- 热key探测解决方案：  https://gitee.com/jd-platform-opensource/hotkey

---

## 🔍 核心命令与监控

### 📊 INFO指令详解
Redis INFO命令提供9大核心信息块：

- **Server**: 服务器信息（版本、运行时间、配置端口等）
- **Clients**: 客户端连接信息（连接数、阻塞连接数等）
- **Memory**: 内存使用详情（已用内存、峰值内存、内存碎片率等）
- **Persistence**: 持久化状态（RDB/AOF状态、最后保存时间等）
- **Stats**: 统计信息（命令总数、连接总数、拒绝连接数等）
- **Replication**: 复制信息（角色、从节点数量、复制延迟等）
- **CPU**: CPU使用情况（系统CPU、用户CPU等）
- **Cluster**: 集群信息（节点状态、槽位分配等）
- **Keyspace**: 数据库键空间统计

### 🐌 慢查询日志分析
```bash
# 设置慢查询阈值（微秒）
CONFIG SET slowlog-log-slower-than 10000

# 查看慢查询日志
SLOWLOG GET 10

# 获取慢查询日志长度
SLOWLOG LEN
```

## ⚡ 性能优化最佳实践

### 🔑 Key命名规范
- **业务前缀**: `user:profile:12345`
- **环境标识**: `prod:cache:user:12345`
- **版本控制**: `v1:user:profile:12345`
- **时间维度**: `daily:stats:20241201`

### 💾 Value大小控制策略
- **压缩阈值**: 超过1KB的数据考虑压缩
- **序列化优化**: 使用高效的序列化格式（如MessagePack、Protocol Buffers）
- **分片存储**: 大对象拆分为多个key存储

### 🔍 扫描优化
```bash
# 避免使用KEYS *，使用SCAN替代
SCAN 0 MATCH user:* COUNT 100

# 批量删除匹配的key
SCAN 0 MATCH temp:* COUNT 100 | xargs redis-cli DEL
```

## 🔌 客户端连接优化

### 🏊 连接池配置要点
```java
// Jedis连接池配置示例
JedisPoolConfig config = new JedisPoolConfig();
config.setMaxTotal(100);           // 最大连接数
config.setMaxIdle(20);             // 最大空闲连接数
config.setMinIdle(5);              // 最小空闲连接数
config.setMaxWaitMillis(3000);     // 最大等待时间
config.setTestOnBorrow(true);      // 借用连接时测试
config.setTestOnReturn(true);      // 归还连接时测试
```

### 🔒 连接安全策略
- **密码保护**: 启用AUTH认证
- **网络隔离**: 使用VPC或防火墙限制访问
- **SSL/TLS**: 生产环境启用加密传输

## 🚨 运维监控与告警

### 📈 关键指标监控
- **内存使用率**: 超过80%触发告警
- **连接数**: 接近最大连接数时告警
- **命令延迟**: P99延迟超过10ms告警
- **错误率**: 命令错误率超过1%告警

### 🚨 告警配置示例
```yaml
# Prometheus告警规则
groups:
- name: redis_alerts
  rules:
  - alert: RedisMemoryHigh
    expr: redis_memory_used_bytes / redis_memory_max_bytes > 0.8
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Redis内存使用率过高"
```

## 🐛 问题排查与解决

### 🔍 Large Key问题处理
```bash
# 1. 识别大key
redis-cli --bigkeys -i 0.1

# 2. 分析key大小分布
redis-cli --bigkeys -i 0.1 -d 1

# 3. 批量删除大key
redis-cli --scan --pattern "large_key:*" | xargs redis-cli UNLINK
```

**解决策略**:
- **数据压缩**: 使用LZ4、Snappy等算法压缩
- **分片存储**: 将大对象拆分为多个小key
- **异步删除**: 使用UNLINK替代DEL，避免阻塞

### 🔥 Hot Key问题处理
**识别方法**:
```bash
# 使用MONITOR命令观察热点key
MONITOR | grep "GET\|SET"

# 分析key访问频率
redis-cli --hotkeys
```

**解决方案**:
1. **本地缓存**: 应用层增加本地缓存
2. **读写分离**: 主从复制分担读压力
3. **集群扩展**: 使用Redis Cluster分散热点
4. **智能路由**: 基于访问频率动态路由

### 🚀 性能调优参数
```bash
# 内存策略优化
CONFIG SET maxmemory-policy allkeys-lru

# 网络缓冲区优化
CONFIG SET tcp-keepalive 300
CONFIG SET tcp-backlog 511

# 持久化优化
CONFIG SET save "900 1 300 10 60 10000"
```

## 📚 最佳实践总结

### ✅ 必须遵循的原则
1. **始终设置key过期时间**
2. **使用连接池管理连接**
3. **避免在生产环境使用KEYS命令**
4. **定期监控内存和连接数**
5. **启用慢查询日志分析**

### ❌ 常见陷阱
1. **忘记设置过期时间导致内存泄漏**
2. **连接池配置不当导致连接耗尽**
3. **使用阻塞命令影响性能**
4. **忽略慢查询日志**
5. **没有监控和告警机制**

### 🔮 进阶优化方向
1. **使用Redis Modules扩展功能**
2. **实施读写分离架构**
3. **配置Redis Sentinel高可用**
4. **使用Redis Streams处理消息队列**
5. **实施Redis Cluster分布式部署**