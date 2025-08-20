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

def replace_internal_md_links(content):
    """
    查找内容中所有指向本地 .md 文件的链接，并将其替换为博客园站内搜索链接。
    例如，将 [链接文本](./some-article.md)
    替换为 [链接文本](https://zzk.cnblogs.com/my/s/blogpost-p?Keywords=some-article )
    """
    # 正则表达式：查找所有 Markdown 链接 `[text](url)`
    # - (\[.*?\]): 分组1, 匹配链接文本，如 `[some text]`
    # - \(: 匹配左括号
    # - (.*?\.md): 分组2, 懒惰匹配所有以 `.md` 结尾的 URL
    # - \): 匹配右括号
    md_link_pattern = re.compile(r'(\[.*?\])\((.*?\.md)\)')

    def replacer(match):
        """
        这是一个替换函数，会作为 re.sub 的参数被调用。
        它接收一个匹配对象，并返回替换后的字符串。
        """
        link_text = match.group(1)  # 获取链接文本，例如 `[查看详情]`
        md_path = match.group(2)    # 获取md文件路径，例如 `./other-post.md`

        # 从路径中提取文件名，并移除 .md 后缀，作为搜索关键词
        # os.path.basename 会处理 `./` 或 `../` 等情况
        keyword = os.path.basename(md_path).replace('.md', '')

        # 对关键词进行 URL 编码
        encoded_keyword = quote(keyword)

        # 构建新的博客园站内搜索 URL
        new_url = f"https://zzk.cnblogs.com/my/s/blogpost-p?Keywords={encoded_keyword}"

        # 返回重组后的新 Markdown 链接
        return f"{link_text}({new_url} )"

    # 使用 re.sub 和自定义的替换函数来处理整个文本内容
    return md_link_pattern.sub(replacer, content)


def post_to_cnblogs(title, content, categories=None):
    """发布文章到博客园"""

    # --- 核心功能：在发布前，处理文章内容中的内部链接 ---
    processed_content = replace_internal_md_links(content)
    # --- 功能结束 ---

    final_categories = ['[Markdown]']
    if categories and isinstance(categories, list):
        final_categories.extend(categories)
    else:
        final_categories.append('[随笔分类]')

    post = {
        'title': title,
        'description': processed_content, # 使用处理过链接的内容
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
