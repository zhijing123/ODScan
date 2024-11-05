import concurrent.futures
import threading
import requests,optparse,sys,re,os
from bs4 import BeautifulSoup
from urllib.parse import urlparse

ODScan_banner = f"""
     _/_/    _/_/_/      _/_/_/                               
  _/    _/  _/    _/  _/          _/_/_/    _/_/_/  _/_/_/    
 _/    _/  _/    _/    _/_/    _/        _/    _/  _/    _/  帮您快速扫描目录泄露中的文件
_/    _/  _/    _/        _/  _/        _/    _/  _/    _/  https://github.com/zhijing123/ODScan
 _/_/    _/_/_/    _/_/_/      _/_/_/    _/_/_/  _/    _/  by zhijing
------------------------------------------------------------
"""
protocol=""
current_directory = ""
header = {'accept': 'text/html,application/xhtml+xml,application/xml',
          'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36',
          'referer': 'http://baidu.com'}
lock = threading.Lock()
count = 0

def is_ssl_used(url):
    return url.lower().startswith("https://")

def get_url_directory(url):
    parsed_url = urlparse(url)
    # urlparse返回的是一个ParseResult对象，它的path属性包含了URL的路径部分
    # 我们可以通过字符串操作来提取目录部分
    path = parsed_url.path
    if path.endswith('/'):
        # 如果路径以斜杠结尾，则移除它以获取目录
        path = path.rstrip('/')
    # 使用os.path模块来从路径中提取目录
    directory = os.path.dirname(path)
    return directory



def crawl_website(url,current_directory,options):
    # 发送HTTP请求

    response = requests.get(url,header,verify=False)

    # 检查请求是否成功
    if response.status_code != 200:
        print(f"Failed to retrieve the content from {url}. Status code: {response.status_code}")
        return None

    # 使用BeautifulSoup解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)

    # 查找所有的<a>标签
    a_tags = soup.find_all('a')


    with concurrent.futures.ThreadPoolExecutor(max_workers=options.thread_num) as executor:
        futures = {executor.submit(traversal, a_tag,current_directory,options):a_tag for a_tag in a_tags}


def traversal (a_tag,current_directory,options):
    # 遍历<a>标签并提取href属性
        href = a_tag.get('href')
        parsed_url = urlparse(options.url).netloc
        # 判断获取的href属性不为空，不为根目录，不为上级目录
        if href !="/" and href and current_directory !=href:
            url = protocol + parsed_url + href
            re_ = re.compile(r'[\w\.\/\:]+/$')
            if not re_.search(url):
                global count
                count= count +1
                print("[*]"+"["+str(count)+"]发现文件 " + url)
                if options.alive:
                    alive(url,parsed_url)

            # 对获取的href属性判断最后一个字符是否为/，如果为/，则为目录
            re_ = re.compile(r'[\w\.\/\:]+/$')
            if re_.search(href):
                # 获取当前目录，作为上级目录，与接下来递归中的href进行比较，保证不进入死循环
                current_directory = get_url_directory(url) + "/"
                # print("---------------------------")
                # print("[*]上级目录" + current_directory)
                print("[*]找到目录 "+url)
                crawl_website(url, current_directory,options)

def alive(url,parsed_url):
    if (not os.path.exists('export')):
        os.makedirs('export')


    # 发送GET请求获取文件内容
    response = requests.get(url, stream=True,verify=False)

    # 确保请求成功
    if response.status_code == 200:
        print("[+]" + url + "文件访问成功")
        with lock:
            with open("./export/"+parsed_url+'.txt', 'a', encoding='utf-8') as f:
                f.write(url+"\n")
    else:
        print("[+]" + url + "文件访问失败")


def download_file(url, filename,max,count):

    if (not os.path.exists('download')):
        os.makedirs('download')
    # 发送GET请求获取文件内容
    response = requests.get(url, stream=True,verify=False)

    # 确保请求成功
    response.raise_for_status()
    if response.status_code ==200:
        with lock:
            # 以二进制写入模式打开文件
            with open("./download/"+filename, 'wb') as file:
                # 分块读取响应内容并写入文件
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
                print("[+]"+"["+str(max -count)+"/"+str(max)+"]" + url + "下载成功")
    else:
        print("[-]" + "[" + str(max - count) + "/" + str(max) + "]" + url + "下载失败")



def extract_filename_from_url(url):
    pattern = r'/([^/]+)$'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None


if __name__ == "__main__":

    opt = optparse.OptionParser()
    opt.add_option("-u","--url",action="store",dest="url",help="指定url，例如http(s)://xxxx/ ")
    opt.add_option("--thread",action="store",dest="thread_num",type="int",default=5,
                   help="线程默认为5")
    opt.add_option("--alive",action="store_true",dest="alive",
                   help = "进行文件访问，访问后的结果自动保存./export下，以域名或ip为文件名的.txt文件")
    opt.add_option("--dump",action="store_true",dest="dump",
                   help = "下载文件至download下")
    (options, args) = opt.parse_args()
    print(ODScan_banner)
    if len(sys.argv) <2 :
        print("example: python ODScan.py -u http://192.168.0.1/ ")
        sys.exit()

    if not options.url:
        print("[-] URL Error!")
    url = options.url
    # 在拿到url后判断后面是否有/ 如果没有就加上
    re_ = re.compile(r'[\w\.\/\:]+/$')
    if not re_.search(url):
        url = url+"/"

    if is_ssl_used(url):
        protocol = "https://"
    else:
        protocol = "http://"

    # 进行扫描和存活探测
    crawl_website(url, current_directory,options)

    # 下载文件
    parsed_url = urlparse(options.url).netloc
    # print(filename)
    if options.dump:
        # 打开文件
        with open("./export/" + parsed_url + '.txt', 'r') as urls:
            max = len(urls.readlines())
            count = 0
        print("---------------开始下载文件---------------")
        print("共计下载"+str(max)+"个文件")
        with concurrent.futures.ThreadPoolExecutor(max_workers=options.thread_num) as executor:
            with open("./export/"+parsed_url+'.txt', 'r') as urls:
                # 遍历文件的每一行
                for url in urls:
                    filename = extract_filename_from_url(url.strip())
                    futures = {executor.submit(download_file,url.strip(), filename,max,count)}
                    count+=1


