#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Redis分布式锁文档链接验证脚本
验证所有引用的技术论据链接的有效性
"""

import asyncio
import aiohttp
import time
from urllib.parse import urlparse
from typing import Dict, List, Tuple
import json
import re

class LinkValidator:
    def __init__(self, timeout: int = 10, max_concurrent: int = 5):
        self.timeout = timeout
        self.max_concurrent = max_concurrent
        self.session = None
        self.results = {}
        
    async def __aenter__(self):
        connector = aiohttp.TCPConnector(limit=self.max_concurrent)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=self.timeout)
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def validate_link(self, url: str, description: str) -> Dict:
        """验证单个链接"""
        start_time = time.time()
        result = {
            'url': url,
            'description': description,
            'status': 'unknown',
            'status_code': None,
            'response_time': None,
            'error': None,
            'content_length': 0,
            'is_redis_related': False,
            'relevance_score': 0
        }
        
        try:
            async with self.session.get(url, allow_redirects=True) as response:
                result['status_code'] = response.status
                result['response_time'] = round(time.time() - start_time, 2)
                
                if response.status == 200:
                    result['status'] = 'success'
                    content = await response.text()
                    result['content_length'] = len(content)
                    
                    # 检查内容相关性
                    result['is_redis_related'] = self._check_redis_relevance(content)
                    result['relevance_score'] = self._calculate_relevance_score(content, description)
                    
                elif response.status in [301, 302, 307, 308]:
                    result['status'] = 'redirect'
                    result['error'] = f"重定向到: {response.headers.get('Location', 'Unknown')}"
                    
                else:
                    result['status'] = 'error'
                    result['error'] = f"HTTP {response.status}"
                    
        except asyncio.TimeoutError:
            result['status'] = 'timeout'
            result['error'] = "请求超时"
        except aiohttp.ClientError as e:
            result['status'] = 'connection_error'
            result['error'] = str(e)
        except Exception as e:
            result['status'] = 'unknown_error'
            result['error'] = str(e)
            
        return result
    
    def _check_redis_relevance(self, content: str) -> bool:
        """检查内容是否与Redis相关"""
        redis_keywords = ['redis', 'distributed lock', 'setnx', 'expire', 'redisson']
        content_lower = content.lower()
        return any(keyword in content_lower for keyword in redis_keywords)
    
    def _calculate_relevance_score(self, content: str, description: str) -> int:
        """计算内容相关性评分 (0-10)"""
        score = 0
        content_lower = content.lower()
        description_lower = description.lower()
        
        # 基于描述关键词匹配
        description_words = set(re.findall(r'\b\w+\b', description_lower))
        content_words = set(re.findall(r'\b\w+\b', content_lower))
        
        # 关键词匹配度
        common_words = description_words.intersection(content_words)
        if len(description_words) > 0:
            score += min(len(common_words) / len(description_words) * 5, 5)
        
        # Redis相关度
        if self._check_redis_relevance(content):
            score += 3
            
        # 内容长度合理性
        if 1000 <= len(content) <= 100000:  # 合理的内容长度
            score += 2
            
        return min(int(score), 10)
    
    async def validate_all_links(self, links: List[Tuple[str, str]]) -> Dict:
        """验证所有链接"""
        print(f"🔍 开始验证 {len(links)} 个链接...")
        
        # 创建验证任务
        tasks = []
        for url, description in links:
            task = self.validate_link(url, description)
            tasks.append(task)
        
        # 并发执行验证
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理结果
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                self.results[links[i][0]] = {
                    'url': links[i][0],
                    'description': links[i][1],
                    'status': 'exception',
                    'error': str(result)
                }
            else:
                self.results[links[i][0]] = result
                
        return self.results
    
    def generate_report(self) -> str:
        """生成验证报告"""
        total = len(self.results)
        success = sum(1 for r in self.results.values() if r['status'] == 'success')
        redirect = sum(1 for r in self.results.values() if r['status'] == 'redirect')
        error = sum(1 for r in self.results.values() if r['status'] not in ['success', 'redirect'])
        
        report = f"""
# 🔒 Redis分布式锁文档链接验证报告

## 📊 验证统计
- **总链接数**: {total}
- **成功访问**: {success} ({success/total*100:.1f}%)
- **重定向**: {redirect} ({redirect/total*100:.1f}%)
- **访问失败**: {error} ({error/total*100:.1f}%)

## ✅ 成功访问的链接
"""
        
        for url, result in self.results.items():
            if result['status'] == 'success':
                report += f"""
### {result['description']}
- **URL**: {url}
- **响应时间**: {result['response_time']}s
- **内容长度**: {result['content_length']} 字符
- **Redis相关性**: {'是' if result['is_redis_related'] else '否'}
- **相关性评分**: {result['relevance_score']}/10
"""
        
        if redirect > 0:
            report += f"\n## 🔄 重定向链接\n"
            for url, result in self.results.items():
                if result['status'] == 'redirect':
                    report += f"- **{result['description']}**: {url} → {result['error']}\n"
        
        if error > 0:
            report += f"\n## ❌ 访问失败的链接\n"
            for url, result in self.results.items():
                if result['status'] not in ['success', 'redirect']:
                    report += f"- **{result['description']}**: {url} - {result['error']}\n"
        
        report += f"""

## 🎯 添加建议

### 高相关性链接 (评分 8-10)
建议优先添加到文档中，这些链接与内容高度相关且权威性较高。

### 中等相关性链接 (评分 5-7)
可以考虑添加，但建议验证内容质量。

### 低相关性链接 (评分 0-4)
不建议添加，内容相关性不足或质量较低。

## ⚠️ 注意事项
1. 所有链接验证基于当前网络环境，结果可能因时间和地点而异
2. 建议定期重新验证链接有效性
3. 优先选择官方文档和权威技术博客
4. 对于重定向链接，建议使用最终目标URL

---
*验证时间: {time.strftime('%Y-%m-%d %H:%M:%S')}*
"""
        return report

async def main():
    """主函数"""
    # 定义要验证的链接
    links = [
        ("https://redis.io/commands/set/", "Redis官方文档 - SET命令"),
        ("https://redis.io/commands/setnx/", "Redis官方文档 - NX参数说明"),
        ("https://redis.io/topics/distlock", "Redis官方文档 - 分布式锁最佳实践"),
        ("https://redis.io/commands/expire/", "Redis官方文档 - 过期时间机制"),
        ("https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html", "Martin Kleppmann的分布式锁分析"),
        ("https://redis.io/topics/distlock#safety-requirements", "Redis官方分布式锁安全指南"),
        ("https://raw.githubusercontent.com/redis/redis/2.8/00-RELEASENOTES", "Redis 2.8版本更新日志"),
        ("https://stackoverflow.com/questions/2955402/redis-setnx-and-expire-atomicity", "Stack Overflow讨论 - 原子性实现"),
        ("https://github.com/redisson/redisson/wiki/8.-distributed-locks-and-synchronizers", "Redisson官方文档 - Watchdog机制"),
        ("https://github.com/redisson/redisson/wiki/8.-distributed-locks-and-synchronizers#81-redis分布式锁", "Redisson官方文档 - 自动续约"),
        ("https://redis.io/topics/distlock#correctness-arguments", "Redis官方文档 - 锁续约最佳实践")
    ]
    
    print("🚀 开始验证Redis分布式锁文档链接...")
    
    async with LinkValidator(timeout=15, max_concurrent=3) as validator:
        results = await validator.validate_all_links(links)
        
        # 生成报告
        report = validator.generate_report()
        
        # 保存报告到文件
        with open('link_validation_report.md', 'w', encoding='utf-8') as f:
            f.write(report)
        
        # 保存详细结果到JSON文件
        with open('link_validation_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print("✅ 验证完成！")
        print("📄 详细报告已保存到: link_validation_report.md")
        print("📊 原始数据已保存到: link_validation_results.json")
        
        # 打印简要结果
        print("\n" + "="*50)
        print(report.split("## 📊 验证统计")[1].split("## ✅ 成功访问的链接")[0])

if __name__ == "__main__":
    asyncio.run(main())
