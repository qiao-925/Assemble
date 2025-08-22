#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技术信息智能构建工作流主程序
整合信息收集、智能分析和内容生成功能
"""

import argparse
import sys
import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tech_info_collector import TechInfoCollector, TechInfo
from tech_analyzer import TechAnalyzer, TechAnalysis

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TechWorkflow:
    """技术信息工作流主控制器"""
    
    def __init__(self, config_path: str = "config/workflow_config.yaml"):
        self.collector = TechInfoCollector(config_path)
        self.analyzer = TechAnalyzer()
        self.config_path = config_path
        
        # 确保必要目录存在
        self._ensure_directories()
    
    def _ensure_directories(self):
        """确保必要的目录存在"""
        directories = ["data", "output", "cache", "config"]
        for dir_name in directories:
            Path(dir_name).mkdir(exist_ok=True)
    
    def run_daily_digest(self) -> str:
        """执行每日技术信息摘要"""
        logger.info("🌅 开始生成每日技术摘要")
        
        # 收集信息
        collected_data = self.collector.collect_all_sources()
        
        # 保存原始数据
        data_file = self.collector.save_collected_data(collected_data)
        
        # 生成趋势分析
        trend_analysis = self.analyzer.generate_trend_report(collected_data)
        
        # 保存分析结果
        output_file = self.analyzer.save_analysis(trend_analysis)
        
        logger.info(f"✅ 每日摘要已完成，输出文件: {output_file}")
        return output_file
    
    def analyze_project(self, repo_url: str) -> str:
        """分析指定的GitHub项目"""
        logger.info(f"🔍 开始分析项目: {repo_url}")
        
        # 进行项目分析
        analysis = self.analyzer.analyze_github_project(repo_url)
        
        if analysis:
            # 保存分析结果
            output_file = self.analyzer.save_analysis(analysis)
            logger.info(f"✅ 项目分析已完成，输出文件: {output_file}")
            return output_file
        else:
            logger.error("❌ 项目分析失败")
            return None
    
    def compare_projects(self, project_urls: list) -> str:
        """对比多个项目"""
        logger.info(f"⚖️ 开始对比 {len(project_urls)} 个项目")
        
        # 分析每个项目
        analyses = []
        for url in project_urls:
            analysis = self.analyzer.analyze_github_project(url)
            if analysis:
                analyses.append(analysis)
        
        if len(analyses) < 2:
            logger.error("❌ 至少需要2个有效项目进行对比")
            return None
        
        # 生成对比报告
        comparison_content = self._generate_comparison_report(analyses)
        
        # 保存对比结果
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"output/competitor_comparison_{timestamp}.md"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(comparison_content)
        
        logger.info(f"✅ 项目对比已完成，输出文件: {output_file}")
        return output_file
    
    def _generate_comparison_report(self, analyses: List[TechAnalysis]) -> str:
        """生成项目对比报告"""
        content_parts = []
        
        # 报告标题
        project_names = [analysis.title.replace(' 技术深度解析', '') for analysis in analyses]
        title = f"# ⚖️ {' vs '.join(project_names)} 竞品技术对比分析"
        content_parts.append(title)
        
        # 对比概览
        overview = f"""
## 🎯 对比概览

本报告对比分析了 {len(analyses)} 个相关技术项目，从技术架构、性能表现、生态系统等多个维度进行深度对比。

### 📊 基本信息对比

| 项目 | Stars | Forks | 主要语言 | 开源协议 |
|------|-------|-------|----------|----------|
"""
        
        # 添加表格数据（这里需要从分析中提取）
        for analysis in analyses:
            # 提取基本信息（简化版，实际需要从分析内容中解析）
            overview += f"| {analysis.title.replace(' 技术深度解析', '')} | - | - | - | - |\n"
        
        content_parts.append(overview)
        
        # 详细对比
        details = """
## 🔧 技术架构对比

### 设计哲学差异
"""
        
        for i, analysis in enumerate(analyses, 1):
            details += f"\n#### {i}. {analysis.title.replace(' 技术深度解析', '')}\n"
            details += f"主要洞察：{analysis.insights[0] if analysis.insights else '待深入分析'}\n"
        
        content_parts.append(details)
        
        # 综合评价
        conclusion = f"""
## 🏆 综合评价

基于技术架构、生态健康度、社区活跃度等维度的综合分析：

*（具体评价需要基于详细的技术对比数据进行生成）*

---
*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        content_parts.append(conclusion)
        
        return '\n'.join(content_parts)
    
    def run_trending_analysis(self, topic: str = None) -> str:
        """运行趋势分析"""
        logger.info(f"📈 开始趋势分析 - 主题: {topic or '全领域'}")
        
        # 收集数据
        collected_data = self.collector.collect_all_sources()
        
        # 如果指定了主题，过滤相关内容
        if topic:
            collected_data = self._filter_by_topic(collected_data, topic)
        
        # 生成趋势报告
        trend_analysis = self.analyzer.generate_trend_report(collected_data)
        
        # 保存结果
        output_file = self.analyzer.save_analysis(trend_analysis)
        
        logger.info(f"✅ 趋势分析已完成，输出文件: {output_file}")
        return output_file
    
    def _filter_by_topic(self, data: Dict, topic: str) -> Dict:
        """根据主题过滤数据"""
        filtered_data = {}
        topic_lower = topic.lower()
        
        for source, info_list in data.items():
            filtered_list = []
            for info in info_list:
                # 检查标题、描述和标签是否包含主题
                if (topic_lower in info['title'].lower() or 
                    topic_lower in info.get('description', '').lower() or
                    any(topic_lower in tag.lower() for tag in info.get('tags', []))):
                    filtered_list.append(info)
            
            if filtered_list:
                filtered_data[source] = filtered_list
        
        return filtered_data

def main():
    """主函数，处理命令行参数"""
    parser = argparse.ArgumentParser(description='技术信息智能构建工作流')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 每日摘要命令
    daily_parser = subparsers.add_parser('daily', help='生成每日技术摘要')
    
    # 项目分析命令
    analyze_parser = subparsers.add_parser('analyze-project', help='分析GitHub项目')
    analyze_parser.add_argument('--repo', required=True, help='GitHub仓库URL或owner/repo格式')
    
    # 趋势分析命令
    trend_parser = subparsers.add_parser('trend-report', help='生成技术趋势报告')
    trend_parser.add_argument('--topic', help='指定分析主题')
    
    # 项目对比命令
    compare_parser = subparsers.add_parser('compare', help='对比多个项目')
    compare_parser.add_argument('--projects', required=True, help='项目列表，用逗号分隔')
    
    # 配置命令
    config_parser = subparsers.add_parser('config', help='显示或修改配置')
    config_parser.add_argument('--show', action='store_true', help='显示当前配置')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 创建工作流实例
    workflow = TechWorkflow()
    
    try:
        if args.command == 'daily':
            output_file = workflow.run_daily_digest()
            print(f"🎉 每日技术摘要已生成: {output_file}")
            
        elif args.command == 'analyze-project':
            repo_url = args.repo
            # 如果不是完整URL，构造GitHub URL
            if not repo_url.startswith('http'):
                repo_url = f"https://github.com/{repo_url}"
            
            output_file = workflow.analyze_project(repo_url)
            if output_file:
                print(f"🎉 项目分析已完成: {output_file}")
            else:
                print("❌ 项目分析失败")
                
        elif args.command == 'trend-report':
            output_file = workflow.run_trending_analysis(args.topic)
            print(f"🎉 趋势报告已生成: {output_file}")
            
        elif args.command == 'compare':
            project_list = [p.strip() for p in args.projects.split(',')]
            # 构造完整URL
            project_urls = []
            for project in project_list:
                if not project.startswith('http'):
                    project_urls.append(f"https://github.com/{project}")
                else:
                    project_urls.append(project)
            
            output_file = workflow.compare_projects(project_urls)
            if output_file:
                print(f"🎉 项目对比已完成: {output_file}")
            else:
                print("❌ 项目对比失败")
                
        elif args.command == 'config':
            if args.show:
                with open('config/workflow_config.yaml', 'r', encoding='utf-8') as f:
                    print(f.read())
                    
    except Exception as e:
        logger.error(f"执行命令时出错: {e}")
        print(f"❌ 命令执行失败: {e}")

if __name__ == "__main__":
    main()