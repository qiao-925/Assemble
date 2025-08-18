# scripts/sync_to_cnblogs.py

import os
import sys
import xmlrpc.client
from datetime import datetime

# --- 配置信息 ---
# 从 GitHub Actions 的环境变量中获取 Secrets
RPC_URL = os.environ.get("CNBLOGS_RPC_URL")
BLOG_ID = os.environ.get("CNBLOGS_BLOG_ID")
USERNAME = os.environ.get("CNBLOGS_USERNAME")
PASSWORD = os.environ.get("CNBLOGS_PASSWORD")

# --- 函数定义 ---

def get_file_content(filepath):
    """读取文件内容"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def post_to_cnblogs(title, content, categories=None):
    """发布文章到博客园"""
    if categories is None:
        categories = ['[随笔分类]'] # 默认分类

    # 准备文章结构体
    post = {
        'title': title,
        'description': content,
        'dateCreated': datetime.now(),
        'categories': categories,
        'publish': True  # True 表示发布，False 表示存为草稿
    }

    # 连接服务器并发布
    try:
        server = xmlrpc.client.ServerProxy(RPC_URL)
        # newPost(blogid, username, password, post_struct, publish)
        post_id = server.metaWeblog.newPost(BLOG_ID, USERNAME, PASSWORD, post, True)
        print(f"✅ 成功发布文章 '{title}'，文章ID: {post_id}")
        return post_id
    except Exception as e:
        print(f"❌ 发布文章 '{title}' 失败: {e}")
        return None

# --- 主逻辑 ---

if __name__ == "__main__":
    # 检查 Secrets 是否已设置
    if not all([RPC_URL, BLOG_ID, USERNAME, PASSWORD]):
        print("❌ 错误：一个或多个环境变量 (CNBLOGS_RPC_URL, CNBLOGS_BLOG_ID, USERNAME, PASSWORD) 未设置。")
        sys.exit(1)

    # 从命令行参数获取需要发布的 Markdown 文件路径
    # GitHub Actions 会将文件路径作为参数传递给这个脚本
    if len(sys.argv) < 2:
        print("🟡 用法: python sync_to_cnblogs.py <file1.md> [file2.md] ...")
        sys.exit(0) # 如果没有文件，则正常退出

    files_to_publish = sys.argv[1:]
    print(f"🚀 准备发布以下文件: {files_to_publish}")

    for md_file in files_to_publish:
        if not os.path.exists(md_file):
            print(f"⚠️ 文件 '{md_file}' 不存在，跳过。")
            continue
        
        # 使用文件名作为文章标题 (去除.md后缀)
        post_title = os.path.basename(md_file).replace('.md', '')
        post_content = get_file_content(md_file)
        
        # 你可以在这里添加更复杂的逻辑，比如从文件元数据中提取标题和分类
        # 例如，如果文件开头有 "--- title: My Title ---" 这样的 front-matter
        
        post_to_cnblogs(post_title, post_content)

