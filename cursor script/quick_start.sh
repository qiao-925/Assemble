#!/bin/bash
# 技术信息工作流系统 - 快速启动脚本

echo "🚀 技术信息智能构建工作流系统"
echo "=================================="

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 python3，请先安装Python 3.7+"
    exit 1
fi

echo "✅ Python环境检查通过"

# 创建虚拟环境（可选）
if [ "$1" = "--venv" ]; then
    echo "🔧 创建虚拟环境..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ 虚拟环境已激活"
fi

# 安装依赖
echo "📦 安装依赖包..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败，请检查网络连接"
    exit 1
fi

echo "✅ 依赖安装完成"

# 创建必要目录
echo "📁 创建目录结构..."
mkdir -p data output cache config

# 检查配置文件
if [ ! -f "config/workflow_config.yaml" ]; then
    echo "⚠️  配置文件不存在，将使用默认配置"
fi

echo "✅ 目录结构创建完成"

# 提供使用选项
echo ""
echo "🎯 现在你可以："
echo "1. 运行演示程序: python demo.py"
echo "2. 生成每日摘要: python tech_workflow.py daily"
echo "3. 分析GitHub项目: python tech_workflow.py analyze-project --repo='microsoft/garnet'"
echo "4. 查看帮助: python tech_workflow.py --help"
echo ""

# 询问是否立即运行演示
read -p "是否立即运行演示程序？(y/n): " choice
if [ "$choice" = "y" ] || [ "$choice" = "Y" ]; then
    echo "🎬 启动演示程序..."
    python demo.py
else
    echo "👋 设置完成！随时运行 python demo.py 开始体验"
fi