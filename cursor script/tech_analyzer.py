#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技术信息智能分析器
基于收集的数据进行深度分析，生成洞察性内容
"""

import json
import requests
import re
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class TechAnalysis:
    """技术分析结果"""
    title: str
    analysis_type: str  # project_analysis, trend_report, competitor_comparison
    content: str
    insights: List[str]
    timeline: List[Dict]
    references: List[str]
    generated_at: datetime

class TechAnalyzer:
    """技术信息分析器"""
    
    def __init__(self):
        self.analysis_templates = self._load_analysis_templates()
    
    def _load_analysis_templates(self) -> Dict:
        """加载分析模板"""
        return {
            'project_analysis': {
                'structure': [
                    '🧠 【思维路线导航】',
                    '📚 项目发展历程', 
                    '🎯 设计哲学深度解析',
                    '🔧 核心技术实现',
                    '⚖️ 竞品对比分析',
                    '🔮 趋势洞察与未来展望',
                    '🔗 参考资料'
                ]
            },
            'trend_report': {
                'structure': [
                    '🎯 核心发现',
                    '📅 技术发展时间线',
                    '🔥 热门项目解析',
                    '📊 数据洞察',
                    '💡 个人观点',
                    '🔗 深度阅读'
                ]
            },
            'competitor_comparison': {
                'structure': [
                    '🎯 对比概览',
                    '📊 技术架构对比',
                    '⚡ 性能表现分析',
                    '🌍 生态系统对比',
                    '💼 商业模式分析',
                    '🏆 综合评价',
                    '🔗 参考资料'
                ]
            }
        }
    
    def analyze_github_project(self, repo_url: str, collected_data: Dict = None) -> TechAnalysis:
        """深度分析GitHub项目"""
        logger.info(f"开始分析项目: {repo_url}")
        
        # 提取仓库信息
        repo_info = self._extract_repo_info(repo_url)
        if not repo_info:
            return None
        
        # 收集项目相关信息
        project_data = self._collect_project_data(repo_info)
        
        # 生成分析内容
        analysis_content = self._generate_project_analysis(repo_info, project_data)
        
        # 生成洞察
        insights = self._generate_project_insights(repo_info, project_data)
        
        # 构建时间线
        timeline = self._build_project_timeline(repo_info, project_data)
        
        # 收集参考资料
        references = self._collect_project_references(repo_info, project_data)
        
        return TechAnalysis(
            title=f"{repo_info['name']} 技术深度解析",
            analysis_type="project_analysis",
            content=analysis_content,
            insights=insights,
            timeline=timeline,
            references=references,
            generated_at=datetime.now()
        )
    
    def _extract_repo_info(self, repo_url: str) -> Dict:
        """从GitHub URL提取仓库信息"""
        try:
            # 从URL提取owner和repo
            pattern = r'github\.com/([^/]+)/([^/]+)'
            match = re.search(pattern, repo_url)
            if not match:
                return None
            
            owner, repo = match.groups()
            
            # 调用GitHub API获取详细信息
            api_url = f"https://api.github.com/repos/{owner}/{repo}"
            response = requests.get(api_url)
            response.raise_for_status()
            
            repo_data = response.json()
            
            return {
                'owner': owner,
                'name': repo,
                'full_name': repo_data['full_name'],
                'description': repo_data.get('description', ''),
                'language': repo_data.get('language', ''),
                'stars': repo_data['stargazers_count'],
                'forks': repo_data['forks_count'],
                'created_at': repo_data['created_at'],
                'updated_at': repo_data['updated_at'],
                'topics': repo_data.get('topics', []),
                'license': repo_data.get('license', {}).get('name', 'Unknown') if repo_data.get('license') else 'Unknown'
            }
            
        except Exception as e:
            logger.error(f"获取仓库信息失败: {e}")
            return None
    
    def _collect_project_data(self, repo_info: Dict) -> Dict:
        """收集项目相关数据"""
        data = {
            'basic_info': repo_info,
            'releases': self._get_project_releases(repo_info),
            'contributors': self._get_top_contributors(repo_info),
            'issues_stats': self._get_issues_statistics(repo_info)
        }
        return data
    
    def _get_project_releases(self, repo_info: Dict) -> List[Dict]:
        """获取项目发布历史"""
        try:
            url = f"https://api.github.com/repos/{repo_info['full_name']}/releases"
            response = requests.get(url, params={'per_page': 10})
            response.raise_for_status()
            
            releases = []
            for release in response.json():
                releases.append({
                    'tag_name': release['tag_name'],
                    'name': release['name'],
                    'published_at': release['published_at'],
                    'body': release.get('body', '')[:200]  # 截取前200字符
                })
            
            return releases
            
        except Exception as e:
            logger.error(f"获取发布历史失败: {e}")
            return []
    
    def _get_top_contributors(self, repo_info: Dict) -> List[Dict]:
        """获取主要贡献者"""
        try:
            url = f"https://api.github.com/repos/{repo_info['full_name']}/contributors"
            response = requests.get(url, params={'per_page': 10})
            response.raise_for_status()
            
            contributors = []
            for contributor in response.json():
                contributors.append({
                    'login': contributor['login'],
                    'contributions': contributor['contributions'],
                    'avatar_url': contributor['avatar_url']
                })
            
            return contributors
            
        except Exception as e:
            logger.error(f"获取贡献者信息失败: {e}")
            return []
    
    def _get_issues_statistics(self, repo_info: Dict) -> Dict:
        """获取Issues统计信息"""
        try:
            # 获取开放Issues数量
            url = f"https://api.github.com/repos/{repo_info['full_name']}/issues"
            response = requests.get(url, params={'state': 'open', 'per_page': 1})
            
            stats = {
                'open_issues': repo_info.get('open_issues_count', 0),
                'recent_activity': response.headers.get('Link') is not None
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"获取Issues统计失败: {e}")
            return {}
    
    def _generate_project_analysis(self, repo_info: Dict, project_data: Dict) -> str:
        """生成项目深度分析内容"""
        
        # 基于模板生成分析内容
        analysis_parts = []
        
        # 思维路线导航
        navigation = f"""
## 🧠 【思维路线导航】

在深入探索 {repo_info['name']} 之前，我们先建立思考框架：

- **历史背景**：{repo_info['name']} 为什么会诞生？解决了什么问题？
- **设计哲学**：核心设计理念是什么？有哪些独特的技术选择？
- **技术实现**：关键技术是如何落地的？
- **竞争分析**：与同类项目相比有什么优势？
- **未来趋势**：项目的发展方向如何？

---
"""
        analysis_parts.append(navigation)
        
        # 项目发展历程
        timeline_section = f"""
## 📚 项目发展历程

### 🎯 基本信息
- **项目名称**：{repo_info['full_name']}
- **主要语言**：{repo_info['language']}
- **创建时间**：{repo_info['created_at'][:10]}
- **当前状态**：⭐ {repo_info['stars']:,} Stars，🍴 {repo_info['forks']:,} Forks
- **开源协议**：{repo_info['license']}

### 📅 重要里程碑
"""
        
        # 添加发布历史
        if project_data['releases']:
            timeline_section += "\n**主要版本发布**：\n"
            for release in project_data['releases'][:5]:
                timeline_section += f"- **{release['tag_name']}** ({release['published_at'][:10]}): {release['name']}\n"
        
        analysis_parts.append(timeline_section)
        
        # 设计哲学分析（这里需要基于项目特点生成）
        philosophy_section = f"""
## 🎯 设计哲学深度解析

### 核心设计理念
{repo_info['description']}

### 技术选择分析
- **主要技术栈**：{repo_info['language']}
- **项目标签**：{', '.join(repo_info['topics'][:5]) if repo_info['topics'] else '暂无标签'}

*（基于项目结构和代码分析的深度哲学解析需要进一步的代码审查和架构分析）*

---
"""
        analysis_parts.append(philosophy_section)
        
        return '\n'.join(analysis_parts)
    
    def _generate_project_insights(self, repo_info: Dict, project_data: Dict) -> List[str]:
        """生成项目洞察"""
        insights = []
        
        # 基于数据生成洞察
        if repo_info['stars'] > 10000:
            insights.append(f"⭐ 高关注度项目：{repo_info['stars']:,} stars表明该项目在社区中具有重要影响力")
        
        if repo_info['forks'] > repo_info['stars'] * 0.1:
            insights.append(f"🍴 活跃开发：Fork比例({repo_info['forks']/repo_info['stars']:.2%})表明开发者积极参与贡献")
        
        # 分析贡献者分布
        if project_data['contributors']:
            top_contributor = project_data['contributors'][0]
            contribution_ratio = top_contributor['contributions'] / sum(c['contributions'] for c in project_data['contributors'][:10])
            if contribution_ratio > 0.5:
                insights.append(f"👑 核心维护者：{top_contributor['login']} 贡献了 {contribution_ratio:.1%} 的代码，项目具有强中心化特征")
            else:
                insights.append(f"🤝 分布式开发：贡献相对分散，体现了健康的开源协作模式")
        
        return insights
    
    def _build_project_timeline(self, repo_info: Dict, project_data: Dict) -> List[Dict]:
        """构建项目时间线"""
        timeline = []
        
        # 创建时间
        timeline.append({
            'date': repo_info['created_at'][:10],
            'event': f"项目创建：{repo_info['full_name']} 在GitHub上创建",
            'type': 'creation'
        })
        
        # 重要版本发布
        for release in project_data['releases'][:3]:
            timeline.append({
                'date': release['published_at'][:10],
                'event': f"版本发布：{release['tag_name']} - {release['name']}",
                'type': 'release'
            })
        
        return sorted(timeline, key=lambda x: x['date'])
    
    def _collect_project_references(self, repo_info: Dict, project_data: Dict) -> List[str]:
        """收集项目参考资料"""
        references = []
        
        # GitHub仓库链接
        references.append(f"https://github.com/{repo_info['full_name']}")
        
        # 如果有官方文档，添加链接（这里可以扩展智能识别）
        if 'docs' in repo_info['topics'] or 'documentation' in repo_info['topics']:
            references.append(f"https://{repo_info['name']}.readthedocs.io")
        
        return references
    
    def generate_trend_report(self, collected_data: Dict) -> TechAnalysis:
        """生成技术趋势报告"""
        logger.info("生成技术趋势报告")
        
        # 分析趋势数据
        trends = self._analyze_trends(collected_data)
        
        # 生成报告内容
        content = self._format_trend_report(trends)
        
        return TechAnalysis(
            title=f"技术趋势调研报告 - {datetime.now().strftime('%Y年%m月')}",
            analysis_type="trend_report",
            content=content,
            insights=trends['insights'],
            timeline=trends['timeline'],
            references=trends['references'],
            generated_at=datetime.now()
        )
    
    def _analyze_trends(self, collected_data: Dict) -> Dict:
        """分析技术趋势"""
        trends = {
            'hot_topics': [],
            'emerging_technologies': [],
            'insights': [],
            'timeline': [],
            'references': []
        }
        
        # 分析GitHub趋势项目
        if 'github_trending' in collected_data:
            github_data = collected_data['github_trending']
            
            # 统计热门技术栈
            languages = {}
            topics = {}
            
            for project in github_data:
                # 统计编程语言
                lang = project.get('metrics', {}).get('language', 'Unknown')
                languages[lang] = languages.get(lang, 0) + 1
                
                # 统计话题标签
                project_tags = project.get('tags', [])
                for tag in project_tags:
                    topics[tag] = topics.get(tag, 0) + 1
            
            # 生成洞察
            if languages:
                top_lang = max(languages.items(), key=lambda x: x[1])
                trends['insights'].append(f"🔥 热门语言：{top_lang[0]} 在趋势项目中占主导地位（{top_lang[1]}个项目）")
            
            if topics:
                top_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)[:3]
                trends['insights'].append(f"📈 热门话题：{', '.join([t[0] for t in top_topics])} 成为开发者关注焦点")
        
        # 分析Hacker News讨论
        if 'hackernews' in collected_data:
            hn_data = collected_data['hackernews']
            
            # 统计讨论热度
            high_engagement = [post for post in hn_data if post.get('metrics', {}).get('comments', 0) > 50]
            if high_engagement:
                trends['insights'].append(f"💬 社区热议：{len(high_engagement)} 个技术话题引发激烈讨论")
        
        return trends
    
    def _format_trend_report(self, trends: Dict) -> str:
        """格式化趋势报告"""
        content_parts = []
        
        # 报告头部
        header = f"""
# 📈 技术趋势调研报告 - {datetime.now().strftime('%Y年%m月')}

## 🎯 核心发现

以下是本期技术生态的关键发现：
"""
        content_parts.append(header)
        
        # 洞察列表
        if trends['insights']:
            insights_section = "\n### 💡 主要洞察\n\n"
            for i, insight in enumerate(trends['insights'], 1):
                insights_section += f"{i}. {insight}\n"
            content_parts.append(insights_section)
        
        return '\n'.join(content_parts)
    
    def save_analysis(self, analysis: TechAnalysis, output_dir: str = "output") -> str:
        """保存分析结果"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = analysis.generated_at.strftime("%Y%m%d_%H%M%S")
        filename = f"{analysis.analysis_type}_{timestamp}.md"
        filepath = os.path.join(output_dir, filename)
        
        # 生成完整的Markdown内容
        full_content = f"""# {analysis.title}

{analysis.content}

## 💡 关键洞察

{chr(10).join(f'- {insight}' for insight in analysis.insights)}

## 📅 时间线

{chr(10).join(f"- **{event['date']}**: {event['event']}" for event in analysis.timeline)}

## 🔗 参考资料

{chr(10).join(f'- {ref}' for ref in analysis.references)}

---
*生成时间：{analysis.generated_at.strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        logger.info(f"分析结果已保存到: {filepath}")
        return filepath

if __name__ == "__main__":
    # 示例使用
    analyzer = TechAnalyzer()
    
    # 模拟收集的数据
    sample_data = {
        'github_trending': [
            {
                'title': 'microsoft/garnet',
                'metrics': {'language': 'C#', 'stars': 8500},
                'tags': ['redis', 'cache', 'performance']
            }
        ]
    }
    
    # 生成趋势报告
    trend_analysis = analyzer.generate_trend_report(sample_data)
    output_file = analyzer.save_analysis(trend_analysis)
    print(f"趋势报告已生成: {output_file}")