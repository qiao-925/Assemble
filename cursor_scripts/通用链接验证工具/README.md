# 通用链接有效性验证工具

这是一个通用的链接有效性验证工具，可以用于验证各种文档中的链接，并分析内容相关性。

## 功能特性

- 🔍 **智能链接提取**: 自动从Markdown文件中提取链接
- ✅ **链接有效性验证**: 检查HTTP状态码和可访问性
- 🎯 **内容相关性分析**: 基于关键词分析内容相关性
- 📊 **详细报告生成**: 生成JSON和Markdown格式的验证报告
- 🔄 **链接替换建议**: 为失效链接提供替代链接建议
- ⚙️ **高度可配置**: 支持自定义关键词、搜索策略等

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 基础链接验证

```python
from link_validator import UniversalLinkValidator

# 创建验证器实例
validator = UniversalLinkValidator(
    project_name="我的项目",
    keywords=["python", "web", "development"],
    domains=["github.com", "stackoverflow.com"]
)

# 验证文档中的链接
validator.validate_document("path/to/document.md")
```

### 2. 自定义配置

```python
# 创建自定义配置
config = {
    "project_name": "Spring框架文档",
    "keywords": ["spring", "java", "framework", "dependency injection"],
    "domains": ["spring.io", "docs.spring.io", "github.com"],
    "relevance_threshold": 0.3,
    "max_links_per_section": 10
}

validator = UniversalLinkValidator(**config)
```

### 3. 批量处理

```python
# 处理多个文档
documents = [
    "docs/chapter1.md",
    "docs/chapter2.md",
    "docs/chapter3.md"
]

for doc in documents:
    validator.validate_document(doc)
```

## 配置选项

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `project_name` | str | "通用项目" | 项目名称，用于报告标题 |
| `keywords` | list | [] | 内容相关性分析的关键词 |
| `domains` | list | [] | 信任的域名列表 |
| `relevance_threshold` | float | 0.3 | 相关性阈值 |
| `max_links_per_section` | int | 5 | 每个章节最大链接数 |
| `timeout` | int | 15 | 请求超时时间(秒) |
| `delay` | float | 1.0 | 请求间隔时间(秒) |

## 输出文件

- `link_validation_results.json`: 详细的验证结果
- `validated_links.md`: 验证后的有效链接列表
- `link_recommendations.md`: 替代链接建议
- `validation_summary.md`: 验证总结报告

## 示例配置

### Redis项目配置
```python
redis_config = {
    "project_name": "Redis设计哲学文档",
    "keywords": ["redis", "antirez", "memory", "cache", "database", "performance"],
    "domains": ["redis.io", "antirez.com", "github.com"],
    "relevance_threshold": 0.25
}
```

### Spring项目配置
```python
spring_config = {
    "project_name": "Spring框架文档",
    "keywords": ["spring", "java", "framework", "dependency injection", "aop"],
    "domains": ["spring.io", "docs.spring.io", "github.com"],
    "relevance_threshold": 0.3
}
```

## 扩展功能

- 支持多种文档格式 (Markdown, HTML, Text)
- 可配置的搜索引擎集成
- 自定义相关性算法
- 批量链接更新
- 链接健康度监控

## 许可证

MIT License
