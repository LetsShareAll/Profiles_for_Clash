import re
import subprocess
import sys
import time
from threading import Thread
from urllib import request
from urllib.parse import urlencode
from urllib.request import urlretrieve

from bs4 import BeautifulSoup

urls = ['https://github.com/Alvin9999/new-pac/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7',
        'https://github.com/Alvin9999/new-pac/wiki/v2ray%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7']  # 网页链接


def save_links(file, link):
    """保存链接。

    :param file: 字符串：文件路径。
    :param link: 字符串：需要保存的链接。
    :return: 0。
    """
    print('Saving links to files...')
    with open(file, 'a', encoding='utf-8') as file:
        file.write(link + '\n')
        file.close()


def remove_repetitive_links(links_stored_file):
    """移除链接存储文件中重复的链接。

    :param links_stored_file: 字符串：文件路径。
    :return: 0。
    """
    print('Removing repetitive links...')
    links = []
    for link in open(links_stored_file):
        if link in links:
            print('Reprtitive link: ' + link.strip() + '。')
            continue
        links.append(link)
    with open(links_stored_file, 'w') as file:
        file.writelines(links)
        file.close()


def get_shared_links(source):
    """获取分享链接。

    :param: source: 字符串：链接的来源（一般为网页链接）。
    :return: 0。
    """
    headers = {'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.36'}
    req = request.Request(source, headers=headers)
    resp = request.urlopen(req)
    soup = BeautifulSoup(resp, 'html.parser')
    for p in soup.find_all('p', string=re.compile('ss://|ssr://|vmess://|vless://')):
        link = p.get_text().strip()
        print('Acquired link: ' + link + ' .')
        save_links('./shared_links.txt', link)


def get_profile_link(links_stored_file, profile_name):
    """获取生成配置文件的链接。

    :param links_stored_file: 字符串：存储链接的文件的路径。
    :param profile_name: 字符串：生成配置的文件名。
    :return: 配置文件的链接。
    """
    url = ''
    for link in open(links_stored_file):
        url = url + '|' + link.strip()
    base_url = 'http://127.0.0.1:25500/sub?'
    params = {
        'target': 'clash',
        'url': url,
        'filename': profile_name
    }
    profile_link = base_url + urlencode(params)
    print('Gennerating SubConverter link: ' + profile_link + ' .')
    return profile_link


def run_get_profile():
    """运行获取配置文件线程

    :return: 0。
    """
    for url in urls:
        get_shared_links(url)
        time.sleep(3)
    remove_repetitive_links('./shared_links.txt')
    subconverter_link = get_profile_link('./shared_links.txt', 'Public from V9999')
    urlretrieve(subconverter_link, '../Profiles/Public from V9999.yml')
    print('Profiles update complete!')
    sys.exit()


def run_subconverter():
    """运行 SubConverter 线程。

    :return: 0。
    """
    process = subprocess.run(['powershell', './subconverter/subconverter.exe'])


def main():
    """从此处开始运行。

    :return: 0。
    """
    subconverter = Thread(target=run_subconverter, daemon=True)
    profile_getter = Thread(target=run_get_profile, daemon=True)
    subconverter.start()
    profile_getter.start()
    profile_getter.join()


if __name__ == '__main__':
    main()
