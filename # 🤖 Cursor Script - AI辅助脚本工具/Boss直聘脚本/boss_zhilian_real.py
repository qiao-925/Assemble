#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Boss直聘批量投递简历脚本 - 真实运行版
功能：自动筛选职位并批量投递简历

作者：AI Assistant
版本：v1.0-real
"""

import time
import json
import logging
import random
from datetime import datetime
from typing import Dict, List, Optional
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os

class BossZhilianBatchApplyReal:
    """Boss直聘批量投递简历主类 - 真实运行版"""
    
    def __init__(self):
        self.driver = None
        self.is_logged_in = False
        self.session = requests.Session()
        self.config = self.load_config()
        self.setup_logging()
        
    def setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('boss_zhilian.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_config(self) -> Dict:
        """加载配置文件"""
        config_file = 'boss_config.json'
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"加载配置文件失败: {e}")
        
        # 默认配置
        default_config = {
            "search_conditions": {
                "keywords": ["Java开发", "Python开发", "前端开发"],
                "city": "北京",
                "salary_min": 15000,
                "salary_max": 30000,
                "experience": "3-5年",
                "education": "本科",
                "company_size": ["100-499人", "500-999人", "1000-9999人"]
            },
            "apply_settings": {
                "max_applications_per_day": 50,
                "delay_between_applies": [3, 8],
                "auto_refresh_jobs": True,
                "skip_applied": True
            },
            "browser_settings": {
                "headless": False,
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        }
        
        # 保存默认配置
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
            
        return default_config
    
    def init_browser(self):
        """初始化浏览器"""
        try:
            chrome_options = Options()
            
            if self.config["browser_settings"]["headless"]:
                chrome_options.add_argument("--headless")
            
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument(f"user-agent={self.config['browser_settings']['user_agent']}")
            
            # 尝试使用webdriver-manager自动下载ChromeDriver
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                from selenium.webdriver.chrome.service import Service
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            except:
                # 如果webdriver-manager不可用，尝试直接使用Chrome
                self.driver = webdriver.Chrome(options=chrome_options)
            
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.logger.info("浏览器初始化成功")
            return True
            
        except Exception as e:
            self.logger.error(f"浏览器初始化失败: {e}")
            return False
    
    def login_with_qr(self) -> bool:
        """使用二维码登录"""
        try:
            self.logger.info("开始二维码登录流程...")
            
            # 访问Boss直聘登录页面
            self.driver.get("https://www.zhipin.com/")
            time.sleep(3)
            
            self.logger.info("已打开Boss直聘网站，请手动完成登录...")
            self.logger.info("登录成功后，请按回车键继续...")
            
            # 等待用户手动登录
            input("登录完成后请按回车键继续...")
            
            # 检查登录状态
            if self.check_login_status():
                self.is_logged_in = True
                self.logger.info("登录成功！")
                return True
            else:
                self.logger.warning("登录状态检查失败，请确保已登录")
                return False
                
        except Exception as e:
            self.logger.error(f"登录过程出错: {e}")
            return False
    
    def check_login_status(self) -> bool:
        """检查登录状态"""
        try:
            # 检查是否存在用户头像或用户名等登录后的元素
            user_avatar = self.driver.find_elements(By.CSS_SELECTOR, ".user-avatar, .user-name, .user-info")
            if len(user_avatar) > 0:
                return True
            
            # 检查URL是否包含登录后的标识
            current_url = self.driver.current_url
            if "login" not in current_url and "auth" not in current_url:
                return True
                
            return False
        except:
            return False
    
    def search_jobs(self) -> List[Dict]:
        """搜索符合条件的职位"""
        try:
            self.logger.info("开始搜索职位...")
            
            # 构建搜索URL
            search_url = self.build_search_url()
            self.logger.info(f"正在访问搜索页面: {search_url}")
            
            self.driver.get(search_url)
            time.sleep(5)
            
            self.logger.info("正在等待页面加载...")
            
            # 等待职位列表加载
            try:
                job_elements = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card-wrapper, .job-list-item, .job-item"))
                )
                self.logger.info(f"找到 {len(job_elements)} 个职位元素")
            except TimeoutException:
                self.logger.warning("等待职位列表超时，尝试其他选择器...")
                # 尝试其他可能的选择器
                job_elements = self.driver.find_elements(By.CSS_SELECTOR, ".job-card, .job-item, .job-list-item, [class*='job']")
                self.logger.info(f"使用备用选择器找到 {len(job_elements)} 个职位元素")
            
            jobs = []
            for i, job_element in enumerate(job_elements[:10]):  # 限制前10个职位
                try:
                    job_info = self.extract_job_info(job_element)
                    if job_info and self.filter_job(job_info):
                        jobs.append(job_info)
                        self.logger.info(f"找到合适职位: {job_info['title']} - {job_info['company']}")
                except Exception as e:
                    self.logger.warning(f"提取职位信息失败: {e}")
                    continue
            
            self.logger.info(f"搜索完成，共找到 {len(jobs)} 个符合条件的职位")
            return jobs
            
        except Exception as e:
            self.logger.error(f"搜索职位失败: {e}")
            return []
    
    def build_search_url(self) -> str:
        """构建搜索URL"""
        conditions = self.config["search_conditions"]
        base_url = "https://www.zhipin.com/web/geek/job"
        
        params = []
        if conditions["keywords"]:
            params.append(f"query={'+'.join(conditions['keywords'])}")
        if conditions["city"]:
            params.append(f"city={conditions['city']}")
        if conditions["salary_min"]:
            params.append(f"salary={conditions['salary_min']}-{conditions['salary_max']}")
        
        if params:
            return f"{base_url}?{'&'.join(params)}"
        return base_url
    
    def extract_job_info(self, job_element) -> Optional[Dict]:
        """提取职位信息"""
        try:
            job_info = {}
            
            # 尝试多种选择器来提取职位信息
            selectors = {
                "title": [".job-name", ".job-title", ".title", "h3", "h4"],
                "company": [".company-name", ".company", ".employer"],
                "salary": [".salary", ".pay", ".compensation"],
                "url": ["a", ".job-link", ".title a"]
            }
            
            # 提取职位名称
            for selector in selectors["title"]:
                try:
                    title_elem = job_element.find_element(By.CSS_SELECTOR, selector)
                    job_info["title"] = title_elem.text.strip()
                    break
                except:
                    continue
            
            # 提取公司名称
            for selector in selectors["company"]:
                try:
                    company_elem = job_element.find_element(By.CSS_SELECTOR, selector)
                    job_info["company"] = company_elem.text.strip()
                    break
                except:
                    continue
            
            # 提取薪资
            for selector in selectors["salary"]:
                try:
                    salary_elem = job_element.find_element(By.CSS_SELECTOR, selector)
                    job_info["salary"] = salary_elem.text.strip()
                    break
                except:
                    continue
            
            # 提取职位链接
            for selector in selectors["url"]:
                try:
                    link_elem = job_element.find_element(By.CSS_SELECTOR, selector)
                    job_info["url"] = link_elem.get_attribute("href")
                    break
                except:
                    continue
            
            # 如果没有找到必要信息，返回None
            if not job_info.get("title") or not job_info.get("company"):
                return None
            
            # 如果没有URL，尝试构建一个
            if not job_info.get("url"):
                job_info["url"] = f"https://www.zhipin.com/job/{hash(job_info['title'])}"
            
            return job_info
            
        except Exception as e:
            self.logger.warning(f"提取职位信息失败: {e}")
            return None
    
    def filter_job(self, job_info: Dict) -> bool:
        """筛选职位是否符合条件"""
        conditions = self.config["search_conditions"]
        
        # 检查薪资范围
        salary_text = job_info.get("salary", "")
        if conditions["salary_min"] and conditions["salary_max"] and salary_text:
            if "K" in salary_text:
                try:
                    salary_range = salary_text.replace("K", "").split("-")
                    if len(salary_range) == 2:
                        min_sal = int(salary_range[0]) * 1000
                        max_sal = int(salary_range[1]) * 1000
                        if min_sal < conditions["salary_min"] or max_sal > conditions["salary_max"]:
                            return False
                except:
                    pass
        
        return True
    
    def apply_job(self, job_info: Dict) -> bool:
        """投递简历到指定职位"""
        try:
            self.logger.info(f"正在投递简历到: {job_info['title']} - {job_info['company']}")
            
            # 打开职位详情页
            self.driver.get(job_info["url"])
            time.sleep(3)
            
            # 尝试多种投递按钮选择器
            apply_selectors = [
                ".btn-apply", ".apply-btn", ".apply-button", 
                "button[class*='apply']", "button[class*='投递']",
                ".btn-primary", ".btn", "button"
            ]
            
            apply_btn = None
            for selector in apply_selectors:
                try:
                    apply_btn = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    if "投递" in apply_btn.text or "apply" in apply_btn.text.lower():
                        break
                except:
                    continue
            
            if not apply_btn:
                self.logger.warning(f"未找到投递按钮: {job_info['title']}")
                return False
            
            # 点击投递按钮
            self.logger.info("找到投递按钮，正在点击...")
            apply_btn.click()
            time.sleep(2)
            
            # 尝试确认投递
            confirm_selectors = [".confirm-btn", ".btn-confirm", ".ok-btn", "button[class*='confirm']"]
            for selector in confirm_selectors:
                try:
                    confirm_btn = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    confirm_btn.click()
                    self.logger.info("确认投递成功")
                    break
                except:
                    continue
            
            # 等待投递结果
            time.sleep(3)
            
            # 检查投递状态
            success_selectors = [".success-msg", ".apply-success", ".success", ".message"]
            for selector in success_selectors:
                try:
                    success_msg = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if success_msg:
                        self.logger.info(f"投递成功: {job_info['title']}")
                        return True
                except:
                    continue
            
            self.logger.warning(f"投递状态不明确: {job_info['title']}")
            return False
                
        except Exception as e:
            self.logger.error(f"投递简历失败: {e}")
            return False
    
    def batch_apply(self, jobs: List[Dict]):
        """批量投递简历"""
        if not jobs:
            self.logger.warning("没有找到符合条件的职位")
            return
        
        self.logger.info(f"开始批量投递，共 {len(jobs)} 个职位")
        
        applied_count = 0
        failed_count = 0
        
        for i, job in enumerate(jobs, 1):
            try:
                self.logger.info(f"进度: {i}/{len(jobs)}")
                
                if self.apply_job(job):
                    applied_count += 1
                    # 记录投递成功的职位
                    self.record_applied_job(job)
                else:
                    failed_count += 1
                
                # 随机延迟，避免被检测
                delay = random.randint(*self.config["apply_settings"]["delay_between_applies"])
                self.logger.info(f"等待 {delay} 秒后继续...")
                time.sleep(delay)
                
                # 检查每日投递限制
                if applied_count >= self.config["apply_settings"]["max_applications_per_day"]:
                    self.logger.info("已达到每日投递限制")
                    break
                    
            except Exception as e:
                self.logger.error(f"处理职位 {job['title']} 时出错: {e}")
                failed_count += 1
                continue
        
        self.logger.info(f"批量投递完成！成功: {applied_count}, 失败: {failed_count}")
    
    def record_applied_job(self, job_info: Dict):
        """记录已投递的职位"""
        try:
            applied_jobs_file = "applied_jobs.json"
            applied_jobs = []
            
            if os.path.exists(applied_jobs_file):
                with open(applied_jobs_file, 'r', encoding='utf-8') as f:
                    applied_jobs = json.load(f)
            
            job_record = {
                "title": job_info["title"],
                "company": job_info["company"],
                "url": job_info["url"],
                "applied_time": datetime.now().isoformat(),
                "status": "applied"
            }
            
            applied_jobs.append(job_record)
            
            with open(applied_jobs_file, 'w', encoding='utf-8') as f:
                json.dump(applied_jobs, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            self.logger.warning(f"记录投递职位失败: {e}")
    
    def run(self):
        """运行主程序"""
        try:
            self.logger.info("启动Boss直聘批量投递脚本（真实运行版）...")
            
            # 初始化浏览器
            if not self.init_browser():
                return
            
            # 登录
            if not self.login_with_qr():
                self.logger.error("登录失败，程序退出")
                return
            
            # 搜索职位
            jobs = self.search_jobs()
            
            # 批量投递
            if jobs:
                self.batch_apply(jobs)
            else:
                self.logger.info("未找到符合条件的职位")
            
        except KeyboardInterrupt:
            self.logger.info("用户中断程序")
        except Exception as e:
            self.logger.error(f"程序运行出错: {e}")
        finally:
            if self.driver:
                self.driver.quit()
                self.logger.info("浏览器已关闭")

def main():
    """主函数"""
    bot = BossZhilianBatchApplyReal()
    bot.run()

if __name__ == "__main__":
    main()
