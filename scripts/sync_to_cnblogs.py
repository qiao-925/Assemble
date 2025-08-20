# scripts/sync_to_cnblogs.py

import os
import sys
import xmlrpc.client
from datetime import datetime
from urllib.parse import quote # 导入用于 URL 编码的模块

# --- 配置信息 ---
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

    # --- 新增功能：在内容前补充关联知识库链接 ---
    # 1. 对标题进行 URL 编码，以安全地放入 URL 中
    encoded_title = quote(title)

    # 2. 构建完整的知识库链接
    knowledge_base_url = f"https://assemble.gitbook.io/assemble?q={encoded_title}"

    # 3. 创建 Markdown 引用格式的补充内容 ，并添加两个换行符以确保与正文分隔
    prepend_content = f"> 关联知识库：[链接]({knowledge_base_url})\n\n"

    # 4. 将补充内容添加到文章原始内容的前面
    final_content = prepend_content + content
    # --- 新增功能结束 ---

    # --- 核心修复：采用参考脚本的正确逻辑 ---
    # 将 '[Markdown]' 作为一个特殊的分类提交
    # 这是触发博客园 Markdown 渲染器的正确方式
    final_categories = ['[Markdown]']

    # 如果用户还想添加其他分类，可以进行合并
    if categories and isinstance(categories, list):
        final_categories.extend(categories)
    else:
        # 如果没有其他分类，可以添加一个默认的随笔分类
        final_categories.append('[随笔分类]')

    post = {
        'title': title,
        'description': final_content, # 使用添加了前缀的 final_content
        'dateCreated': datetime.now(),
        'categories': final_categories, # 使用包含 '[Markdown]' 的分类列表
        'publish': True
    }

    # 连接服务器并发布
    try:
        server = xmlrpc.client.ServerProxy(RPC_URL)
        post_id = server.metaWeblog.newPost(BLOG_ID, USERNAME, PASSWORD, post, post['publish'])
        print(f"✅ 成功发布文章 '{title}'，文章ID: {post_id}")
        return post_id
    except Exception as e:
        print(f"❌ 发布文章 '{title}' 失败: {e}")
        return None

# --- 主逻辑 (保持不变) ---

if __name__ == "__main__":
    if not all([RPC_URL, BLOG_ID, USERNAME, PASSWORD]):
        print("❌ 错误：一个或多个环境变量未设置。")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("🟡 用法: python sync_to_cnblogs.py <file1.md> ...")
        sys.exit(0)

    files_to_publish = sys.argv[1:]
    print(f"🚀 准备发布以下文件: {files_to_publish}")

    for md_file in files_to_publish:
        if not os.path.exists(md_file):
            print(f"⚠️ 文件 '{md_file}' 不存在，跳过。")
            continue

        # 注意：这里的标题是从文件名生成的，如果文件名包含空格，链接也会正确处理
        post_title = os.path.basename(md_file).replace('.md', '')
        post_content = get_file_content(md_file)

        # 未来可以从文件元数据中提取真实分类
        post_to_cnblogs(post_title, post_content)
