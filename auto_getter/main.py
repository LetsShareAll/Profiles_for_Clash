#!/usr/bin/python3

import os
import re
import subprocess
import sys
from threading import Thread
from time import sleep
from urllib.parse import urlencode
from urllib.request import urlretrieve, Request, urlopen

import yaml
from bs4 import BeautifulSoup

config_file = 'config.yml'


def load_yaml_data(yaml_file, not_supported_tags):
    """读取 YAML 类型文件数据。

    :param yaml_file: 字符串：YAML 文件路径。
    :param not_supported_tags: 列表：不受支持的 YAML 标签。
    :return: 字典：YAML 文件数据。
    """
    with open(yaml_file, 'r', encoding='utf-8') as data_file:
        content = data_file.read()
    content = rm_yaml_tags(content, not_supported_tags)
    yaml_data = yaml.load(content, Loader=yaml.FullLoader)
    return yaml_data


def save_yaml_file(dict_content, yaml_file_path):
    """保存字典至 YAML 文件

    :param dict_content: 字典：要保存的字典内容。
    :param yaml_file_path: 字符串：要保存的文件。
    :return: 0。
    """
    yaml_file = open(yaml_file_path, 'w')
    yaml_file.write(yaml.dump(dict_content))
    yaml_file.close()


def rm_yaml_tags(content, tags):
    """移除 YAML 标签。

    :param content: 字符串：YAML 文件内容。
    :param tags: 列表：YAML 标签。
    :return: 字符串：处理后的 YAML 文件内容。
    """
    for tag in tags:
        print('Removing tag "' + tag + '"...')
        content = content.replace('!<' + tag + '>', '')
    return content


def rm_proxies_with_ciphers(proxies, ciphers):
    """移除含有特定加密方式的代理。

    :param proxies: 列表：需处理的代理。
    :param ciphers: 列表：需移除的加密方式。
    :return: 列表：移除加密方式后的代理。
    """
    print('Removing proxies with "{ciphers}"...'.format(ciphers=ciphers))
    for proxy in proxies:
        index = proxies.index(proxy)
        for cipher in ciphers:
            if proxy['cipher'] == cipher:
                print('Found a proxy "No.{index}: {server}:{port}" has cipher: "{cipher}".'.format(
                    index=index, server=proxy['server'], port=proxy['port'], cipher=cipher))
                print('Now removing it...')
                del proxies[index]
    return proxies


def rm_outdated_proxies(proxies):
    """移除过时代理。

    :param proxies: 列表：需处理的代理。
    :return: 列表：移除过时代理后的代理。
    """
    proxies_servers = []
    for proxy in proxies:
        checking_index = proxies.index(proxy)
        print('Checking No.{index}: "{server}:{port}"...'.format(index=checking_index + 1, server=proxy['server'],
                                                                 port=proxy['port']))
        for proxy_server in proxies_servers:
            if determine_dict_in_another({'server': proxy['server'], 'port': proxy['port']}, proxy_server):
                existed_index = proxy_server['checking_index']
                print('Found a outdated proxy: No.{index}: "{server}:{port}".'.format(
                    index=existed_index + 1, server=proxy['server'], port=proxy['port']))
                print('Now replacing it with the latest one...')
                proxies[existed_index] = proxies[checking_index]
                del proxies[checking_index]
        proxies_servers.append({'checking_index': checking_index, 'server': proxy['server'], 'port': proxy['port']})
    return proxies


def rm_dir_files(directory):
    """删除文件夹内部所有文件。

    :param directory: 字符串：要删除内部文件的文件夹。
    :return: 0。
    """
    print('Removing directory "' + directory + '"...')
    if os.path.exists(directory):
        for root, dirs, files in os.walk(directory, topdown=False):
            for name in files:
                print('Removing file "' + name + '"...')
                os.remove(os.path.join(root, name))
            for name in dirs:
                print('Removing directory ' + name + '...')
                os.rmdir(os.path.join(root, name))
    else:
        print('The directory "' + directory + '" dos not exits!')


def mkdir(directory):
    """创建文件夹。

    :param directory: 字符串：文件夹路径。
    :return: 0。
    """
    folder = os.path.exists(directory)
    print('Creating directory "' + directory + '"...')
    if not folder:
        os.makedirs(directory)
        print('The directory "' + directory + '" successfully created!')
    else:
        print('The directory "' + directory + '" exits!')


def save_links(file, link):
    """保存链接。

    :param file: 字符串：文件路径。
    :param link: 字符串：需要保存的链接。
    :return: 0。
    """
    print('Saving link to file...')
    with open(file, 'a', encoding='utf-8') as file:
        file.write(link + '\n')
        file.close()


def remove_repetitive_links(shared_links_stored_file):
    """移除链接存储文件中重复的链接。

    :param shared_links_stored_file: 字符串：文件路径。
    :return: 0。
    """
    print('Removing repetitive links...')
    if os.path.exists(shared_links_stored_file):
        links = []
        for link in open(shared_links_stored_file, encoding='utf-8'):
            if link in links:
                print('Repetitive link: "' + link.strip() + '".')
                continue
            links.append(link)
        with open(shared_links_stored_file, 'w', encoding='utf-8') as links_file:
            links_file.writelines(links)
            links_file.close()
    else:
        print('Removing repetitive links failed! No such file: "' + shared_links_stored_file + '".')


def get_shared_links_from_element(page, tag, tag_class, shared_links_store_file, shared_link_begin_with):
    """从网页元素中获取链接。

    :param page: 字符串：网页链接。
    :param tag: 字符串：网页元素标签。
    :param tag_class: 字符串：网页元素所属类。
    :param shared_links_store_file: 字符串：存储链接的文件。
    :param shared_link_begin_with: 字符串：链接开头。
    :return: 0。
    """
    print('Getting links from tag="' + tag + '" and class="' + tag_class + '"...')
    soup = BeautifulSoup(page, 'html.parser')
    for tag in soup.find_all(tag, class_=tag_class, string=re.compile(shared_link_begin_with)):
        link = tag.get_text().strip()
        print('Acquired link: "' + link + '".')
        save_links(shared_links_store_file, link)


def get_shared_links_from_tg_channels(tg_channel_name, shared_links_store_file, shared_link_begin_with):
    """从电报频道获取链接。

    :param tg_channel_name: 字符串：电报频道名。
    :param shared_links_store_file: 字符串：分享链接的存储文件。
    :param shared_link_begin_with: 字符串：分享链接的开头。
    :return: 0。
    """
    tg_channel_pre_page = 'https://t.me/s/' + tg_channel_name
    headers = {'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.36'}
    req = Request(tg_channel_pre_page, headers=headers)
    resp = urlopen(req)
    soup = BeautifulSoup(resp, 'html.parser')
    # 将 br 标签替换为 \n
    message_html_str = str(soup.select('div', class_='tgme_widget_message_text')
                           ).replace('<br>', '\n').replace('<br/>', '\n').replace('<br />', '\n')
    get_shared_links_from_element(message_html_str, 'div', 'tgme_widget_message_text', shared_links_store_file,
                                  shared_link_begin_with)


def get_shared_links_from_files(remote_file, temp_file, shared_links_store_file, shared_link_begin_with):
    """从文件行获取链接。

    :param remote_file: 字符串：远程文件链接。
    :param temp_file: 字符串：临时文件存放路径。
    :param shared_links_store_file: 字符串：链接存储文件。
    :param shared_link_begin_with: 字符串：链接开头。
    :return: 0。
    """
    print('Getting links from "' + remote_file + '"...')
    if remote_file != '':
        urlretrieve(remote_file, temp_file)
        with open(temp_file, 'r', encoding='utf-8') as search_file:
            for line in search_file:
                link_list = re.compile(shared_link_begin_with).findall(line)
                if len(link_list) > 0:
                    link = link_list[0]
                    print('Acquired link: "' + link + '".')
                    save_links(shared_links_store_file, link)
    else:
        print('Remote file is null!')


def get_shared_links_from_pages(source, shared_links_store_file, shared_link_begin_with):
    """从网页链接获取链接。

    :param: source: 字符串：链接的来源（一般为网页链接）。
    :param: shared_links_store_file: 字符串：存储链接的文件位置。
    :param: shared_link_begin_with: 字符串：链接开头。
    :return: 0。
    """
    print('Getting links from "' + source + '"...')
    if source != '':
        headers = {'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.36'}
        req = Request(source, headers=headers)
        resp = urlopen(req)
        get_shared_links_from_element(resp, 'p', '', shared_links_store_file, shared_link_begin_with)
    else:
        print('Source is null!')


def get_profile_link(parameters, shared_links_stored_file):
    """获取生成配置文件的链接。

    :param parameters: 字典：用于 Sub Converter 的参数。
    :param shared_links_stored_file: 字符串：存储链接的文件的路径。
    :return: 配置文件的链接。
    """
    if os.path.exists(shared_links_stored_file):
        url = ''
        for link in open(shared_links_stored_file, encoding='utf-8'):
            url = url + '|' + link.strip()
        parameters['url'] = url
        base_url = 'http://127.0.0.1:25500/sub?'
        profile_link = base_url + urlencode(parameters)
        print('Generating Sub_Converter link: "' + profile_link + '".')
        return profile_link
    else:
        print('Profile get failed! No such file: "' + shared_links_stored_file + '".')
        return ''


def get_profile(config_path):
    """获取配置。

    :param config_path: 字符串：运行时的配置文件。
    :return: 0。
    """
    # 读取配置数据。
    config_path = './' + config_file
    config = load_yaml_data(config_path, [])
    # 读取其他设置。
    others_config = config['others']
    directories_config = others_config['directories']
    shared_links_stored_dir = directories_config['shared-links-stored-dir']
    profiles_stored_dir = directories_config['profiles-stored-dir']
    temp_file_stored_dir = directories_config['temp-file-stored-dir']
    supported_shared_link_begin_with = others_config['supported-shared-link-begin-with']
    supported_subscribe_link_begin_with = others_config['supported-subscribe-link-begin-with']
    not_supported_yaml_tags = others_config['not-supported-yaml-tags']
    # 获取 Sub Converter 设置。
    sub_converter_config = config['sub-converter']
    # 获取配置文件设置。
    profile_config = config['profile']
    profile_clash_config = profile_config['clash']
    clash_not_supported_ciphers = profile_clash_config['not-supported-ciphers']

    # 创建文件夹并删除过时链接文件。
    for directory in directories_config:
        mkdir(directories_config[directory])
        rm_dir_files(directories_config[directory])

    # 根据设置的 Profile 生成配置。
    for profile in config['profiles-source']:
        # 获取 Profile 信息。
        profile_name = profile['name']
        shared_links_stored_file_path = shared_links_stored_dir + '/' + profile_name + '.txt'
        profile_path = profiles_stored_dir + '/' + profile_name + '.yml'
        temp_file_path = temp_file_stored_dir + '/' + profile_name + '.txt'

        # 生成配置文件。
        print('Getting profile for ' + profile_name + '...')
        for source_type in profile['sources']:
            # 防止配置中该来源类型数值为空。
            if len(profile['sources'][source_type]) > 0:
                print('Source type: ' + source_type + '.')

                # 遍历该来源类型下所有的来源。
                for i in range(0, len(profile['sources'][source_type])):
                    # 获取来源。
                    source = profile['sources'][source_type][i]

                    # 根据来源类型选择相应方法。
                    if source_type == 'pages':
                        get_shared_links_from_pages(source, shared_links_stored_file_path,
                                                    supported_shared_link_begin_with)
                    elif source_type == 'tg-channels':
                        if source != '':
                            get_shared_links_from_tg_channels(source, shared_links_stored_file_path,
                                                              supported_shared_link_begin_with)
                        else:
                            print('Telegram channel is null!')
                    elif source_type == 'files':
                        get_shared_links_from_files(source, temp_file_path, shared_links_stored_file_path,
                                                    supported_shared_link_begin_with)
                    else:
                        print('Don`t support the source type named "' + source_type + '" now!')
                    sleep(3)
            else:
                print(source_type + ' in "' + profile_name + '" is NULL!')

        remove_repetitive_links(shared_links_stored_file_path)

        # 下载配置。
        sub_converter_link = get_profile_link(sub_converter_config, shared_links_stored_file_path)
        if sub_converter_link != '':
            urlretrieve(sub_converter_link, profile_path)
            print('Profile "' + profile_name + '" update complete!')
        else:
            print('Profile "' + profile_name + '" update failed!')

        # 对下载的配置文件进行操作。
        profile_data = load_yaml_data(profile, not_supported_yaml_tags)
        proxies = profile_data['proxies']
        proxies = rm_proxies_with_ciphers(proxies, clash_not_supported_ciphers)
        proxies = rm_outdated_proxies(proxies)
        profile_data['proxies'] = proxies
        save_yaml_file(profile_data, profile)


def run_get_profile():
    """运行获取配置文件线程

    :return: 0。
    """
    get_profile(config_file)
    sys.exit()


def run_sub_converter():
    """运行 Sub Converter 线程。

    :return: 0。
    """
    system_platform = sys.platform
    print('Your system platform is "' + system_platform + '".')
    if system_platform == 'linux':
        process = subprocess.run(args='./subconverter/linux32/subconverter')
    elif system_platform == 'win32':
        process = subprocess.run(['powershell', './subconverter/win32/subconverter.exe'])
    elif system_platform == 'darwin':
        process = subprocess.run(args='./subconverter/darwin64/GNUSparseFile.0/subconverter')
    else:
        print('The platform "' + system_platform + '" does not support now!')


def main():
    """从此处开始运行。

    :return: 0。
    """
    sub_converter = Thread(target=run_sub_converter, daemon=True)
    profile_getter = Thread(target=run_get_profile, daemon=True)
    sub_converter.start()
    profile_getter.start()
    profile_getter.join()


if __name__ == '__main__':
    main()
