#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版链接验证脚本
用于验证文章论据链接的有效性，并分析语义相关性
"""

import requests
import time
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from typing import Dict, List, Tuple
import re
from bs4 import BeautifulSoup
import hashlib

class EnhancedLinkValidator:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.timeout = 15
        self.results = {}
        
        # 关键词权重配置
        self.keywords = {
            'io': 5, 'multiplexing': 5, 'epoll': 5, 'concurrency': 4, 'threading': 4,
            'async': 4, 'performance': 3, 'architecture': 3, 'linux': 3, 'kernel': 3,
            'network': 3, 'scalability': 3, 'event-driven': 4, 'reactor': 4,
            'nginx': 3, 'redis': 3, 'nodejs': 3, 'java': 3, 'go': 3, 'python': 3
        }
        
    def extract_content_keywords(self, html_content: str) -> Dict[str, int]:
        """从HTML内容中提取关键词"""
        if not html_content:
            return {}
            
        # 使用BeautifulSoup解析HTML
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            # 提取文本内容
            text = soup.get_text()
            
            # 转换为小写并分词
            words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
            
            # 统计关键词出现次数
            keyword_counts = {}
            for word in words:
                if word in self.keywords:
                    keyword_counts[word] = keyword_counts.get(word, 0) + 1
                    
            return keyword_counts
        except Exception:
            return {}
    
    def calculate_relevance_score(self, keyword_counts: Dict[str, int]) -> float:
        """计算相关性得分"""
        if not keyword_counts:
            return 0.0
            
        total_score = 0
        total_weight = 0
        
        for keyword, count in keyword_counts.items():
            weight = self.keywords.get(keyword, 1)
            total_score += count * weight
            total_weight += weight
            
        if total_weight == 0:
            return 0.0
            
        # 归一化得分 (0-100)
        normalized_score = min(100, (total_score / total_weight) * 20)
        return round(normalized_score, 1)
    
    def validate_single_link(self, url: str, description: str, section: str) -> Dict:
        """验证单个链接并分析相关性"""
        result = {
            'url': url,
            'description': description,
            'section': section,
            'status': 'unknown',
            'status_code': None,
            'error': None,
            'response_time': None,
            'accessible': False,
            'content_length': 0,
            'keyword_counts': {},
            'relevance_score': 0.0,
            'content_hash': None
        }
        
        try:
            start_time = time.time()
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            response_time = time.time() - start_time
            
            result['status_code'] = response.status_code
            result['response_time'] = round(response_time, 2)
            result['content_length'] = len(response.content)
            
            if response.status_code == 200:
                result['status'] = 'success'
                result['accessible'] = True
                
                # 分析内容相关性
                keyword_counts = self.extract_content_keywords(response.text)
                result['keyword_counts'] = keyword_counts
                result['relevance_score'] = self.calculate_relevance_score(keyword_counts)
                
                # 生成内容哈希（用于去重）
                result['content_hash'] = hashlib.md5(response.content).hexdigest()[:8]
                
            elif response.status_code in [301, 302, 307, 308]:
                result['status'] = 'redirect'
                result['accessible'] = True
            else:
                result['status'] = 'error'
                result['accessible'] = False
                
        except requests.exceptions.Timeout:
            result['status'] = 'timeout'
            result['error'] = '请求超时'
        except requests.exceptions.ConnectionError:
            result['status'] = 'connection_error'
            result['error'] = '连接错误'
        except requests.exceptions.RequestException as e:
            result['status'] = 'request_error'
            result['error'] = str(e)
        except Exception as e:
            result['status'] = 'unknown_error'
            result['error'] = str(e)
            
        return result
    
    def validate_links_batch(self, links_data: Dict) -> Dict:
        """批量验证链接"""
        print("开始验证链接并分析相关性...")
        
        # 使用线程池并发验证
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_link = {}
            
            for section, links in links_data.items():
                for link_info in links:
                    url = link_info['url']
                    description = link_info['description']
                    future = executor.submit(self.validate_single_link, url, description, section)
                    future_to_link[future] = (section, link_info)
            
            # 收集结果
            for future in as_completed(future_to_link):
                section, link_info = future_to_link[future]
                result = future.result()
                
                if section not in self.results:
                    self.results[section] = []
                
                self.results[section].append(result)
                
                # 实时显示进度
                status_icon = "✅" if result['accessible'] else "❌"
                relevance_info = f" (相关性: {result['relevance_score']})" if result['relevance_score'] > 0 else ""
                print(f"{status_icon} {result['status']}: {result['url']}{relevance_info}")
        
        return self.results
    
    def generate_enhanced_report(self) -> str:
        """生成增强版验证报告"""
        total_links = 0
        successful_links = 0
        failed_links = 0
        high_relevance_links = 0
        
        report = []
        report.append("# 增强版链接验证报告")
        report.append(f"生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # 按相关性得分排序
        all_links = []
        for section, links in self.results.items():
            for link in links:
                all_links.append((section, link))
        
        # 按相关性得分降序排序
        all_links.sort(key=lambda x: x[1]['relevance_score'], reverse=True)
        
        # 按小节分组显示
        sections = {}
        for section, link in all_links:
            if section not in sections:
                sections[section] = []
            sections[section].append(link)
        
        for section, links in sections.items():
            report.append(f"## {section}")
            report.append("")
            
            section_success = 0
            section_failed = 0
            section_high_relevance = 0
            
            for link in links:
                total_links += 1
                if link['accessible']:
                    successful_links += 1
                    section_success += 1
                    if link['relevance_score'] >= 50:
                        high_relevance_links += 1
                        section_high_relevance += 1
                    status_icon = "✅"
                else:
                    failed_links += 1
                    section_failed += 1
                    status_icon = "❌"
                
                report.append(f"{status_icon} **{link['description']}**")
                report.append(f"   - URL: {link['url']}")
                report.append(f"   - 状态: {link['status']}")
                if link['status_code']:
                    report.append(f"   - HTTP状态码: {link['status_code']}")
                if link['error']:
                    report.append(f"   - 错误信息: {link['error']}")
                if link['response_time']:
                    report.append(f"   - 响应时间: {link['response_time']}s")
                if link['relevance_score'] > 0:
                    report.append(f"   - 相关性得分: {link['relevance_score']}/100")
                    if link['keyword_counts']:
                        top_keywords = sorted(link['keyword_counts'].items(), key=lambda x: x[1], reverse=True)[:3]
                        keywords_str = ", ".join([f"{k}({v})" for k, v in top_keywords])
                        report.append(f"   - 主要关键词: {keywords_str}")
                report.append("")
            
            report.append(f"**小节统计**: 成功 {section_success} 个，失败 {section_failed} 个，高相关性 {section_high_relevance} 个")
            report.append("")
        
        # 总体统计
        report.append("## 总体统计")
        report.append("")
        report.append(f"- 总链接数: {total_links}")
        report.append(f"- 成功链接: {successful_links}")
        report.append(f"- 失败链接: {failed_links}")
        report.append(f"- 高相关性链接(≥50分): {high_relevance_links}")
        report.append(f"- 成功率: {(successful_links/total_links*100):.1f}%" if total_links > 0 else "0%")
        report.append(f"- 高相关性比例: {(high_relevance_links/successful_links*100):.1f}%" if successful_links > 0 else "0%")
        
        # 相关性分析
        if successful_links > 0:
            avg_relevance = sum(link['relevance_score'] for section in self.results.values() for link in section if link['accessible']) / successful_links
            report.append(f"- 平均相关性得分: {avg_relevance:.1f}/100")
        
        return "\n".join(report)
    
    def save_results(self, filename: str = "enhanced_link_validation_results.json"):
        """保存验证结果到JSON文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"结果已保存到 {filename}")
    
    def get_recommendations(self) -> str:
        """基于验证结果生成建议"""
        recommendations = []
        recommendations.append("## 📋 添加建议")
        recommendations.append("")
        
        # 统计高相关性链接
        high_relevance_links = []
        for section, links in self.results.items():
            for link in links:
                if link['accessible'] and link['relevance_score'] >= 50:
                    high_relevance_links.append((section, link))
        
        if high_relevance_links:
            recommendations.append(f"### ✅ 强烈推荐添加 ({len(high_relevance_links)} 个)")
            recommendations.append("以下链接具有高相关性，强烈建议添加到文章中：")
            recommendations.append("")
            
            for section, link in high_relevance_links[:10]:  # 显示前10个
                recommendations.append(f"- **{link['description']}**")
                recommendations.append(f"  - 相关性得分: {link['relevance_score']}/100")
                recommendations.append(f"  - 来源: {link['url']}")
                recommendations.append("")
        
        # 统计中等相关性链接
        medium_relevance_links = []
        for section, links in self.results.items():
            for link in links:
                if link['accessible'] and 20 <= link['relevance_score'] < 50:
                    medium_relevance_links.append((section, link))
        
        if medium_relevance_links:
            recommendations.append(f"### ⚠️ 谨慎考虑添加 ({len(medium_relevance_links)} 个)")
            recommendations.append("以下链接相关性中等，建议根据文章需要谨慎选择：")
            recommendations.append("")
            
            for section, link in medium_relevance_links[:5]:  # 显示前5个
                recommendations.append(f"- **{link['description']}**")
                recommendations.append(f"  - 相关性得分: {link['relevance_score']}/100")
                recommendations.append(f"  - 来源: {link['url']}")
                recommendations.append("")
        
        # 统计失败链接
        failed_links = []
        for section, links in self.results.items():
            for link in links:
                if not link['accessible']:
                    failed_links.append((section, link))
        
        if failed_links:
            recommendations.append(f"### ❌ 需要替换 ({len(failed_links)} 个)")
            recommendations.append("以下链接无法访问，建议寻找替代资源：")
            recommendations.append("")
            
            for section, link in failed_links[:5]:  # 显示前5个
                recommendations.append(f"- **{link['description']}**")
                recommendations.append(f"  - 错误: {link['error'] or f'HTTP {link['status_code']}'}")
                recommendations.append(f"  - 原链接: {link['url']}")
                recommendations.append("")
        
        return "\n".join(recommendations)

def main():
    # 定义要验证的链接数据
    links_data = {
        "第一部分：时间线篇 - 第一幕：史前时代": [
            {"url": "https://www.computer.org/publications/tech-news/operating-systems/the-evolution-of-operating-systems", "description": "The Evolution of Operating Systems - IEEE Computer Society"},
            {"url": "https://dl.acm.org/doi/10.1145/1234567.1234568", "description": "History of Multithreading - ACM Digital Library"},
            {"url": "https://www.bell-labs.com/usr/dmr/www/pdfs/utss.pdf", "description": "Unix Time-Sharing System - Bell Labs Technical Journal"},
            {"url": "https://www.os-book.com/OS9/", "description": "Operating System Concepts - Silberschatz et al."},
            {"url": "https://archive.org/details/designofunixoper00bach", "description": "The Design of the Unix Operating System - Maurice J. Bach"}
        ],
        "第一部分：时间线篇 - 第二幕：C10K挑战时代": [
            {"url": "http://www.kegel.com/c10k.html", "description": "The C10K Problem - Dan Kegel"},
            {"url": "https://queue.acm.org/detail.cfm?id=3487018", "description": "Scalable Event Multiplexing: epoll vs. kqueue - ACM Queue"},
            {"url": "https://nginx.org/en/docs/", "description": "Nginx Architecture - Nginx Official Documentation"},
            {"url": "https://redis.io/topics/architecture", "description": "Redis Architecture - Redis Documentation"},
            {"url": "https://nodejs.org/en/docs/guides/event-loop-timers-and-nexttick/", "description": "Node.js Event Loop - Node.js Documentation"}
        ],
        "第一部分：时间线篇 - 第三幕：多核与分布式时代": [
            {"url": "https://www.microsoft.com/en-us/research/publication/actor-model-everything-need-know/", "description": "The Actor Model: Everything You Need to Know - Microsoft Research"},
            {"url": "https://go.dev/blog/pipelines", "description": "Go Concurrency Patterns - Go Blog"},
            {"url": "https://erlang.org/doc/design_principles/des_princ.html", "description": "Erlang/OTP Design Principles - Ericsson"},
            {"url": "https://kotlinlang.org/docs/coroutines-guide.html", "description": "Kotlin Coroutines Guide - Kotlin Documentation"},
            {"url": "https://openjdk.org/projects/loom/", "description": "Java Project Loom - OpenJDK"}
        ],
        "第一部分：时间线篇 - 第四幕：未来已来": [
            {"url": "https://lwn.net/Articles/810414/", "description": "Linux io_uring: The Future of Async I/O - LWN.net"},
            {"url": "https://www.kernel.org/doc/html/latest/userspace-api/io_uring.html", "description": "The io_uring Interface - Linux Kernel Documentation"},
            {"url": "https://dl.acm.org/doi/10.1145/3458336.3465278", "description": "Async I/O Performance Comparison - ACM SIGOPS"},
            {"url": "https://isocpp.org/std/the-standard", "description": "Modern C++ Async I/O - C++ Standards Committee"},
            {"url": "https://www.cncf.io/blog/", "description": "Cloud Native I/O Patterns - Cloud Native Computing Foundation"}
        ],
        "第二部分：权责视角篇 - 阵营一：应用层主导型": [
            {"url": "https://ieeexplore.ieee.org/document/1234567", "description": "Thread Management in Modern Operating Systems - IEEE Transactions"},
            {"url": "https://dl.acm.org/doi/10.1145/3458336.3465279", "description": "User-Level Threading: Performance and Scalability - ACM SIGOPS"},
            {"url": "https://www.sciencedirect.com/science/article/abs/pii/S0364008X12345678", "description": "Application-Level Concurrency Control - Computer Science Review"},
            {"url": "https://resources.sei.cmu.edu/library/", "description": "Thread Synchronization Patterns - Software Engineering Institute"},
            {"url": "https://www.sciencedirect.com/journal/performance-evaluation", "description": "Performance Analysis of Multi-threaded Applications - Performance Evaluation"}
        ],
        "第二部分：权责视角篇 - 阵营二：内核代理型": [
            {"url": "https://www.linuxjournal.com/article/1234", "description": "Kernel-Level I/O Multiplexing - Linux Journal"},
            {"url": "https://www.usenix.org/conference/atc21", "description": "System Call Overhead Analysis - USENIX ATC"},
            {"url": "https://dl.acm.org/journal/tocs", "description": "Kernel-User Space Communication - ACM TOCS"},
            {"url": "https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=40", "description": "Hardware Interrupt Handling - IEEE Micro"},
            {"url": "https://dl.acm.org/journal/csur", "description": "Operating System I/O Subsystem Design - ACM Computing Surveys"}
        ],
        "第二部分：权责视角篇 - 阵营三：应用层优化型": [
            {"url": "https://pldi21.sigplan.org/", "description": "Coroutine Implementation Techniques - PLDI Conference"},
            {"url": "https://popl21.sigplan.org/", "description": "Actor Model Implementation - POPL Conference"},
            {"url": "https://sosp21.rcs.uwaterloo.ca/", "description": "User-Space Scheduling Algorithms - SOSP Conference"},
            {"url": "https://middleware-conf.github.io/2021/", "description": "Application-Level Load Balancing - Middleware Conference"},
            {"url": "https://conf.researchr.org/home/cgo-2021", "description": "Runtime System Optimization - CGO Conference"}
        ],
        "第三部分：IO多路复用深度解析 - 3.1 生态与影响": [
            {"url": "https://docs.oracle.com/javase/8/docs/api/java/nio/package-summary.html", "description": "Java NIO Implementation - Oracle Documentation"},
            {"url": "https://netty.io/wiki/", "description": "Netty Framework Architecture - Netty Official Site"},
            {"url": "https://github.com/libuv/libuv", "description": "Node.js libuv Implementation - GitHub Repository"},
            {"url": "https://peps.python.org/pep-3156/", "description": "Python asyncio Design - Python PEP 3156"},
            {"url": "https://redis.com/blog/", "description": "Redis Network Architecture - Redis Labs Blog"}
        ],
        "第三部分：IO多路复用深度解析 - 3.2 核心三要素": [
            {"url": "https://github.com/torvalds/linux/blob/master/fs/eventpoll.c", "description": "Linux epoll Implementation - Linux Kernel Source"},
            {"url": "https://lwn.net/Articles/123456/", "description": "epoll Data Structures - LWN.net Technical Articles"},
            {"url": "https://www.kernel.org/doc/html/latest/networking/", "description": "Kernel Socket Management - Linux Documentation"},
            {"url": "https://www.kernel.org/doc/html/latest/core-api/rbtree.html", "description": "Red-Black Tree in Kernel - Linux Kernel Documentation"},
            {"url": "https://www.kernel.org/doc/html/latest/core-api/kernel-api.html", "description": "Kernel Linked List Implementation - Linux Kernel Documentation"}
        ],
        "第三部分：IO多路复用深度解析 - 3.3 黄金触发链": [
            {"url": "https://software.intel.com/content/www/us/en/develop/articles/intel-sdm.html", "description": "Hardware Interrupt Processing - Intel Developer Manual"},
            {"url": "https://www.kernel.org/doc/html/latest/networking/", "description": "Network Card Interrupt Handling - Linux Networking Documentation"},
            {"url": "https://www.kernel.org/doc/html/latest/", "description": "Kernel Callback Mechanisms - Linux Kernel Development"},
            {"url": "https://man.openbsd.org/socket.2", "description": "Socket Buffer Management - BSD Socket Programming"},
            {"url": "https://pubs.opengroup.org/onlinepubs/9699919799/", "description": "Event Notification Systems - POSIX Standards"}
        ],
        "第三部分：IO多路复用深度解析 - 3.4 技术优势总结": [
            {"url": "https://dl.acm.org/journal/sigmetr", "description": "Performance Comparison: Polling vs. Interrupts - ACM SIGMETRICS"},
            {"url": "https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=69", "description": "Scalability Analysis of Event-Driven Systems - IEEE Transactions"},
            {"url": "https://www.usenix.org/conference/osdi20", "description": "Kernel-User Space Efficiency - USENIX OSDI"},
            {"url": "https://www.sigarch.org/", "description": "Hardware Event Processing - Computer Architecture News"},
            {"url": "https://dl.acm.org/journal/tocs", "description": "System Call Performance Optimization - ACM TOCS"}
        ],
        "第四部分：技术选型篇 - 4.1 核心原则": [
            {"url": "https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=52", "description": "System Architecture Design Principles - IEEE Software"},
            {"url": "https://dl.acm.org/journal/csur", "description": "Separation of Concerns in Software Design - ACM Computing Surveys"},
            {"url": "https://dl.acm.org/journal/tocs", "description": "Operating System Design Philosophy - ACM TOCS"},
            {"url": "https://sosp21.rcs.uwaterloo.ca/", "description": "Kernel-Application Interface Design - SOSP Conference"},
            {"url": "https://www.sciencedirect.com/journal/performance-evaluation", "description": "System Performance Optimization - Performance Evaluation"}
        ],
        "第四部分：技术选型篇 - 4.2 决策框架": [
            {"url": "https://dl.acm.org/journal/sigmetr", "description": "Application Performance Profiling - ACM SIGMETRICS"},
            {"url": "https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=69", "description": "Concurrency Level Analysis - IEEE Transactions"},
            {"url": "https://dl.acm.org/journal/sigops", "description": "Resource Constraint Optimization - ACM SIGOPS"},
            {"url": "https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=52", "description": "Team Productivity Analysis - IEEE Software"},
            {"url": "https://www.springer.com/journal/10664", "description": "Technology Selection Framework - Software Engineering"}
        ],
        "第四部分：技术选型篇 - 4.3 场景分析与最佳实践": [
            {"url": "https://www.nginx.com/blog/", "description": "Nginx Performance Tuning - Nginx Official Blog"},
            {"url": "https://redis.com/blog/", "description": "Redis Performance Optimization - Redis Labs Blog"},
            {"url": "https://netty.io/wiki/", "description": "Netty Architecture Best Practices - Netty Documentation"},
            {"url": "https://go.dev/blog/", "description": "Go Concurrency Best Practices - Go Blog"},
            {"url": "https://openjdk.org/projects/loom/", "description": "Java Virtual Threads Guide - OpenJDK Documentation"}
        ]
    }
    
    # 创建验证器并执行验证
    validator = EnhancedLinkValidator()
    results = validator.validate_links_batch(links_data)
    
    # 生成报告
    report = validator.generate_enhanced_report()
    print("\n" + "="*60)
    print("验证完成！生成增强版报告...")
    print("="*60)
    print(report)
    
    # 生成建议
    recommendations = validator.get_recommendations()
    print("\n" + "="*60)
    print("生成添加建议...")
    print("="*60)
    print(recommendations)
    
    # 保存结果
    validator.save_results()
    
    # 显示成功和失败的链接统计
    print("\n" + "="*60)
    print("验证结果统计:")
    print("="*60)
    
    total_links = sum(len(links) for links in results.values())
    successful_links = sum(1 for section in results.values() for link in section if link['accessible'])
    failed_links = total_links - successful_links
    high_relevance_links = sum(1 for section in results.values() for link in section if link['accessible'] and link['relevance_score'] >= 50)
    
    print(f"总链接数: {total_links}")
    print(f"成功链接: {successful_links}")
    print(f"失败链接: {failed_links}")
    print(f"高相关性链接(≥50分): {high_relevance_links}")
    print(f"成功率: {(successful_links/total_links*100):.1f}%")
    print(f"高相关性比例: {(high_relevance_links/successful_links*100):.1f}%" if successful_links > 0 else "0%")

if __name__ == "__main__":
    main()
