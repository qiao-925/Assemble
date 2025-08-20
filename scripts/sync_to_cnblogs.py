# scripts/sync_to_cnblogs.py

import os
import sys
import re # 导入正则表达式模块
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

# --- 新增的辅助函数 ---
def replace_internal_md_links(content):
    """
    查找内容中所有指向本地 .md 文件的链接，并将其替换为博客园站内搜索链接。
    """
    # 正则表达式，用于匹配 Markdown 格式的链接，其 URL 以 .md 结尾
    md_link_pattern = re.compile(r'(\[.*?\])\((.*?\.md)\)')

    def replacer(match):
        """用于 re.sub 的替换函数"""
        link_text = match.group(1)  # 链接文本，如 `[查看详情]`
        md_path = match.group(2)    # .md 文件路径，如 `./other-post.md`

        # 从路径中提取文件名作为搜索关键词
        keyword = os.path.basename(md_path).replace('.md', '')

        # 对关键词进行 URL 编码
        encoded_keyword = quote(keyword)

        # 构建新的博客园站内搜索 URL
        new_url = f"https://zzk.cnblogs.com/my/s/blogpost-p?Keywords={encoded_keyword}"

        # 返回完整的新 Markdown 链接
        return f"{link_text}({new_url} )"

    # 在整个内容上执行查找和替换
    return md_link_pattern.sub(replacer, content)
# --- 新增函数结束 ---


def post_to_cnblogs(title, content, categories=None):
    """发布文章到博客园"""

    # --- 步骤1: 保留您原有的功能，在内容前补充 GitBook 知识库链接 ---
    encoded_title = quote(title)
    knowledge_base_url = f"https://assemble.gitbook.io/assemble?q={encoded_title}"
    prepend_content = f"> 关联知识库：[链接]({knowledge_base_url} )\n\n"

    # --- 步骤2: 在原始的 content 上执行我们新增的内部链接替换功能 ---
    processed_body = replace_internal_md_links(content)

    # --- 步骤3: 将顶部引用和处理后的正文结合起来 ---
    final_content = prepend_content + processed_body

    # --- 发布逻辑 (基于您提供的代码) ---
    final_categories = ['[Markdown]']
    if categories and isinstance(categories, list):
        final_categories.extend(categories)
    else:
        final_categories.append('[随笔分类]')

    post = {
        'title': title,
        'description': final_content, # 使用我们组合后的最终内容
        'dateCreated': datetime.now(),
        'categories': final_categories,
        'publish': True
    }

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

        post_title = os.path.basename(md_file).replace('.md', '')
        post_content = get_file_content(md_file)

        post_to_cnblogs(post_title, post_content)
