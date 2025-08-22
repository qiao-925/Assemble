#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技术信息工作流守护进程
可以自主运行，支持定时任务和外部触发
"""

import os
import sys
import time
import json
import schedule
import logging
import threading
import signal
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tech_workflow import TechWorkflow

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/workflow_daemon.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TechWorkflowDaemon:
    """技术信息工作流守护进程"""
    
    def __init__(self, config_path: str = "config/workflow_config.yaml"):
        self.workflow = TechWorkflow(config_path)
        self.running = True
        self.config_path = config_path
        
        # 触发控制文件路径
        self.trigger_dir = Path("triggers")
        self.trigger_dir.mkdir(exist_ok=True)
        
        # 状态文件
        self.status_file = "daemon_status.json"
        
        # 确保日志目录存在
        Path("logs").mkdir(exist_ok=True)
        
        # 注册信号处理
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """处理系统信号"""
        logger.info(f"收到信号 {signum}，准备优雅退出...")
        self.running = False
    
    def start_daemon(self):
        """启动守护进程"""
        logger.info("🚀 技术信息工作流守护进程启动")
        
        # 更新状态
        self._update_status("running", "守护进程已启动")
        
        # 设置定时任务
        self._setup_scheduled_tasks()
        
        # 启动触发文件监听线程
        trigger_thread = threading.Thread(target=self._monitor_triggers, daemon=True)
        trigger_thread.start()
        
        # 主循环
        try:
            while self.running:
                # 执行定时任务
                schedule.run_pending()
                
                # 短暂休眠，避免CPU占用过高
                time.sleep(10)
                
        except KeyboardInterrupt:
            logger.info("用户中断，准备退出...")
        except Exception as e:
            logger.error(f"守护进程出错: {e}")
        finally:
            self._cleanup()
    
    def _setup_scheduled_tasks(self):
        """设置定时任务"""
        logger.info("📅 设置定时任务")
        
        # 每日技术摘要 - 每天8:00执行
        schedule.every().day.at("08:00").do(self._run_daily_digest)
        
        # 周度深度分析 - 每周一9:00执行
        schedule.every().monday.at("09:00").do(self._run_weekly_analysis)
        
        # 数据清理 - 每天凌晨2:00执行
        schedule.every().day.at("02:00").do(self._cleanup_old_data)
        
        logger.info("✅ 定时任务设置完成")
    
    def _run_daily_digest(self):
        """执行每日摘要任务"""
        try:
            logger.info("🌅 开始每日技术摘要生成")
            output_file = self.workflow.run_daily_digest()
            
            # 更新状态
            self._update_status("daily_completed", f"每日摘要已生成: {output_file}")
            
            # 创建成功标记文件，供外部检查
            self._create_completion_marker("daily_digest", output_file)
            
            logger.info(f"✅ 每日摘要完成: {output_file}")
            
        except Exception as e:
            logger.error(f"❌ 每日摘要生成失败: {e}")
            self._update_status("error", f"每日摘要失败: {e}")
    
    def _run_weekly_analysis(self):
        """执行周度深度分析"""
        try:
            logger.info("📊 开始周度技术趋势分析")
            
            # 生成多个主题的趋势报告
            topics = ["ai", "cloud-native", "database", "performance"]
            output_files = []
            
            for topic in topics:
                output_file = self.workflow.run_trending_analysis(topic)
                if output_file:
                    output_files.append(output_file)
            
            # 更新状态
            self._update_status("weekly_completed", f"周度分析已完成: {len(output_files)} 个报告")
            
            logger.info(f"✅ 周度分析完成: {len(output_files)} 个报告")
            
        except Exception as e:
            logger.error(f"❌ 周度分析失败: {e}")
            self._update_status("error", f"周度分析失败: {e}")
    
    def _monitor_triggers(self):
        """监听触发文件"""
        logger.info("👁️ 开始监听触发文件")
        
        while self.running:
            try:
                # 检查触发文件
                trigger_files = list(self.trigger_dir.glob("*.trigger"))
                
                for trigger_file in trigger_files:
                    self._process_trigger_file(trigger_file)
                
                time.sleep(5)  # 每5秒检查一次
                
            except Exception as e:
                logger.error(f"监听触发文件时出错: {e}")
                time.sleep(10)
    
    def _process_trigger_file(self, trigger_file: Path):
        """处理触发文件"""
        try:
            # 读取触发指令
            with open(trigger_file, 'r', encoding='utf-8') as f:
                trigger_data = json.load(f)
            
            command = trigger_data.get('command')
            params = trigger_data.get('params', {})
            
            logger.info(f"🔔 收到触发指令: {command}")
            
            # 执行相应命令
            output_file = None
            if command == 'daily_digest':
                output_file = self.workflow.run_daily_digest()
                
            elif command == 'analyze_project':
                repo = params.get('repo')
                if repo:
                    output_file = self.workflow.analyze_project(f"https://github.com/{repo}")
                    
            elif command == 'trend_analysis':
                topic = params.get('topic')
                output_file = self.workflow.run_trending_analysis(topic)
                
                         elif command == 'compare_projects':
                 projects = params.get('projects', [])
                 if len(projects) >= 2:
                     project_urls = [f"https://github.com/{p}" for p in projects]
                     output_file = self.workflow.compare_projects(project_urls)
             
             elif command == 'stop_daemon':
                 logger.info("🛑 收到停止信号，准备退出")
                 self.running = False
                 trigger_file.unlink()
                 return
             
             # 创建完成标记
             if output_file:
                 self._create_completion_marker(command, output_file)
                 logger.info(f"✅ 触发任务完成: {output_file}")
             
             # 删除触发文件
             trigger_file.unlink()
            
        except Exception as e:
            logger.error(f"处理触发文件失败: {e}")
            # 移动到错误目录
            error_dir = self.trigger_dir / "errors"
            error_dir.mkdir(exist_ok=True)
            trigger_file.rename(error_dir / trigger_file.name)
    
    def _create_completion_marker(self, task_type: str, output_file: str):
        """创建任务完成标记"""
        marker_dir = Path("completed")
        marker_dir.mkdir(exist_ok=True)
        
        marker_data = {
            'task_type': task_type,
            'output_file': output_file,
            'completed_at': datetime.now().isoformat(),
            'status': 'success'
        }
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        marker_file = marker_dir / f"{task_type}_{timestamp}.completed"
        
        with open(marker_file, 'w', encoding='utf-8') as f:
            json.dump(marker_data, f, ensure_ascii=False, indent=2)
    
    def _update_status(self, status: str, message: str):
        """更新守护进程状态"""
        status_data = {
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'uptime_seconds': (datetime.now() - self.start_time).total_seconds() if hasattr(self, 'start_time') else 0
        }
        
        with open(self.status_file, 'w', encoding='utf-8') as f:
            json.dump(status_data, f, ensure_ascii=False, indent=2)
    
    def _cleanup_old_data(self):
        """清理旧数据"""
        try:
            logger.info("🧹 开始清理旧数据")
            
            # 清理30天前的原始数据
            data_dir = Path("data")
            if data_dir.exists():
                cutoff_date = datetime.now() - timedelta(days=30)
                for file_path in data_dir.glob("tech_info_*.json"):
                    if file_path.stat().st_mtime < cutoff_date.timestamp():
                        file_path.unlink()
                        logger.info(f"删除旧数据文件: {file_path}")
            
            # 清理7天前的完成标记
            completed_dir = Path("completed")
            if completed_dir.exists():
                cutoff_date = datetime.now() - timedelta(days=7)
                for file_path in completed_dir.glob("*.completed"):
                    if file_path.stat().st_mtime < cutoff_date.timestamp():
                        file_path.unlink()
            
            logger.info("✅ 数据清理完成")
            
        except Exception as e:
            logger.error(f"数据清理失败: {e}")
    
    def _cleanup(self):
        """守护进程清理"""
        logger.info("🧹 守护进程清理中...")
        self._update_status("stopped", "守护进程已停止")

def create_systemd_service():
    """创建systemd服务文件"""
    service_content = f"""[Unit]
Description=Tech Info Workflow Daemon
After=network.target

[Service]
Type=simple
User={os.getenv('USER', 'root')}
WorkingDirectory={os.getcwd()}
Environment=PATH={os.environ.get('PATH')}
ExecStart={sys.executable} {os.path.abspath(__file__)} --daemon
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
    
    service_file = f"/etc/systemd/system/tech-workflow.service"
    print(f"📝 Systemd服务文件内容:")
    print(service_content)
    print(f"\n💡 要安装为系统服务，请运行:")
    print(f"sudo tee {service_file} << 'EOF'")
    print(service_content)
    print("EOF")
    print("sudo systemctl enable tech-workflow")
    print("sudo systemctl start tech-workflow")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='技术信息工作流守护进程')
    parser.add_argument('--daemon', action='store_true', help='以守护进程模式运行')
    parser.add_argument('--create-service', action='store_true', help='创建systemd服务文件')
    parser.add_argument('--status', action='store_true', help='查看守护进程状态')
    parser.add_argument('--stop', action='store_true', help='停止守护进程')
    
    args = parser.parse_args()
    
    if args.create_service:
        create_systemd_service()
        return
    
    if args.status:
        # 查看状态
        status_file = "daemon_status.json"
        if os.path.exists(status_file):
            with open(status_file, 'r', encoding='utf-8') as f:
                status = json.load(f)
            print(f"📊 守护进程状态: {status['status']}")
            print(f"📝 最后消息: {status['message']}")  
            print(f"⏰ 更新时间: {status['timestamp']}")
            if 'uptime_seconds' in status:
                uptime_hours = status['uptime_seconds'] / 3600
                print(f"⏱️ 运行时长: {uptime_hours:.1f} 小时")
        else:
            print("❌ 守护进程未运行或状态文件不存在")
        return
    
    if args.stop:
        # 创建停止信号文件
        stop_file = Path("triggers/stop_daemon.trigger")
        stop_data = {
            'command': 'stop_daemon',
            'timestamp': datetime.now().isoformat()
        }
        with open(stop_file, 'w', encoding='utf-8') as f:
            json.dump(stop_data, f, ensure_ascii=False, indent=2)
        print("🛑 停止信号已发送")
        return
    
    if args.daemon:
        # 启动守护进程
        daemon = TechWorkflowDaemon()
        daemon.start_time = datetime.now()
        daemon.start_daemon()
    else:
        # 显示帮助
        print("🤖 技术信息工作流守护进程")
        print("\n使用方式:")
        print("  python tech_workflow_daemon.py --daemon          # 启动守护进程")
        print("  python tech_workflow_daemon.py --status          # 查看状态")  
        print("  python tech_workflow_daemon.py --stop            # 停止守护进程")
        print("  python tech_workflow_daemon.py --create-service  # 创建系统服务")

if __name__ == "__main__":
    main()