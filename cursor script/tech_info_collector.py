#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技术信息智能收集器
支持GitHub趋势、技术新闻、社区讨论等多源信息收集
"""

import requests
import json
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass
import yaml
import os

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class TechInfo:
    """技术信息数据结构"""
    title: str
    url: str
    source: str
    category: str
    timestamp: datetime
    description: str = ""
    tags: List[str] = None
    metrics: Dict = None

class TechInfoCollector:
    """技术信息收集器"""
    
    def __init__(self, config_path: str = "config/workflow_config.yaml"):
        self.config = self._load_config(config_path)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TechInfoCollector/1.0 (https://github.com/your-repo)'
        })
    
    def _load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        else:
            # 默认配置
            return {
                'information_sources': {
                    'primary': ['github_trending', 'hackernews'],
                    'secondary': ['infoq_cn'],
                    'custom': []
                },
                'analysis_focus': ['architecture_design', 'performance_optimization'],
                'output_preferences': {
                    'language': 'zh-CN',
                    'style': 'deep_analysis'
                }
            }
    
    def collect_github_trending(self, timeframe: str = "weekly", language: str = None) -> List[TechInfo]:
        """收集GitHub趋势项目"""
        logger.info(f"收集GitHub趋势项目 - 时间范围: {timeframe}")
        
        # GitHub Trending API (非官方)
        url = "https://api.github.com/search/repositories"
        
        # 计算日期范围
        if timeframe == "daily":
            since = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        elif timeframe == "weekly":
            since = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        else:
            since = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        params = {
            'q': f'created:>{since}',
            'sort': 'stars',
            'order': 'desc',
            'per_page': 10
        }
        
        if language:
            params['q'] += f' language:{language}'
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            trending_repos = []
            for item in data.get('items', []):
                tech_info = TechInfo(
                    title=item['full_name'],
                    url=item['html_url'],
                    source='github_trending',
                    category='open_source_project',
                    timestamp=datetime.now(),
                    description=item.get('description', ''),
                    tags=item.get('topics', []),
                    metrics={
                        'stars': item['stargazers_count'],
                        'forks': item['forks_count'],
                        'language': item.get('language', 'Unknown')
                    }
                )
                trending_repos.append(tech_info)
            
            logger.info(f"成功收集到 {len(trending_repos)} 个趋势项目")
            return trending_repos
            
        except Exception as e:
            logger.error(f"收集GitHub趋势时出错: {e}")
            return []
    
    def collect_hackernews_posts(self, max_posts: int = 20) -> List[TechInfo]:
        """收集Hacker News技术相关帖子"""
        logger.info("收集Hacker News技术帖子")
        
        try:
            # 获取热门故事ID
            top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
            response = self.session.get(top_stories_url)
            response.raise_for_status()
            story_ids = response.json()[:max_posts]
            
            tech_posts = []
            for story_id in story_ids:
                # 获取具体故事信息
                story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                story_response = self.session.get(story_url)
                if story_response.status_code == 200:
                    story_data = story_response.json()
                    
                    # 过滤技术相关内容
                    if self._is_tech_related(story_data.get('title', '')):
                        tech_info = TechInfo(
                            title=story_data.get('title', ''),
                            url=story_data.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                            source='hackernews',
                            category='tech_discussion',
                            timestamp=datetime.fromtimestamp(story_data.get('time', 0)),
                            description=story_data.get('text', ''),
                            metrics={
                                'score': story_data.get('score', 0),
                                'comments': story_data.get('descendants', 0)
                            }
                        )
                        tech_posts.append(tech_info)
                
                # 避免请求过于频繁
                time.sleep(0.1)
            
            logger.info(f"成功收集到 {len(tech_posts)} 个HN技术帖子")
            return tech_posts
            
        except Exception as e:
            logger.error(f"收集Hacker News帖子时出错: {e}")
            return []
    
    def _is_tech_related(self, title: str) -> bool:
        """判断标题是否与技术相关"""
        tech_keywords = [
            'python', 'javascript', 'rust', 'go', 'java', 'typescript',
            'docker', 'kubernetes', 'redis', 'postgresql', 'mongodb',
            'react', 'vue', 'angular', 'nodejs', 'api', 'database',
            'ai', 'ml', 'machine learning', 'deep learning', 'llm',
            'cloud', 'aws', 'azure', 'gcp', 'microservices',
            'open source', 'github', 'framework', 'library',
            'performance', 'optimization', 'security', 'devops'
        ]
        
        title_lower = title.lower()
        return any(keyword in title_lower for keyword in tech_keywords)
    
    def collect_all_sources(self) -> Dict[str, List[TechInfo]]:
        """收集所有配置的信息源"""
        all_info = {}
        
        # 收集一级信息源
        for source in self.config['information_sources']['primary']:
            if source == 'github_trending':
                all_info['github_trending'] = self.collect_github_trending()
            elif source == 'hackernews':
                all_info['hackernews'] = self.collect_hackernews_posts()
        
        return all_info
    
    def save_collected_data(self, data: Dict[str, List[TechInfo]], output_dir: str = "data"):
        """保存收集的数据"""
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 转换为可序列化的格式
        serializable_data = {}
        for source, info_list in data.items():
            serializable_data[source] = []
            for info in info_list:
                info_dict = {
                    'title': info.title,
                    'url': info.url,
                    'source': info.source,
                    'category': info.category,
                    'timestamp': info.timestamp.isoformat(),
                    'description': info.description,
                    'tags': info.tags or [],
                    'metrics': info.metrics or {}
                }
                serializable_data[source].append(info_dict)
        
        output_file = os.path.join(output_dir, f"tech_info_{timestamp}.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(serializable_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"数据已保存到: {output_file}")
        return output_file

if __name__ == "__main__":
    # 示例使用
    collector = TechInfoCollector()
    
    print("🚀 开始收集技术信息...")
    collected_data = collector.collect_all_sources()
    
    print("\n📊 收集结果统计:")
    for source, info_list in collected_data.items():
        print(f"  {source}: {len(info_list)} 条信息")
    
    # 保存数据
    output_file = collector.save_collected_data(collected_data)
    print(f"\n💾 数据已保存: {output_file}")