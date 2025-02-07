import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

ODScan_banner = f"""
     _/_/    _/_/_/      _/_/_/                               
  _/    _/  _/    _/  _/          _/_/_/    _/_/_/  _/_/_/    
 _/    _/  _/    _/    _/_/    _/        _/    _/  _/    _/  帮您快速扫描目录泄露中的文件
_/    _/  _/    _/        _/  _/        _/    _/  _/    _/  https://github.com/zhijing123/ODScan
 _/_/    _/_/_/    _/_/_/      _/_/_/    _/_/_/  _/    _/  by zhijing
------------------------------------------------------------
"""

lock = threading.Lock()  # 线程锁，用于保护共享资源
file_count = 0  # 全局文件计数器

def is_directory(url):
    """
    判断URL是否指向一个目录（以'/'结尾的URL通常是目录）
    """
    return url.endswith('/')

def crawl_links(url, visited=None):
    """
    爬取网页链接，并递归处理目录
    :param url: 要爬取的URL
    :param visited: 已访问的URL集合，用于避免重复访问
    """
    if visited is None:
        visited = set()

    with lock:
        if url in visited:
            return
        print(f"Crawling: {url}")
        visited.add(url)

    try:
        # 获取网页内容
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        return

    # 解析HTML内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找所有链接
    links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        full_url = urljoin(url, href)  # 将相对URL转换为完整URL
        links.append(full_url)

    # 使用线程池处理链接
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for link in links:
            if is_directory(link):
                # 如果是目录，提交到线程池递归处理
                futures.append(executor.submit(crawl_links, link, visited))
            else:
                # 如果是文件，打印链接并增加计数器
                with lock:
                    global file_count
                    file_count += 1
                    print(f"Found file ({file_count}): {link}")

        # 等待所有任务完成
        for future in as_completed(futures):
            future.result()  # 捕获可能的异常

if __name__ == "__main__":
    print(ODScan_banner)
    # 输入要爬取的起始URL
    start_url = input("Enter the starting URL: ").strip()
    if not start_url.startswith(('http://', 'https://')):
        start_url = 'http://' + start_url

    # 开始爬取
    crawl_links(start_url)

    # 最终输出文件总数
    print(f"Total files found: {file_count}")
