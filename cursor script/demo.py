#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技术信息工作流演示脚本
快速体验各种功能的演示程序
"""

import sys
import os
from datetime import datetime

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tech_workflow import TechWorkflow

def print_banner():
    """打印系统横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                🤖 技术信息智能构建工作流系统                   ║
║                     Tech Info Workflow Demo                   ║
╚══════════════════════════════════════════════════════════════╝

🎯 功能展示菜单：
"""
    print(banner)

def print_menu():
    """打印功能菜单"""
    menu = """
1. 📈 生成每日技术趋势摘要
2. 🔍 深度分析GitHub项目  
3. ⚖️ 对比多个技术项目
4. 🎯 按主题生成趋势报告
5. 📋 查看系统配置
6. 🧪 运行完整演示流程
0. 退出

请选择功能 (0-6): """
    return input(menu).strip()

def demo_daily_digest(workflow):
    """演示每日摘要功能"""
    print("\n🌅 正在生成每日技术摘要...")
    print("📡 收集GitHub趋势项目和Hacker News讨论...")
    
    try:
        output_file = workflow.run_daily_digest()
        print(f"✅ 每日摘要已生成！")
        print(f"📄 输出文件: {output_file}")
        
        # 显示部分内容预览
        print("\n📖 内容预览:")
        with open(output_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:20]  # 前20行
            for line in lines:
                print(f"   {line.rstrip()}")
        if len(lines) == 20:
            print("   ... (更多内容请查看完整文件)")
            
    except Exception as e:
        print(f"❌ 生成失败: {e}")

def demo_project_analysis(workflow):
    """演示项目分析功能"""
    print("\n🔍 项目深度分析演示")
    
    # 提供一些示例项目
    sample_projects = [
        "microsoft/garnet",
        "redis/redis", 
        "kubernetes/kubernetes",
        "facebook/react",
        "openai/whisper"
    ]
    
    print("\n📚 推荐分析项目:")
    for i, project in enumerate(sample_projects, 1):
        print(f"  {i}. {project}")
    
    choice = input("\n请选择项目编号，或输入自定义的 owner/repo 格式: ").strip()
    
    try:
        if choice.isdigit() and 1 <= int(choice) <= len(sample_projects):
            repo = sample_projects[int(choice) - 1]
        else:
            repo = choice
        
        print(f"\n🔍 正在分析项目: {repo}")
        print("📊 收集项目信息、发布历史、贡献者数据...")
        
        output_file = workflow.analyze_project(f"https://github.com/{repo}")
        
        if output_file:
            print(f"✅ 项目分析已完成！")
            print(f"📄 输出文件: {output_file}")
            
            # 显示部分内容预览
            print("\n📖 分析预览:")
            with open(output_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:25]
                for line in lines:
                    print(f"   {line.rstrip()}")
            if len(lines) == 25:
                print("   ... (完整分析请查看输出文件)")
        else:
            print("❌ 分析失败，请检查项目名称是否正确")
            
    except Exception as e:
        print(f"❌ 分析失败: {e}")

def demo_project_comparison(workflow):
    """演示项目对比功能"""
    print("\n⚖️ 竞品技术对比演示")
    
    # 提供一些对比组合
    comparison_sets = [
        ["redis/redis", "microsoft/garnet", "memcached/memcached"],
        ["kubernetes/kubernetes", "docker/swarm", "hashicorp/nomad"],
        ["facebook/react", "vuejs/vue", "angular/angular"],
        ["openai/whisper", "mozilla/DeepSpeech", "speechbrain/speechbrain"]
    ]
    
    print("\n📊 推荐对比组合:")
    for i, projects in enumerate(comparison_sets, 1):
        print(f"  {i}. {' vs '.join(projects)}")
    
    choice = input("\n请选择对比组合编号，或输入自定义项目列表(用逗号分隔): ").strip()
    
    try:
        if choice.isdigit() and 1 <= int(choice) <= len(comparison_sets):
            projects = comparison_sets[int(choice) - 1]
        else:
            projects = [p.strip() for p in choice.split(',')]
        
        if len(projects) < 2:
            print("❌ 至少需要2个项目进行对比")
            return
        
        print(f"\n⚖️ 正在对比项目: {' vs '.join(projects)}")
        print("📊 收集各项目详细信息...")
        
        project_urls = [f"https://github.com/{project}" for project in projects]
        output_file = workflow.compare_projects(project_urls)
        
        if output_file:
            print(f"✅ 项目对比已完成！")
            print(f"📄 输出文件: {output_file}")
        else:
            print("❌ 对比失败")
            
    except Exception as e:
        print(f"❌ 对比失败: {e}")

def demo_trend_analysis(workflow):
    """演示趋势分析功能"""
    print("\n📈 技术趋势分析演示")
    
    topics = [
        "ai", "kubernetes", "rust", "performance", 
        "database", "cloud-native", "security", "frontend"
    ]
    
    print("\n🎯 热门主题:")
    for i, topic in enumerate(topics, 1):
        print(f"  {i}. {topic}")
    
    choice = input("\n请选择主题编号，或输入自定义主题（回车分析全领域）: ").strip()
    
    try:
        if choice.isdigit() and 1 <= int(choice) <= len(topics):
            topic = topics[int(choice) - 1]
        elif choice:
            topic = choice
        else:
            topic = None
        
        print(f"\n📈 正在分析趋势 - 主题: {topic or '全领域'}")
        print("📡 收集相关技术信息...")
        
        output_file = workflow.run_trending_analysis(topic)
        print(f"✅ 趋势分析已完成！")
        print(f"📄 输出文件: {output_file}")
        
    except Exception as e:
        print(f"❌ 趋势分析失败: {e}")

def show_config():
    """显示系统配置"""
    print("\n📋 当前系统配置:")
    
    config_file = "config/workflow_config.yaml"
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            config_content = f.read()
        
        # 只显示前50行，避免过长
        lines = config_content.split('\n')[:50]
        for line in lines:
            print(f"   {line}")
        
        if len(config_content.split('\n')) > 50:
            print("   ... (更多配置请查看完整文件)")
    else:
        print("❌ 配置文件不存在")

def run_full_demo(workflow):
    """运行完整演示流程"""
    print("\n🧪 完整演示流程开始")
    print("=" * 60)
    
    demos = [
        ("📈 每日摘要演示", lambda: demo_daily_digest(workflow)),
        ("🔍 项目分析演示", lambda: demo_project_analysis_simple(workflow)),
        ("📊 趋势分析演示", lambda: demo_trend_analysis_simple(workflow))
    ]
    
    for name, demo_func in demos:
        print(f"\n{name}")
        print("-" * 40)
        try:
            demo_func()
            print("✅ 演示完成")
        except Exception as e:
            print(f"❌ 演示失败: {e}")
        
        input("\n按回车继续下一个演示...")
    
    print("\n🎉 完整演示流程结束！")

def demo_project_analysis_simple(workflow):
    """简化版项目分析演示"""
    # 使用固定项目避免用户输入
    repo = "microsoft/garnet"
    print(f"分析项目: {repo}")
    output_file = workflow.analyze_project(f"https://github.com/{repo}")
    if output_file:
        print(f"分析完成: {output_file}")

def demo_trend_analysis_simple(workflow):
    """简化版趋势分析演示"""
    print("分析主题: AI")
    output_file = workflow.run_trending_analysis("ai")
    print(f"趋势分析完成: {output_file}")

def main():
    """主演示程序"""
    print_banner()
    
    # 创建工作流实例
    try:
        workflow = TechWorkflow()
        print("✅ 系统初始化完成")
    except Exception as e:
        print(f"❌ 系统初始化失败: {e}")
        return
    
    while True:
        try:
            choice = print_menu()
            
            if choice == "0":
                print("\n👋 感谢使用技术信息工作流系统！")
                break
            elif choice == "1":
                demo_daily_digest(workflow)
            elif choice == "2":
                demo_project_analysis(workflow)
            elif choice == "3":
                demo_project_comparison(workflow)
            elif choice == "4":
                demo_trend_analysis(workflow)
            elif choice == "5":
                show_config()
            elif choice == "6":
                run_full_demo(workflow)
            else:
                print("❌ 无效选择，请重新输入")
            
            if choice != "0":
                input("\n按回车继续...")
                
        except KeyboardInterrupt:
            print("\n\n👋 用户中断，系统退出")
            break
        except Exception as e:
            print(f"\n❌ 系统错误: {e}")
            input("按回车继续...")

if __name__ == "__main__":
    main()