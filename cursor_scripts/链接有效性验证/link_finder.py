#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Redis设计哲学文档链接查找器
手动收集和验证有效链接
"""

import requests
from bs4 import BeautifulSoup
import json
import time

class LinkFinder:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # 预设的候选链接
        self.candidate_links = {
            "1.1": [  # Redis诞生背景
                "https://redis.io/",
                "https://redis.io/docs/",
                "https://github.com/redis/redis",
                "https://stackoverflow.com/questions/10558465/memcached-vs-redis",
                "http://antirez.com/latest/0"
            ],
            "1.2": [  # Redis设计目标
                "https://redis.io/docs/about/",
                "https://github.com/redis/redis/blob/unstable/README.md",
                "http://antirez.com/news/56",
                "https://redis.com/redis-enterprise/",
                "https://redis.io/docs/getting-started/"
            ],
            "2.1": [  # Redis核心哲学
                "https://redis.io/docs/reference/optimization/",
                "http://antirez.com/news/56",
                "https://redis.io/docs/getting-started/faq/",
                "https://github.com/redis/redis/blob/unstable/src/server.c",
                "https://redis.com/blog/redis-performance/"
            ],
            "3.1": [  # Redis I/O模型
                "https://redis.io/docs/reference/optimization/io-multiplexing/",
                "https://man7.org/linux/man-pages/man7/epoll.7.html",
                "https://github.com/redis/redis/blob/unstable/src/ae.c",
                "https://redis.io/docs/reference/clients/",
                "http://antirez.com/news/65"
            ],
            "3.2": [  # Redis线程模型
                "https://redis.io/docs/reference/optimization/io-threads/",
                "http://antirez.com/news/126",
                "https://github.com/redis/redis/releases/tag/6.0.0",
                "https://redis.io/docs/getting-started/faq/#redis-is-single-threaded-how-can-it-be-so-fast",
                "https://redis.com/blog/diving-into-redis-6/"
            ],
            "3.3": [  # Redis数据存储
                "https://redis.io/docs/management/persistence/",
                "https://redis.io/docs/management/persistence/rdb/",
                "https://redis.io/docs/management/persistence/aof/",
                "https://github.com/redis/redis/blob/unstable/src/rdb.c",
                "https://redis.com/blog/redis-persistence-demystified/"
            ],
            "summary": [  # 总结
                "https://redis.io/docs/about/",
                "http://antirez.com/news/56",
                "https://github.com/redis/redis",
                "https://redis.com/redis-enterprise/technology/",
                "https://redis.io/docs/"
            ]
        }
    
    def check_link_validity(self, url, description=""):
        """检查单个链接的有效性和相关性"""
        print(f"正在检查: {url}")
        
        try:
            response = self.session.get(url, timeout=15, allow_redirects=True)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                text_content = soup.get_text()
                
                relevance_score = self.analyze_relevance(text_content)
                title = soup.title.string if soup.title else 'No title'
                
                result = {
                    'status': 'valid',
                    'status_code': response.status_code,
                    'relevance_score': relevance_score,
                    'title': title.strip(),
                    'is_relevant': relevance_score > 0.15,
                    'content_length': len(text_content),
                    'url': url
                }
                
                print(f"✓ 链接有效 (状态码: {response.status_code})")
                print(f"  相关性评分: {relevance_score:.2f}")
                print(f"  页面标题: {title.strip()}")
                
                return result
            else:
                print(f"✗ 链接无效 (状态码: {response.status_code})")
                return {'status': 'error', 'status_code': response.status_code, 'url': url}
                
        except Exception as e:
            print(f"✗ 请求失败: {e}")
            return {'status': 'error', 'error': str(e), 'url': url}
    
    def analyze_relevance(self, text):
        """分析内容相关性"""
        redis_keywords = [
            'redis', 'antirez', 'memory', 'cache', 'database', 'performance',
            'i/o', 'multiplexing', 'epoll', 'event loop', 'single thread',
            'persistence', 'rdb', 'aof', 'data structure', 'nosql', 'key-value'
        ]
        
        design_keywords = [
            'design', 'philosophy', 'architecture', 'principle', 'approach',
            'strategy', 'methodology', 'thinking', 'concept', 'pattern'
        ]
        
        text_lower = text.lower()
        
        redis_score = sum(1 for keyword in redis_keywords if keyword in text_lower)
        design_score = sum(1 for keyword in design_keywords if keyword in text_lower)
        
        total_score = (redis_score + design_score) / (len(redis_keywords) + len(design_keywords))
        
        return min(total_score, 1.0)
    
    def find_valid_links_for_all_sections(self):
        """为所有章节查找有效链接"""
        sections = {
            "1.1": "Redis诞生背景",
            "1.2": "Redis设计目标", 
            "2.1": "Redis核心哲学",
            "3.1": "Redis I/O模型",
            "3.2": "Redis线程模型",
            "3.3": "Redis数据存储",
            "summary": "Redis设计哲学总结"
        }
        
        all_results = {}
        
        for section_id, topic in sections.items():
            print(f"\n{'='*60}")
            print(f"处理章节 {section_id}: {topic}")
            print('='*60)
            
            valid_links = []
            candidate_urls = self.candidate_links.get(section_id, [])
            
            for url in candidate_urls:
                result = self.check_link_validity(url, topic)
                if result['status'] == 'valid':
                    valid_links.append(result)
                
                print("-" * 50)
                time.sleep(1)  # 避免请求过于频繁
            
            # 按相关性排序，取前5个
            valid_links.sort(key=lambda x: x['relevance_score'], reverse=True)
            all_results[section_id] = {
                'topic': topic,
                'valid_links': valid_links[:5]
            }
            
            print(f"章节 {section_id} 找到 {len(valid_links)} 个有效链接")
        
        return all_results
    
    def generate_markdown_output(self, results):
        """生成Markdown格式的输出"""
        markdown_lines = ["# Redis设计哲学文档 - 验证后的参考资料\n"]
        
        for section_id, data in results.items():
            markdown_lines.append(f"## 章节 {section_id}: {data['topic']}\n")
            markdown_lines.append("*   **参考资料：**")
            
            for link in data['valid_links']:
                title = link['title']
                url = link['url']
                relevance = link['relevance_score']
                
                # 生成简短描述
                if 'redis.io' in url:
                    desc = "Redis官方文档"
                elif 'antirez.com' in url:
                    desc = "Redis创造者antirez的博客"
                elif 'github.com' in url:
                    desc = "Redis官方源码仓库"
                elif 'stackoverflow.com' in url:
                    desc = "Stack Overflow技术讨论"
                elif 'man7.org' in url:
                    desc = "Linux官方文档"
                else:
                    desc = "相关技术资料"
                
                markdown_lines.append(f"    *   [{title}]({url}) - {desc}")
            
            if not data['valid_links']:
                markdown_lines.append("    *   暂无有效链接")
            
            markdown_lines.append("")
        
        return '\n'.join(markdown_lines)

def main():
    print("Redis设计哲学文档链接查找器")
    print("="*60)
    
    finder = LinkFinder()
    
    # 查找所有章节的有效链接
    results = finder.find_valid_links_for_all_sections()
    
    # 生成报告
    print(f"\n{'='*60}")
    print("链接验证报告")
    print('='*60)
    
    total_valid = sum(len(data['valid_links']) for data in results.values())
    total_relevant = sum(len([link for link in data['valid_links'] if link['is_relevant']]) 
                        for data in results.values())
    
    print(f"总共验证了 {sum(len(finder.candidate_links[k]) for k in finder.candidate_links)} 个候选链接")
    print(f"找到 {total_valid} 个有效链接")
    print(f"其中 {total_relevant} 个高相关性链接")
    
    # 保存结果
    with open('validated_links.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # 生成Markdown
    markdown_content = finder.generate_markdown_output(results)
    with open('validated_references.md', 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"\n结果已保存到:")
    print(f"- validated_links.json")
    print(f"- validated_references.md")

if __name__ == "__main__":
    main()
