# 🤖 Background Agent 使用指南

## ⚡ **一键启动系统**

```python
# 在cursor script目录下执行
exec(open("auto_setup.py").read())
```

## 🎯 **核心功能**

### 📱 **每日自动生成**
系统会在每天8:00自动生成技术摘要，无需干预。

### 🔔 **Background Agent 触发接口**

```python
# 导入触发工具
from bg_agent_trigger import (
    bg_daily_digest, bg_analyze_project, 
    bg_trend_analysis, bg_compare_projects,
    bg_get_status, bg_get_recent_reports
)

# 1. 生成每日技术摘要
output_file = bg_daily_digest()
print(f"每日摘要: {output_file}")

# 2. 深度分析GitHub项目
output_file = bg_analyze_project("microsoft/garnet")
print(f"项目分析: {output_file}")

# 3. 技术趋势分析
output_file = bg_trend_analysis("ai")  # 指定主题
output_file = bg_trend_analysis()      # 全领域分析
print(f"趋势分析: {output_file}")

# 4. 项目对比分析
output_file = bg_compare_projects([
    "redis/redis", 
    "microsoft/garnet", 
    "memcached/memcached"
])
print(f"项目对比: {output_file}")

# 5. 获取系统状态
status = bg_get_status()
print(f"系统状态: {status['status']}")

# 6. 获取最近报告
reports = bg_get_recent_reports(days=7)
print(f"最近报告: {len(reports)} 个")
```

## 🔧 **系统管理**

### 启动/停止服务
```python
# 启动服务
os.system("cd cursor script && python service_manager.py start")

# 查看状态  
os.system("cd cursor script && python service_manager.py status")

# 停止服务
os.system("cd cursor script && python service_manager.py stop")
```

### 快速检查
```python
# 快速检查服务状态
import json
status_file = "cursor script/daemon_status.json"
if os.path.exists(status_file):
    with open(status_file) as f:
        status = json.load(f)
    print(f"状态: {status['status']} - {status['message']}")
```

## 📊 **输出说明**

所有生成的内容都保存在 `cursor script/output/` 目录：

- **每日摘要**: `trend_report_YYYYMMDD_HHMMSS.md`
- **项目分析**: `project_analysis_YYYYMMDD_HHMMSS.md` 
- **竞品对比**: `competitor_comparison_YYYYMMDD_HHMMSS.md`

## 🎨 **自定义配置**

编辑 `cursor script/config/workflow_config.yaml` 可以自定义：

- **信息源**: 添加RSS、技术媒体、开源基金会等
- **分析重点**: 技术架构、性能、生态系统等维度
- **筛选规则**: 项目星标数、技术领域等过滤条件
- **触发时间**: 修改每日生成时间

## ⚡ **极简使用**

最简单的使用方式：

```python
# 一行代码触发每日摘要
exec(open("cursor script/bg_agent_trigger.py").read().replace("if __name__", "if False")); print(bg_daily_digest())

# 一行代码分析项目
exec(open("cursor script/bg_agent_trigger.py").read().replace("if __name__", "if False")); print(bg_analyze_project("microsoft/garnet"))
```

## 🚀 **完整工作流示例**

```python
# 完整的每日工作流示例
import os
import json
from datetime import datetime

# 1. 检查服务状态
os.chdir("cursor script")
from bg_agent_trigger import bg_get_status, bg_daily_digest, bg_get_recent_reports

status = bg_get_status()
print(f"🔄 系统状态: {status.get('status', 'unknown')}")

# 2. 如果需要，触发每日分析
if input("是否生成今日技术摘要？(y/n): ").lower() == 'y':
    print("🚀 开始生成...")
    result = bg_daily_digest()
    if result:
        print(f"✅ 完成! 文件: {result}")
        
        # 3. 显示部分内容
        with open(result, 'r', encoding='utf-8') as f:
            content = f.read()[:500]
        print(f"\n📖 内容预览:\n{content}...")

# 4. 查看最近的报告
reports = bg_get_recent_reports(3)
if reports:
    print(f"\n📚 最近报告 ({len(reports)} 个):")
    for report in reports:
        print(f"  📄 {os.path.basename(report['file'])}")
```

---

**🎯 关键优势**：
- ✅ **无需人工干预** - 每天自动生成技术摘要
- ✅ **即时响应** - Background Agent可随时触发分析  
- ✅ **深度分析** - 模仿用户的分析风格和深度
- ✅ **完全可配置** - 信息源、分析重点可自定义
- ✅ **状态可见** - 实时监控运行状态和结果