#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Redis设计哲学文档链接替换器
自动搜索并验证新的有效链接来替换失效链接
"""

import requests
import re
from urllib.parse import urlparse, quote
from bs4 import BeautifulSoup
import time
import json
from googlesearch import search
import random

class LinkReplacer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.results = {}
        
        # 章节主题关键词
        self.section_keywords = {
            "1.1": ["redis history", "redis origin", "redis birth", "memcached vs redis", "2009 database"],
            "1.2": ["redis design goals", "redis objectives", "redis purpose", "antirez redis"],
            "2.1": ["redis performance", "redis philosophy", "lightweight computation", "I/O optimization"],
            "3.1": ["redis I/O multiplexing", "epoll redis", "event loop redis", "redis networking"],
            "3.2": ["redis single thread", "redis threading model", "redis 6.0 multithreading"],
            "3.3": ["redis persistence", "redis RDB", "redis AOF", "redis durability"],
            "summary": ["redis design philosophy", "redis architecture", "redis principles"]
        }
        
    def check_link_validity(self, url, description):
        """检查单个链接的有效性和相关性"""
        try:
            response = self.session.get(url, timeout=15, allow_redirects=True)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                text_content = soup.get_text()
                
                relevance_score = self.analyze_relevance(text_content, description)
                
                return {
                    'status': 'valid',
                    'status_code': response.status_code,
                    'relevance_score': relevance_score,
                    'title': soup.title.string if soup.title else 'No title',
                    'is_relevant': relevance_score > 0.2,
                    'content_length': len(text_content)
                }
            else:
                return {'status': 'error', 'status_code': response.status_code}
                
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def analyze_relevance(self, text, description):
        """分析内容相关性"""
        redis_keywords = [
            'redis', 'antirez', 'memory', 'cache', 'database', 'performance',
            'i/o', 'multiplexing', 'epoll', 'event loop', 'single thread',
            'persistence', 'rdb', 'aof', 'data structure', 'nosql'
        ]
        
        philosophy_keywords = [
            'design', 'philosophy', 'architecture', 'principle', 'approach',
            'strategy', 'methodology', 'thinking', 'concept', 'pattern'
        ]
        
        text_lower = text.lower()
        description_lower = description.lower()
        
        # 计算关键词匹配度
        redis_score = sum(1 for keyword in redis_keywords if keyword in text_lower)
        philosophy_score = sum(1 for keyword in philosophy_keywords if keyword in text_lower)
        
        # 描述匹配度
        desc_words = description_lower.split()
        desc_score = sum(1 for word in desc_words if word in text_lower and len(word) > 3)
        
        total_score = (redis_score + philosophy_score + desc_score * 2) / (len(redis_keywords) + len(philosophy_keywords) + len(desc_words) * 2)
        
        return min(total_score, 1.0)
    
    def search_alternative_links(self, section_id, topic, num_results=10):
        """为特定主题搜索替代链接"""
        print(f"正在为章节 {section_id} 搜索主题: {topic}")
        
        keywords = self.section_keywords.get(section_id, [topic])
        valid_links = []
        
        for keyword in keywords[:2]:  # 限制搜索词数量
            try:
                search_query = f"{keyword} site:redis.io OR site:github.com OR site:stackoverflow.com OR site:antirez.com OR site:redislabs.com"
                print(f"搜索: {search_query}")
                
                search_results = list(search(search_query, num=5, stop=5, pause=2))
                
                for url in search_results:
                    if any(domain in url for domain in ['redis.io', 'github.com', 'stackoverflow.com', 'antirez.com', 'redislabs.com']):
                        result = self.check_link_validity(url, topic)
                        if result['status'] == 'valid' and result['is_relevant']:
                            valid_links.append({
                                'url': url,
                                'title': result['title'],
                                'relevance': result['relevance_score'],
                                'keyword': keyword
                            })
                            print(f"✓ 找到有效链接: {url} (相关性: {result['relevance_score']:.2f})")
                        
                        if len(valid_links) >= num_results:
                            break
                
                time.sleep(random.uniform(2, 4))  # 随机延迟避免被限制
                
            except Exception as e:
                print(f"搜索出错: {e}")
                continue
        
        # 按相关性排序
        valid_links.sort(key=lambda x: x['relevance'], reverse=True)
        return valid_links[:5]  # 返回前5个最相关的链接
    
    def generate_replacement_links(self):
        """为每个章节生成替代链接"""
        sections = {
            "1.1": "Redis诞生背景",
            "1.2": "Redis设计目标", 
            "2.1": "Redis核心哲学",
            "3.1": "Redis I/O模型",
            "3.2": "Redis线程模型",
            "3.3": "Redis数据存储",
            "summary": "Redis设计哲学总结"
        }
        
        all_recommendations = {}
        
        for section_id, topic in sections.items():
            print(f"\n{'='*60}")
            print(f"处理章节 {section_id}: {topic}")
            print('='*60)
            
            links = self.search_alternative_links(section_id, topic)
            all_recommendations[section_id] = {
                'topic': topic,
                'links': links
            }
            
            print(f"为章节 {section_id} 找到 {len(links)} 个有效链接")
            time.sleep(3)  # 章节间延迟
        
        return all_recommendations
    
    def create_markdown_references(self, recommendations):
        """生成Markdown格式的参考资料"""
        markdown_output = []
        
        for section_id, data in recommendations.items():
            markdown_output.append(f"\n### 章节 {section_id}: {data['topic']}\n")
            markdown_output.append("*   **参考资料：**")
            
            for i, link in enumerate(data['links'], 1):
                title = link['title'].strip()
                url = link['url']
                relevance = link['relevance']
                keyword = link['keyword']
                
                markdown_output.append(f"    *   [{title}]({url}) - 相关性: {relevance:.2f} (关键词: {keyword})")
            
            if not data['links']:
                markdown_output.append("    *   暂未找到合适的替代链接")
        
        return '\n'.join(markdown_output)

def main():
    print("Redis设计哲学文档链接替换器")
    print("="*60)
    
    replacer = LinkReplacer()
    
    # 搜索并验证新链接
    recommendations = replacer.generate_replacement_links()
    
    # 生成报告
    print(f"\n{'='*60}")
    print("链接推荐报告")
    print('='*60)
    
    total_links = sum(len(data['links']) for data in recommendations.values())
    print(f"总共找到 {total_links} 个有效替代链接")
    
    # 保存结果
    with open('link_recommendations.json', 'w', encoding='utf-8') as f:
        json.dump(recommendations, f, indent=2, ensure_ascii=False)
    
    # 生成Markdown格式
    markdown_refs = replacer.create_markdown_references(recommendations)
    with open('recommended_references.md', 'w', encoding='utf-8') as f:
        f.write("# Redis设计哲学文档 - 推荐参考资料\n")
        f.write(markdown_refs)
    
    print(f"\n详细结果已保存到:")
    print(f"- link_recommendations.json")
    print(f"- recommended_references.md")

if __name__ == "__main__":
    main()
