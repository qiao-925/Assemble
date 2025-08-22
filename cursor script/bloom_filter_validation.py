#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
布隆过滤器文章论据验证脚本
用于验证文章中提到的链接有效性和论据相关性
"""

import asyncio
import aiohttp
import time
import json
from urllib.parse import urlparse
from typing import Dict, List, Tuple
import re

class BloomFilterValidator:
    def __init__(self):
        self.session = None
        self.results = []
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def validate_url(self, url: str, description: str) -> Dict:
        """验证单个URL的有效性"""
        start_time = time.time()
        result = {
            'url': url,
            'description': description,
            'status_code': None,
            'response_time': None,
            'error': None,
            'content_length': 0,
            'is_valid': False,
            'relevance_score': 0
        }
        
        try:
            async with self.session.get(url, allow_redirects=True) as response:
                result['status_code'] = response.status
                result['response_time'] = time.time() - start_time
                
                if response.status == 200:
                    content = await response.text()
                    result['content_length'] = len(content)
                    result['is_valid'] = True
                    
                    # 分析内容相关性
                    result['relevance_score'] = self.analyze_relevance(content, description)
                    
                elif response.status in [301, 302, 307, 308]:
                    result['is_valid'] = True
                    result['error'] = f"重定向到: {response.headers.get('Location', 'Unknown')}"
                    
        except Exception as e:
            result['error'] = str(e)
            result['response_time'] = time.time() - start_time
            
        return result
    
    def analyze_relevance(self, content: str, description: str) -> int:
        """分析内容与描述的相关性，返回0-100的分数"""
        # 提取关键词
        keywords = self.extract_keywords(description)
        
        # 计算相关性分数
        score = 0
        content_lower = content.lower()
        
        for keyword in keywords:
            if keyword.lower() in content_lower:
                score += 20
                
        # 检查特定技术术语
        tech_terms = ['bloom filter', 'redis', 'hash', 'bit array', 'false positive']
        for term in tech_terms:
            if term in content_lower:
                score += 10
                
        return min(score, 100)
    
    def extract_keywords(self, description: str) -> List[str]:
        """从描述中提取关键词"""
        # 移除特殊字符，提取有意义的词汇
        words = re.findall(r'\b\w+\b', description.lower())
        # 过滤掉停用词
        stop_words = {'的', '是', '在', '有', '和', '与', '或', '等', '等', 'a', 'an', 'the', 'and', 'or', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        return keywords[:5]  # 返回前5个关键词
    
    async def validate_all_urls(self, urls: List[Tuple[str, str]]) -> List[Dict]:
        """并发验证所有URL"""
        tasks = [self.validate_url(url, desc) for url, desc in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理异常结果
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                results[i] = {
                    'url': urls[i][0],
                    'description': urls[i][1],
                    'status_code': None,
                    'response_time': None,
                    'error': str(result),
                    'content_length': 0,
                    'is_valid': False,
                    'relevance_score': 0
                }
        
        return results
    
    def generate_report(self, results: List[Dict]) -> str:
        """生成验证报告"""
        total = len(results)
        valid = sum(1 for r in results if r['is_valid'])
        failed = total - valid
        
        report = f"""# 🔍 布隆过滤器文章论据验证报告

## 📊 验证统计
- **总链接数**: {total}
- **有效链接**: {valid}
- **无效链接**: {failed}
- **成功率**: {(valid/total*100):.1f}%

## ✅ 有效链接详情
"""
        
        for result in results:
            if result['is_valid']:
                report += f"""
### {result['description']}
- **URL**: {result['url']}
- **状态码**: {result['status_code']}
- **响应时间**: {result['response_time']:.2f}s
- **内容长度**: {result['content_length']:,} 字符
- **相关性评分**: {result['relevance_score']}/100
"""
        
        if failed > 0:
            report += f"""
## ❌ 无效链接详情
"""
            for result in results:
                if not result['is_valid']:
                    report += f"""
### {result['description']}
- **URL**: {result['url']}
- **错误**: {result['error']}
- **响应时间**: {result['response_time']:.2f}s
"""
        
        report += f"""
## 🎯 相关性分析
- **高相关性 (80-100分)**: {sum(1 for r in results if r['relevance_score'] >= 80)}
- **中相关性 (50-79分)**: {sum(1 for r in results if r['relevance_score'] >= 50 and r['relevance_score'] < 80)}
- **低相关性 (0-49分)**: {sum(1 for r in results if r['relevance_score'] < 50)}

## 💡 建议
"""
        
        if valid/total >= 0.8:
            report += "- ✅ 大部分链接有效，文章论据质量较高"
        else:
            report += "- ⚠️ 存在较多无效链接，建议更新或替换"
            
        if any(r['relevance_score'] >= 80 for r in results):
            report += "\n- ✅ 存在高相关性论据，支撑文章论点"
        else:
            report += "\n- ⚠️ 论据相关性较低，建议寻找更相关的资料"
            
        return report

async def main():
    """主函数"""
    # 布隆过滤器文章中的链接列表
    urls_to_validate = [
        ("https://redis.io/docs/stack/bloom/", "Redis Bloom官方文档"),
        ("https://github.com/RedisBloom/RedisBloom", "Redis Bloom插件仓库"),
        ("https://cloud.tencent.com/developer/article/2459806", "腾讯云Redis Bloom分析"),
        ("https://krisives.github.io/bloom-calculator/", "Bloom Calculator在线工具"),
        ("https://redis.io/docs/stack/bloom/", "Redis Bloom官方文档(重复)"),
    ]
    
    print("🔍 开始验证布隆过滤器文章中的链接...")
    
    async with BloomFilterValidator() as validator:
        results = await validator.validate_all_urls(urls_to_validate)
        
        # 生成报告
        report = validator.generate_report(results)
        
        # 保存报告
        with open('bloom_filter_validation_report.md', 'w', encoding='utf-8') as f:
            f.write(report)
        
        # 保存详细结果
        with open('bloom_filter_validation_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print("✅ 验证完成！")
        print(f"📊 总链接: {len(results)}, 有效: {sum(1 for r in results if r['is_valid'])}")
        print("📄 详细报告已保存到 bloom_filter_validation_report.md")
        print("📋 原始数据已保存到 bloom_filter_validation_results.json")
        
        # 显示简要结果
        print("\n🔍 简要结果:")
        for result in results:
            status = "✅" if result['is_valid'] else "❌"
            print(f"{status} {result['description']}: {result['url']}")

if __name__ == "__main__":
    asyncio.run(main())
