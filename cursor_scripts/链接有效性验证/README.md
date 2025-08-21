# Cursor Scripts 文件夹

这个文件夹专门用于存放由 Cursor/AI 工具生成的脚本、数据文件和相关资源。

## 📁 文件夹用途

- **区分内容来源**: 明确区分用户原创内容和AI生成内容
- **组织管理**: 集中管理AI生成的工具脚本和数据文件
- **版本控制**: 便于在版本控制中识别和管理AI生成的文件

## 📋 当前文件说明

### 脚本文件
- `link_validator.py` - Redis文档链接验证器
- `link_finder.py` - 链接查找和验证工具

### 数据文件
- `link_validation_results.json` - 原始链接验证结果数据
- `validated_links.json` - 验证后的有效链接数据
- `validated_references.md` - 验证后的参考资料Markdown格式

## 🚀 使用说明

1. 安装依赖:
   ```bash
   pip install requests beautifulsoup4 lxml
   ```

2. 运行链接验证:
   ```bash
   python link_validator.py
   ```

3. 运行链接查找工具:
   ```bash
   python link_finder.py
   ```

## 📊 工作成果

- ✅ 验证了Redis设计哲学文档中的35个原始链接
- ✅ 找到了18个有效替代链接
- ✅ 更新了文档中的所有参考资料
- ✅ 每个章节都有3-5个经过验证的高质量链接

## ⚠️ 注意事项

- 这些脚本由AI工具生成，使用前请检查和测试
- 运行脚本时请注意网络请求频率，避免被目标网站限制
- 生成的数据文件仅供参考，请人工审核后使用

## 📝 维护说明

此文件夹中的内容主要由AI工具维护和更新，如需修改请谨慎操作。
