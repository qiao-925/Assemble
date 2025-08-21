#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用链接有效性验证器
支持各种项目的链接验证和内容相关性分析
"""

import requests
import re
import json
import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Any
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UniversalLinkValidator:
    """通用链接验证器"""
    
    def __init__(self, **config):
        """
        初始化验证器
        
        Args:
            project_name (str): 项目名称
            keywords (List[str]): 内容相关性分析的关键词
            domains (List[str]): 信任的域名列表
            relevance_threshold (float): 相关性阈值 (0-1)
            max_links_per_section (int): 每个章节最大链接数
            timeout (int): 请求超时时间(秒)
            delay (float): 请求间隔时间(秒)
            user_agent (str): 自定义User-Agent
        """
        self.config = {
            'project_name': config.get('project_name', '通用项目'),
            'keywords': config.get('keywords', []),
            'domains': config.get('domains', []),
            'relevance_threshold': config.get('relevance_threshold', 0.3),
            'max_links_per_section': config.get('max_links_per_section', 5),
            'timeout': config.get('timeout', 15),
            'delay': config.get('delay', 1.0),
            'user_agent': config.get('user_agent', 
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        }
        
        # 初始化HTTP会话
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.config['user_agent']})
        
        # 存储验证结果
        self.results = {}
        self.statistics = {
            'total_links': 0,
            'valid_links': 0,
            'invalid_links': 0,
            'relevant_links': 0,
            'start_time': None,
            'end_time': None
        }
        
        logger.info(f"初始化 {self.config['project_name']} 链接验证器")
        logger.info(f"关键词: {self.config['keywords']}")
        logger.info(f"信任域名: {self.config['domains']}")
    
    def check_link(self, url: str, description: str = "") -> Dict[str, Any]:
        """
        检查单个链接的有效性和内容相关性
        
        Args:
            url (str): 要检查的URL
            description (str): 链接描述
            
        Returns:
            Dict: 包含验证结果的字典
        """
        logger.info(f"正在检查链接: {url}")
        if description:
            logger.info(f"描述: {description}")
        
        result = {
            'url': url,
            'description': description,
            'status': 'unknown',
            'status_code': None,
            'error': None,
            'title': None,
            'content_length': 0,
            'relevance_score': 0.0,
            'is_relevant': False,
            'domain': urlparse(url).netloc,
            'check_time': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        try:
            # 发送HTTP请求
            response = self.session.get(
                url, 
                timeout=self.config['timeout'], 
                allow_redirects=True
            )
            
            if response.status_code == 200:
                # 解析HTML内容
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 提取文本内容
                text_content = soup.get_text()
                
                # 分析内容相关性
                relevance_score = self.analyze_relevance(text_content, description)
                
                # 更新结果
                result.update({
                    'status': 'valid',
                    'status_code': response.status_code,
                    'content_length': len(text_content),
                    'relevance_score': relevance_score,
                    'title': soup.title.string.strip() if soup.title else 'No title',
                    'is_relevant': relevance_score >= self.config['relevance_threshold']
                })
                
                logger.info(f"✓ 链接有效 (状态码: {response.status_code})")
                logger.info(f"  相关性评分: {relevance_score:.2f}")
                logger.info(f"  页面标题: {result['title']}")
                
            else:
                result.update({
                    'status': 'error',
                    'status_code': response.status_code,
                    'error': f'HTTP {response.status_code}'
                })
                logger.warning(f"✗ 链接无效 (状态码: {response.status_code})")
                
        except requests.exceptions.RequestException as e:
            result.update({
                'status': 'error',
                'error': str(e)
            })
            logger.error(f"✗ 请求失败: {e}")
        except Exception as e:
            result.update({
                'status': 'error',
                'error': f'Unexpected error: {str(e)}'
            })
            logger.error(f"✗ 未知错误: {e}")
        
        return result
    
    def analyze_relevance(self, text: str, description: str = "") -> float:
        """
        分析内容相关性
        
        Args:
            text (str): 页面文本内容
            description (str): 链接描述
            
        Returns:
            float: 相关性评分 (0-1)
        """
        if not self.config['keywords']:
            return 0.5  # 如果没有关键词，返回中等相关性
        
        text_lower = text.lower()
        description_lower = description.lower()
        
        # 计算关键词匹配度
        keyword_score = 0
        for keyword in self.config['keywords']:
            if keyword.lower() in text_lower:
                keyword_score += 1
        
        # 计算描述匹配度
        desc_words = [word for word in description_lower.split() if len(word) > 3]
        desc_score = 0
        for word in desc_words:
            if word in text_lower:
                desc_score += 1
        
        # 计算总相关性评分
        total_keywords = len(self.config['keywords'])
        total_desc_words = len(desc_words)
        
        if total_keywords + total_desc_words == 0:
            return 0.0
        
        relevance = (keyword_score + desc_score * 2) / (total_keywords + total_desc_words * 2)
        
        return min(relevance, 1.0)
    
    def extract_links_from_markdown(self, file_path: str) -> List[Dict[str, str]]:
        """
        从Markdown文件中提取链接
        
        Args:
            file_path (str): Markdown文件路径
            
        Returns:
            List[Dict]: 包含链接信息的列表
        """
        links = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 使用正则表达式匹配Markdown链接
            link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
            matches = re.findall(link_pattern, content)
            
            for description, url in matches:
                # 过滤掉非HTTP链接
                if url.startswith(('http://', 'https://')):
                    links.append({
                        'description': description.strip(),
                        'url': url.strip()
                    })
                    
        except FileNotFoundError:
            logger.error(f"文件不存在: {file_path}")
        except Exception as e:
            logger.error(f"读取文件失败: {e}")
            
        logger.info(f"从 {file_path} 中提取到 {len(links)} 个链接")
        return links
    
    def validate_document(self, file_path: str) -> Dict[str, Any]:
        """
        验证文档中的所有链接
        
        Args:
            file_path (str): 要验证的文档路径
            
        Returns:
            Dict: 验证结果统计
        """
        logger.info(f"开始验证文档: {file_path}")
        logger.info("=" * 60)
        
        # 记录开始时间
        self.statistics['start_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
        
        # 提取链接
        links = self.extract_links_from_markdown(file_path)
        self.statistics['total_links'] = len(links)
        
        if not links:
            logger.warning("未找到任何链接")
            return self.statistics
        
        # 验证每个链接
        for i, link in enumerate(links, 1):
            logger.info(f"[{i}/{len(links)}]")
            result = self.check_link(link['url'], link['description'])
            
            # 存储结果
            self.results[link['url']] = result
            
            # 更新统计
            if result['status'] == 'valid':
                self.statistics['valid_links'] += 1
                if result['is_relevant']:
                    self.statistics['relevant_links'] += 1
            else:
                self.statistics['invalid_links'] += 1
            
            # 延迟避免请求过于频繁
            if i < len(links):
                time.sleep(self.config['delay'])
        
        # 记录结束时间
        self.statistics['end_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
        
        # 生成报告
        self.generate_report()
        
        return self.statistics
    
    def generate_report(self) -> None:
        """生成验证报告"""
        logger.info("=" * 60)
        logger.info(f"{self.config['project_name']} - 链接验证报告")
        logger.info("=" * 60)
        
        # 分类链接
        valid_links = []
        invalid_links = []
        relevant_links = []
        
        for url, result in self.results.items():
            if result['status'] == 'valid':
                valid_links.append(url)
                if result['is_relevant']:
                    relevant_links.append(url)
            else:
                invalid_links.append(url)
        
        # 输出统计信息
        logger.info(f"总链接数: {self.statistics['total_links']}")
        logger.info(f"有效链接: {self.statistics['valid_links']}")
        logger.info(f"无效链接: {self.statistics['invalid_links']}")
        logger.info(f"相关内容: {self.statistics['relevant_links']}")
        
        # 输出无效链接
        if invalid_links:
            logger.info(f"\n无效链接列表:")
            for url in invalid_links:
                error = self.results[url].get('error', 'Unknown error')
                logger.info(f"  - {url}")
                logger.info(f"    错误: {error}")
        
        # 输出高相关性链接
        if relevant_links:
            logger.info(f"\n高相关性链接:")
            for url in relevant_links:
                score = self.results[url].get('relevance_score', 0)
                logger.info(f"  - {url} (相关性: {score:.2f})")
        
        # 保存结果到JSON文件
        self.save_results()
        
        # 生成Markdown报告
        self.generate_markdown_report()
    
    def save_results(self) -> None:
        """保存验证结果到JSON文件"""
        output_file = f"{self.config['project_name']}_link_validation_results.json"
        
        # 准备输出数据
        output_data = {
            'project_info': {
                'name': self.config['project_name'],
                'validation_time': {
                    'start': self.statistics['start_time'],
                    'end': self.statistics['end_time']
                },
                'configuration': self.config
            },
            'statistics': self.statistics,
            'results': self.results
        }
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            logger.info(f"详细结果已保存到: {output_file}")
        except Exception as e:
            logger.error(f"保存结果失败: {e}")
    
    def generate_markdown_report(self) -> None:
        """生成Markdown格式的报告"""
        output_file = f"{self.config['project_name']}_validation_summary.md"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# {self.config['project_name']} - 链接验证总结报告\n\n")
                
                # 基本信息
                f.write("## 验证信息\n\n")
                f.write(f"- **项目名称**: {self.config['project_name']}\n")
                f.write(f"- **验证开始时间**: {self.statistics['start_time']}\n")
                f.write(f"- **验证结束时间**: {self.statistics['end_time']}\n")
                f.write(f"- **总链接数**: {self.statistics['total_links']}\n\n")
                
                # 统计信息
                f.write("## 验证统计\n\n")
                f.write(f"- **有效链接**: {self.statistics['valid_links']}\n")
                f.write(f"- **无效链接**: {self.statistics['invalid_links']}\n")
                f.write(f"- **相关内容**: {self.statistics['relevant_links']}\n")
                f.write(f"- **成功率**: {(self.statistics['valid_links']/self.statistics['total_links']*100):.1f}%\n\n")
                
                # 有效链接列表
                f.write("## 有效链接列表\n\n")
                valid_links = [url for url, result in self.results.items() if result['status'] == 'valid']
                for url in valid_links:
                    result = self.results[url]
                    title = result.get('title', 'No title')
                    relevance = result.get('relevance_score', 0)
                    f.write(f"- [{title}]({url}) (相关性: {relevance:.2f})\n")
                
                # 无效链接列表
                if any(result['status'] == 'error' for result in self.results.values()):
                    f.write("\n## 无效链接列表\n\n")
                    invalid_links = [url for url, result in self.results.items() if result['status'] == 'error']
                    for url in invalid_links:
                        result = self.results[url]
                        error = result.get('error', 'Unknown error')
                        f.write(f"- {url} - {error}\n")
            
            logger.info(f"Markdown报告已保存到: {output_file}")
        except Exception as e:
            logger.error(f"生成Markdown报告失败: {e}")
    
    def get_recommendations(self) -> Dict[str, Any]:
        """
        获取链接改进建议
        
        Returns:
            Dict: 改进建议
        """
        recommendations = {
            'broken_links': [],
            'low_relevance_links': [],
            'domain_distribution': {},
            'improvement_suggestions': []
        }
        
        # 分析失效链接
        for url, result in self.results.items():
            if result['status'] == 'error':
                recommendations['broken_links'].append({
                    'url': url,
                    'error': result.get('error', 'Unknown error')
                })
        
        # 分析低相关性链接
        for url, result in self.results.items():
            if (result['status'] == 'valid' and 
                result.get('relevance_score', 0) < self.config['relevance_threshold']):
                recommendations['low_relevance_links'].append({
                    'url': url,
                    'relevance': result.get('relevance_score', 0)
                })
        
        # 分析域名分布
        for url, result in self.results.items():
            domain = result.get('domain', 'unknown')
            if domain not in recommendations['domain_distribution']:
                recommendations['domain_distribution'][domain] = 0
            recommendations['domain_distribution'][domain] += 1
        
        # 生成改进建议
        if recommendations['broken_links']:
            recommendations['improvement_suggestions'].append(
                f"需要修复 {len(recommendations['broken_links'])} 个失效链接"
            )
        
        if recommendations['low_relevance_links']:
            recommendations['improvement_suggestions'].append(
                f"有 {len(recommendations['low_relevance_links'])} 个链接内容相关性较低，建议更新"
            )
        
        return recommendations
