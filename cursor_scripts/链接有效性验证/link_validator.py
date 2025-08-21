#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Redis设计哲学文档链接验证器
检查所有链接的有效性和内容相关性
"""

import requests
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import time
import json

class LinkValidator:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.results = {}
        
    def check_link(self, url, description):
        """检查单个链接的有效性和内容相关性"""
        print(f"正在检查: {url}")
        print(f"描述: {description}")
        
        try:
            # 设置超时时间
            response = self.session.get(url, timeout=15, allow_redirects=True)
            
            if response.status_code == 200:
                # 解析HTML内容
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 提取文本内容
                text_content = soup.get_text()
                
                # 分析内容相关性
                relevance_score = self.analyze_relevance(text_content, description)
                
                result = {
                    'status': 'valid',
                    'status_code': response.status_code,
                    'content_length': len(text_content),
                    'relevance_score': relevance_score,
                    'title': soup.title.string if soup.title else 'No title',
                    'is_relevant': relevance_score > 0.3
                }
                
                print(f"✓ 链接有效 (状态码: {response.status_code})")
                print(f"  相关性评分: {relevance_score:.2f}")
                print(f"  页面标题: {result['title']}")
                
            else:
                result = {
                    'status': 'error',
                    'status_code': response.status_code,
                    'error': f'HTTP {response.status_code}'
                }
                print(f"✗ 链接无效 (状态码: {response.status_code})")
                
        except requests.exceptions.RequestException as e:
            result = {
                'status': 'error',
                'error': str(e)
            }
            print(f"✗ 请求失败: {e}")
        
        print("-" * 50)
        return result
    
    def analyze_relevance(self, text, description):
        """分析内容相关性"""
        # Redis相关关键词
        redis_keywords = [
            'redis', 'antirez', 'memory', 'cache', 'database', 'performance',
            'i/o', 'multiplexing', 'epoll', 'event loop', 'single thread',
            'persistence', 'rdb', 'aof', 'data structure'
        ]
        
        # 设计哲学相关关键词
        philosophy_keywords = [
            'design', 'philosophy', 'architecture', 'principle', 'approach',
            'strategy', 'methodology', 'thinking', 'concept', 'idea'
        ]
        
        text_lower = text.lower()
        
        # 计算关键词匹配度
        redis_score = sum(1 for keyword in redis_keywords if keyword in text_lower)
        philosophy_score = sum(1 for keyword in philosophy_keywords if keyword in text_lower)
        
        # 计算总相关性评分 (0-1)
        total_score = (redis_score + philosophy_score) / (len(redis_keywords) + len(philosophy_keywords))
        
        return total_score
    
    def find_links_in_markdown(self, file_path):
        """从Markdown文件中提取链接"""
        links = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 使用正则表达式匹配Markdown链接
            link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
            matches = re.findall(link_pattern, content)
            
            for description, url in matches:
                links.append({
                    'description': description,
                    'url': url
                })
                
        except Exception as e:
            print(f"读取文件失败: {e}")
            
        return links
    
    def validate_all_links(self, file_path):
        """验证文件中的所有链接"""
        print("开始验证Redis设计哲学文档中的链接...")
        print("=" * 60)
        
        links = self.find_links_in_markdown(file_path)
        print(f"找到 {len(links)} 个链接")
        print()
        
        for i, link in enumerate(links, 1):
            print(f"[{i}/{len(links)}]")
            result = self.check_link(link['url'], link['description'])
            self.results[link['url']] = result
            time.sleep(1)  # 避免请求过于频繁
        
        self.generate_report()
    
    def generate_report(self):
        """生成验证报告"""
        print("\n" + "=" * 60)
        print("链接验证报告")
        print("=" * 60)
        
        valid_links = []
        invalid_links = []
        relevant_links = []
        
        for url, result in self.results.items():
            if result['status'] == 'valid':
                valid_links.append(url)
                if result.get('is_relevant', False):
                    relevant_links.append(url)
            else:
                invalid_links.append(url)
        
        print(f"总链接数: {len(self.results)}")
        print(f"有效链接: {len(valid_links)}")
        print(f"无效链接: {len(invalid_links)}")
        print(f"相关内容: {len(relevant_links)}")
        
        if invalid_links:
            print(f"\n无效链接列表:")
            for url in invalid_links:
                print(f"  - {url}")
                print(f"    错误: {self.results[url].get('error', 'Unknown error')}")
        
        if relevant_links:
            print(f"\n高相关性链接:")
            for url in relevant_links:
                score = self.results[url].get('relevance_score', 0)
                print(f"  - {url} (相关性: {score:.2f})")
        
        # 保存结果到JSON文件
        with open('link_validation_results.json', 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n详细结果已保存到: link_validation_results.json")

def main():
    validator = LinkValidator()
    
    # 验证Redis大事件文档
    markdown_file = "../Stack/Redis/Redis大事件（8.0回归开源）.md"
    validator.validate_all_links(markdown_file)

if __name__ == "__main__":
    main()
