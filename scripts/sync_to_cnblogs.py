# scripts/sync_to_cnblogs.py

import os
import sys
import re
import xmlrpc.client
from datetime import datetime
from urllib.parse import quote

# --- 配置信息 ---
RPC_URL = os.environ.get("CNBLOGS_RPC_URL")
BLOG_ID = os.environ.get("CNBLOGS_BLOG_ID")
USERNAME = os.environ.get("CNBLOGS_USERNAME")
PASSWORD = os.environ.get("CNBLOGS_PASSWORD")

# --- 本地化开关 ---
# True:  强制覆盖模式。如果文章已存在，会用新内容覆盖它。
# False: 安全同步模式。如果文章已存在，会直接跳过，不作任何修改。
FORCE_OVERWRITE_EXISTING = True

# --- 函数定义 ---

def get_file_content(filepath):
    """读取文件内容"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def replace_internal_md_links(content):
    """查找内容中所有指向本地 .md 文件的链接，并将其替换为博客园站内搜索链接。"""
    md_link_pattern = re.compile(r'(\[.*?\])\((.*?\.md)\)')
    def replacer(match):
        link_text = match.group(1)
        md_path = match.group(2)
        keyword = os.path.basename(md_path).replace('.md', '')
        encoded_keyword = quote(keyword)
        new_url = f"https://zzk.cnblogs.com/my/s/blogpost-p?Keywords={encoded_keyword}"
        return f"{link_text}({new_url} )"
    return md_link_pattern.sub(replacer, content)

def get_existing_post_id(server, title):
    """通过标题查询博客园，看文章是否已存在。如果存在，返回 post_id；否则返回 None。"""
    try:
        recent_posts = server.metaWeblog.getRecentPosts(BLOG_ID, USERNAME, PASSWORD, 100)
        for post in recent_posts:
            if post.get('title') == title:
                print(f"🔍 发现已存在同名文章 '{title}'，Post ID: {post['postid']}")
                return post['postid']
        return None
    except Exception as e:
        print(f"⚠️ 查询文章列表时出错: {e}。")
        return None

def post_to_cnblogs(title, content, categories=None):
    """发布文章到博客园，根据 FORCE_OVERWRITE_EXISTING 开关决定行为。"""
    # --- 步骤1: 准备最终内容 (逻辑不变) ---
    encoded_title = quote(title)
    knowledge_base_url = f"https://assemble.gitbook.io/assemble?q={encoded_title}"
    prepend_content = f"> 关联知识库：[链接]({knowledge_base_url} )\n\n"
    processed_body = replace_internal_md_links(content)
    final_content = prepend_content + processed_body

    # --- 步骤2: 准备 post 数据结构 ---
    final_categories = ['[Markdown]']
    if categories and isinstance(categories, list):
        final_categories.extend(categories)
    else:
        final_categories.append('[随笔分类]')

    post_data = {
        'title': title,
        'description': final_content,
        'categories': final_categories,
        'publish': True
    }

    # --- 步骤3: 核心发布/更新/跳过逻辑 ---
    try:
        server = xmlrpc.client.ServerProxy(RPC_URL)

        # 检查文章是否已存在
        existing_post_id = get_existing_post_id(server, title)

        if existing_post_id:
            # 文章已存在，根据开关决定下一步操作
            if FORCE_OVERWRITE_EXISTING:
                # 开关开启，执行覆盖更新
                print(f"ℹ️ 强制覆盖模式已开启。正在更新文章 '{title}'...")
                success = server.metaWeblog.editPost(existing_post_id, USERNAME, PASSWORD, post_data, post_data['publish'])
                if success:
                    print(f"✅ 成功覆盖更新文章 '{title}'，Post ID: {existing_post_id}")
                else:
                    print(f"❌ 覆盖更新文章 '{title}' 失败。")
            else:
                # 开关关闭，直接跳过
                print(f"ℹ️ 安全同步模式已开启。文章 '{title}' 已存在，将直接跳过。")
                return # 结束当前函数执行
        else:
            # 文章不存在，总是创建新文章
            print(f"📄 未找到文章 '{title}'，将创建新文章。")
            new_post_id = server.metaWeblog.newPost(BLOG_ID, USERNAME, PASSWORD, post_data, post_data['publish'])
            print(f"✅ 成功发布新文章 '{title}'，文章ID: {new_post_id}")

    except Exception as e:
        print(f"❌ 发布或更新文章 '{title}' 时发生严重错误: {e}")

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

        post_title = os.path.basename(md_file).replace('.md', '')
        post_content = get_file_content(md_file)

        post_to_cnblogs(post_title, post_content)
