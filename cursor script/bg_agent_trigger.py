#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Background Agent 触发工具
专门为Cursor Background Agent设计的简单触发接口
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict

class BackgroundAgentTrigger:
    """Background Agent 触发器"""
    
    def __init__(self, work_dir: str = None):
        """
        初始化触发器
        
        Args:
            work_dir: 工作目录路径，默认为当前脚本所在目录
        """
        if work_dir is None:
            work_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.work_dir = Path(work_dir)
        self.trigger_dir = self.work_dir / "triggers"
        self.completed_dir = self.work_dir / "completed"
        
        # 确保目录存在
        self.trigger_dir.mkdir(exist_ok=True)
        self.completed_dir.mkdir(exist_ok=True)
    
    def trigger_daily_digest(self) -> str:
        """
        触发每日技术摘要生成
        
        Returns:
            str: 触发文件路径
        """
        trigger_data = {
            'command': 'daily_digest',
            'params': {},
            'timestamp': datetime.now().isoformat(),
            'source': 'background_agent'
        }
        
        return self._create_trigger_file('daily_digest', trigger_data)
    
    def trigger_project_analysis(self, repo: str) -> str:
        """
        触发GitHub项目深度分析
        
        Args:
            repo: GitHub仓库，格式为 'owner/repo' 或完整URL
            
        Returns:
            str: 触发文件路径
        """
        # 清理repo格式
        if repo.startswith('https://github.com/'):
            repo = repo.replace('https://github.com/', '')
        
        trigger_data = {
            'command': 'analyze_project',
            'params': {'repo': repo},
            'timestamp': datetime.now().isoformat(),
            'source': 'background_agent'
        }
        
        return self._create_trigger_file('analyze_project', trigger_data)
    
    def trigger_trend_analysis(self, topic: Optional[str] = None) -> str:
        """
        触发技术趋势分析
        
        Args:
            topic: 分析主题，如 'ai', 'kubernetes' 等，None表示全领域分析
            
        Returns:
            str: 触发文件路径
        """
        trigger_data = {
            'command': 'trend_analysis',
            'params': {'topic': topic} if topic else {},
            'timestamp': datetime.now().isoformat(),
            'source': 'background_agent'
        }
        
        return self._create_trigger_file('trend_analysis', trigger_data)
    
    def trigger_project_comparison(self, projects: List[str]) -> str:
        """
        触发项目对比分析
        
        Args:
            projects: 项目列表，格式为 ['owner/repo1', 'owner/repo2', ...]
            
        Returns:
            str: 触发文件路径
        """
        if len(projects) < 2:
            raise ValueError("至少需要2个项目进行对比")
        
        # 清理项目格式
        clean_projects = []
        for project in projects:
            if project.startswith('https://github.com/'):
                project = project.replace('https://github.com/', '')
            clean_projects.append(project)
        
        trigger_data = {
            'command': 'compare_projects',
            'params': {'projects': clean_projects},
            'timestamp': datetime.now().isoformat(),
            'source': 'background_agent'
        }
        
        return self._create_trigger_file('compare_projects', trigger_data)
    
    def _create_trigger_file(self, task_name: str, trigger_data: Dict) -> str:
        """创建触发文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        trigger_file = self.trigger_dir / f"{task_name}_{timestamp}.trigger"
        
        with open(trigger_file, 'w', encoding='utf-8') as f:
            json.dump(trigger_data, f, ensure_ascii=False, indent=2)
        
        print(f"🔔 已创建触发任务: {task_name}")
        print(f"📁 触发文件: {trigger_file}")
        
        return str(trigger_file)
    
    def wait_for_completion(self, task_name: str, timeout: int = 300) -> Optional[str]:
        """
        等待任务完成
        
        Args:
            task_name: 任务名称
            timeout: 超时时间（秒），默认5分钟
            
        Returns:
            str: 输出文件路径，如果超时则返回None
        """
        print(f"⏳ 等待任务完成: {task_name} (超时: {timeout}秒)")
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # 检查完成标记文件
            for completed_file in self.completed_dir.glob(f"{task_name}_*.completed"):
                try:
                    with open(completed_file, 'r', encoding='utf-8') as f:
                        completion_data = json.load(f)
                    
                    if completion_data.get('status') == 'success':
                        output_file = completion_data.get('output_file')
                        print(f"✅ 任务完成: {output_file}")
                        return output_file
                    
                except Exception as e:
                    print(f"⚠️ 读取完成标记失败: {e}")
            
            time.sleep(2)  # 每2秒检查一次
        
        print(f"⏰ 任务超时: {task_name}")
        return None
    
    def get_daemon_status(self) -> Dict:
        """获取守护进程状态"""
        status_file = self.work_dir / "daemon_status.json"
        
        if status_file.exists():
            with open(status_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {'status': 'unknown', 'message': '状态文件不存在'}
    
    def get_recent_outputs(self, days: int = 7) -> List[Dict]:
        """获取最近的输出文件"""
        outputs = []
        output_dir = self.work_dir / "output"
        
        if output_dir.exists():
            cutoff_time = time.time() - (days * 24 * 3600)
            
            for output_file in output_dir.glob("*.md"):
                if output_file.stat().st_mtime > cutoff_time:
                    outputs.append({
                        'file': str(output_file),
                        'created': datetime.fromtimestamp(output_file.stat().st_mtime).isoformat(),
                        'size_kb': round(output_file.stat().st_size / 1024, 1)
                    })
        
        return sorted(outputs, key=lambda x: x['created'], reverse=True)

# 便捷函数，供Background Agent直接调用
def bg_daily_digest() -> Optional[str]:
    """Background Agent：触发每日摘要"""
    trigger = BackgroundAgentTrigger()
    trigger.trigger_daily_digest()
    return trigger.wait_for_completion('daily_digest')

def bg_analyze_project(repo: str) -> Optional[str]:
    """Background Agent：分析GitHub项目"""
    trigger = BackgroundAgentTrigger()
    trigger.trigger_project_analysis(repo)
    return trigger.wait_for_completion('analyze_project')

def bg_trend_analysis(topic: str = None) -> Optional[str]:
    """Background Agent：技术趋势分析"""
    trigger = BackgroundAgentTrigger()
    trigger.trigger_trend_analysis(topic)
    return trigger.wait_for_completion('trend_analysis')

def bg_compare_projects(projects: List[str]) -> Optional[str]:
    """Background Agent：项目对比分析"""
    trigger = BackgroundAgentTrigger()
    trigger.trigger_project_comparison(projects)
    return trigger.wait_for_completion('compare_projects')

def bg_get_status() -> Dict:
    """Background Agent：获取系统状态"""
    trigger = BackgroundAgentTrigger()
    return trigger.get_daemon_status()

def bg_get_recent_reports(days: int = 7) -> List[Dict]:
    """Background Agent：获取最近的报告"""
    trigger = BackgroundAgentTrigger()
    return trigger.get_recent_outputs(days)

if __name__ == "__main__":
    # 命令行使用示例
    import argparse
    
    parser = argparse.ArgumentParser(description='Background Agent 触发工具')
    parser.add_argument('action', choices=['daily', 'analyze', 'trend', 'compare', 'status'], 
                       help='要执行的操作')
    parser.add_argument('--repo', help='GitHub仓库 (用于analyze)')
    parser.add_argument('--topic', help='分析主题 (用于trend)')
    parser.add_argument('--projects', help='项目列表，逗号分隔 (用于compare)')
    parser.add_argument('--wait', action='store_true', help='等待任务完成')
    
    args = parser.parse_args()
    
    trigger = BackgroundAgentTrigger()
    
    if args.action == 'daily':
        trigger.trigger_daily_digest()
        if args.wait:
            result = trigger.wait_for_completion('daily_digest')
            print(f"结果: {result}")
            
    elif args.action == 'analyze':
        if not args.repo:
            print("❌ 请提供 --repo 参数")
            sys.exit(1)
        trigger.trigger_project_analysis(args.repo)
        if args.wait:
            result = trigger.wait_for_completion('analyze_project')
            print(f"结果: {result}")
            
    elif args.action == 'trend':
        trigger.trigger_trend_analysis(args.topic)
        if args.wait:
            result = trigger.wait_for_completion('trend_analysis')
            print(f"结果: {result}")
            
    elif args.action == 'compare':
        if not args.projects:
            print("❌ 请提供 --projects 参数")
            sys.exit(1)
        projects = [p.strip() for p in args.projects.split(',')]
        trigger.trigger_project_comparison(projects)
        if args.wait:
            result = trigger.wait_for_completion('compare_projects')
            print(f"结果: {result}")
            
    elif args.action == 'status':
        status = trigger.get_daemon_status()
        print(f"📊 系统状态: {json.dumps(status, ensure_ascii=False, indent=2)}")
        
        recent_reports = trigger.get_recent_outputs()
        if recent_reports:
            print(f"\n📄 最近报告 ({len(recent_reports)} 个):")
            for report in recent_reports[:5]:
                print(f"  - {os.path.basename(report['file'])} ({report['created'][:10]})")