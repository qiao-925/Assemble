# 🤖 Cursor Script - AI辅助脚本工具

> AI辅助开发的实用脚本集合，提升编程效率

## 📚 脚本列表

### 🔗 链接验证工具
- **[enhanced_link_validator.py](enhanced_link_validator.py)** - 增强版链接验证脚本，支持多种链接格式检测

### 📦 依赖管理
- **[enhanced_requirements.txt](enhanced_requirements.txt)** - 增强版依赖管理文件

### 🚀 **NEW! 技术信息智能构建工作流**
- **[tech_workflow.py](tech_workflow.py)** - 主工作流程序，整合信息收集和分析功能
- **[tech_info_collector.py](tech_info_collector.py)** - 技术信息收集器，支持GitHub趋势、HN讨论等多源采集
- **[tech_analyzer.py](tech_analyzer.py)** - 智能分析器，生成深度技术解析和趋势报告
- **[demo.py](demo.py)** - 交互式演示程序，快速体验各种功能
- **[config/workflow_config.yaml](config/workflow_config.yaml)** - 完全可自定义的配置文件
- **[requirements.txt](requirements.txt)** - 工作流系统依赖包

## 🎯 主要功能

### 🔍 链接验证
- **多格式支持** - 支持HTTP、HTTPS、FTP等多种链接格式
- **批量检测** - 支持批量验证多个链接
- **状态报告** - 详细的验证结果和状态报告
- **错误处理** - 完善的异常处理和重试机制

### 🚀 **技术信息智能构建（NEW!）**
- **🔍 开源项目深度解析** - 自动分析GitHub项目的技术架构、设计哲学
- **📊 技术趋势调研报告** - 基于多源数据生成趋势洞察
- **⚖️ 竞品技术对比分析** - 多维度对比分析技术项目
- **📈 可视化内容生成** - 自动生成图表和技术地图
- **⏰ 定时/手动触发** - 支持每日自动生成或按需手动触发
- **🎨 完全可配置** - 信息源、分析重点、输出格式完全自定义

## 💡 使用场景

### 🔗 链接验证
- **文档维护** - 定期检查文档中的链接有效性
- **网站监控** - 监控网站链接的健康状态
- **内容审核** - 验证内容中的外部链接
- **质量保证** - 确保文档和代码的质量

### 🤖 **技术信息工作流（NEW!）**
- **技术调研** - 自动收集和分析最新技术趋势
- **项目评估** - 深度分析开源项目的技术价值
- **竞品分析** - 多维度对比技术解决方案
- **知识积累** - 构建结构化的技术知识库
- **决策支持** - 为技术选型提供数据支撑

## 🚀 **快速开始 - 技术信息工作流**

### 1️⃣ 安装依赖
```bash
cd "cursor script"
pip install -r requirements.txt
```

### 2️⃣ 体验演示
```bash
python demo.py
```

### 3️⃣ 命令行使用
```bash
# 生成每日技术摘要
python tech_workflow.py daily

# 深度分析GitHub项目
python tech_workflow.py analyze-project --repo="microsoft/garnet"

# 生成特定主题的趋势报告
python tech_workflow.py trend-report --topic="ai"

# 对比多个项目
python tech_workflow.py compare --projects="redis/redis,microsoft/garnet,memcached/memcached"

# 查看配置
python tech_workflow.py config --show
```

### 4️⃣ 自定义配置
编辑 [config/workflow_config.yaml](config/workflow_config.yaml) 文件，可以自定义：
- 📡 信息源（GitHub、HN、技术媒体等）
- 🎯 分析重点（技术、商业、社区维度）
- 🎨 输出偏好（语言、风格、格式）
- ⏰ 触发机制（定时任务设置）
- 🔍 过滤规则（项目筛选条件）

## 🔗 相关资源

- [scripts](../scripts/) - 更多实用脚本
- [Hammer](../# 🔨 Hammer - 工具与脚本/) - 工具和脚本集合
- [AI共创 - 速查Tips](../# 🚀 AI共创 - 速查Tips.md) - AI辅助编程技巧
- [tech_info_workflow_design.md](tech_info_workflow_design.md) - 工作流系统详细设计文档

## 📖 使用建议

### 🔗 链接验证
- 定期运行链接验证脚本，保持链接健康
- 结合AI工具优化验证逻辑和规则
- 关注验证结果，及时修复无效链接
- 持续改进脚本功能，提升验证效率

### 🤖 **技术信息工作流**
- **每日使用**：设置每日自动摘要，跟踪技术动态
- **深度分析**：遇到感兴趣的项目时，使用深度分析功能
- **决策支持**：技术选型前，使用竞品对比功能
- **知识积累**：定期运行趋势分析，构建技术知识体系
- **配置优化**：根据关注领域调整信息源和筛选规则

---

*持续更新中，欢迎提出建议和贡献内容！*