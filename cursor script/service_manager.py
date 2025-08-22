#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技术信息工作流服务管理器
简化守护进程的启动、停止和监控
"""

import os
import sys
import json
import subprocess
import time
import signal
from datetime import datetime
from pathlib import Path
from typing import Dict

class ServiceManager:
    """服务管理器"""
    
    def __init__(self):
        self.work_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        self.pid_file = self.work_dir / "daemon.pid"
        self.log_file = self.work_dir / "logs" / "service_manager.log"
        
        # 确保日志目录存在
        self.log_file.parent.mkdir(exist_ok=True)
    
    def start_service(self, detached: bool = True):
        """启动服务"""
        if self.is_running():
            print("⚠️ 服务已在运行中")
            return False
        
        print("🚀 启动技术信息工作流服务...")
        
        # 构建启动命令
        daemon_script = self.work_dir / "tech_workflow_daemon.py"
        
        if detached:
            # 后台运行
            cmd = [
                sys.executable, str(daemon_script), "--daemon"
            ]
            
            with open(self.log_file, 'a', encoding='utf-8') as log_f:
                process = subprocess.Popen(
                    cmd,
                    stdout=log_f,
                    stderr=subprocess.STDOUT,
                    cwd=str(self.work_dir),
                    start_new_session=True  # 创建新会话，脱离当前终端
                )
            
            # 保存PID
            with open(self.pid_file, 'w') as f:
                f.write(str(process.pid))
            
            # 等待一下确认启动成功
            time.sleep(2)
            
            if self.is_running():
                print(f"✅ 服务启动成功 (PID: {process.pid})")
                print(f"📋 状态查看: python service_manager.py status")
                print(f"📄 日志文件: {self.log_file}")
                return True
            else:
                print("❌ 服务启动失败，请检查日志")
                return False
        else:
            # 前台运行（用于调试）
            cmd = [sys.executable, str(daemon_script), "--daemon"]
            subprocess.run(cmd, cwd=str(self.work_dir))
            return True
    
    def stop_service(self):
        """停止服务"""
        if not self.is_running():
            print("⚠️ 服务未运行")
            return False
        
        print("🛑 正在停止服务...")
        
        try:
            # 读取PID
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            # 发送TERM信号
            os.kill(pid, signal.SIGTERM)
            
            # 等待进程结束
            for i in range(10):
                if not self.is_running():
                    break
                time.sleep(1)
            
            # 如果还在运行，强制结束
            if self.is_running():
                print("⚠️ 优雅停止失败，强制结束...")
                os.kill(pid, signal.SIGKILL)
                time.sleep(1)
            
            # 清理PID文件
            if self.pid_file.exists():
                self.pid_file.unlink()
            
            print("✅ 服务已停止")
            return True
            
        except (FileNotFoundError, ProcessLookupError):
            # 进程已不存在，清理PID文件
            if self.pid_file.exists():
                self.pid_file.unlink()
            print("✅ 服务已停止")
            return True
        except Exception as e:
            print(f"❌ 停止服务失败: {e}")
            return False
    
    def restart_service(self):
        """重启服务"""
        print("🔄 重启服务...")
        self.stop_service()
        time.sleep(2)
        return self.start_service()
    
    def is_running(self) -> bool:
        """检查服务是否运行"""
        if not self.pid_file.exists():
            return False
        
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            # 检查进程是否存在
            os.kill(pid, 0)  # 发送0信号检查进程是否存在
            return True
            
        except (FileNotFoundError, ProcessLookupError, ValueError):
            return False
    
    def get_status(self) -> Dict:
        """获取详细状态"""
        status = {
            'service_running': self.is_running(),
            'timestamp': datetime.now().isoformat()
        }
        
        # 读取守护进程状态
        daemon_status_file = self.work_dir / "daemon_status.json"
        if daemon_status_file.exists():
            try:
                with open(daemon_status_file, 'r', encoding='utf-8') as f:
                    daemon_status = json.load(f)
                status.update(daemon_status)
            except Exception as e:
                status['daemon_error'] = str(e)
        
        # 读取PID
        if self.pid_file.exists():
            try:
                with open(self.pid_file, 'r') as f:
                    status['pid'] = int(f.read().strip())
            except Exception:
                pass
        
        return status
    
    def show_logs(self, lines: int = 50):
        """显示最近的日志"""
        log_files = [
            self.work_dir / "logs" / "workflow_daemon.log",
            self.log_file
        ]
        
        print(f"📄 最近 {lines} 行日志:")
        print("=" * 60)
        
        for log_file in log_files:
            if log_file.exists():
                print(f"\n📁 {log_file.name}:")
                try:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        log_lines = f.readlines()
                        for line in log_lines[-lines:]:
                            print(f"  {line.rstrip()}")
                except Exception as e:
                    print(f"❌ 读取日志失败: {e}")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='技术信息工作流服务管理器')
    parser.add_argument('action', 
                       choices=['start', 'stop', 'restart', 'status', 'logs'],
                       help='服务操作')
    parser.add_argument('--foreground', action='store_true', 
                       help='前台运行（仅用于start）')
    parser.add_argument('--lines', type=int, default=50,
                       help='显示日志行数（用于logs）')
    
    args = parser.parse_args()
    
    manager = ServiceManager()
    
    if args.action == 'start':
        manager.start_service(detached=not args.foreground)
        
    elif args.action == 'stop':
        manager.stop_service()
        
    elif args.action == 'restart':
        manager.restart_service()
        
    elif args.action == 'status':
        status = manager.get_status()
        
        print("📊 服务状态报告")
        print("=" * 40)
        print(f"🔄 服务运行: {'✅ 是' if status['service_running'] else '❌ 否'}")
        
        if 'pid' in status:
            print(f"🆔 进程ID: {status['pid']}")
        
        if 'status' in status:
            print(f"📋 守护进程状态: {status['status']}")
            print(f"📝 最后消息: {status.get('message', 'N/A')}")
        
        if 'uptime_seconds' in status:
            uptime_hours = status['uptime_seconds'] / 3600
            print(f"⏱️ 运行时长: {uptime_hours:.1f} 小时")
        
        # 显示最近的任务完成情况
        from bg_agent_trigger import BackgroundAgentTrigger
        trigger = BackgroundAgentTrigger()
        recent_reports = trigger.get_recent_outputs(3)
        
        if recent_reports:
            print(f"\n📄 最近报告 ({len(recent_reports)} 个):")
            for report in recent_reports[:3]:
                print(f"  - {os.path.basename(report['file'])} ({report['created'][:16]})")
        
    elif args.action == 'logs':
        manager.show_logs(args.lines)

if __name__ == "__main__":
    main()