#!/usr/bin/python3
import datetime
import json
import os
import re
import subprocess
import sys
from threading import Thread
from time import sleep
from urllib.parse import urlencode
from urllib.request import urlretrieve, Request, urlopen

import emoji
import yaml
from bs4 import BeautifulSoup
from googletrans import Translator

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


def translate(content, src_lang, dest_lang):
    """翻译文本。

    :param content: 字符串：要翻译的文本。
    :param src_lang: 字符串：源语言类型。
    :param dest_lang: 字符串：目标语言类型。
    :return: 字符串：翻译后的文本。
    """
    translator = Translator(service_urls=['translate.google.com', 'translate.google.cn'])
    trans = translator.translate(text=content, src=src_lang, dest=dest_lang)
    return trans.text


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


def determine_dict_in_another(dict_included, dict_including):
    """判断一部字典是否包含另一部字典。

    :param dict_included: 字典：被包含的字典。
    :param dict_including: 字典：包含另一部字典的字典。
    :return: 布尔：是否包含字典。
    """
    dict_included_set = set(dict_included.items())
    dict_including_set = set(dict_including.items())
    return dict_included_set.issubset(dict_including_set)


def rm_proxies_with_ciphers(profile_data, ciphers):
    """移除含有特定加密方式的代理。

    :param profile_data: 字典：需处理的代理文件数据。
    :param ciphers: 列表：需移除的加密方式。
    :return: 字典：移除加密方式后的代理文件数据。
    """
    print('Removing proxies with "{ciphers}"...'.format(ciphers=ciphers))
    proxies = profile_data['proxies']
    proxy_groups = profile_data['proxy-groups']
    proxy_index = 0
    while proxy_index < len(proxies):
        proxy = proxies[proxy_index]
        if 'cipher' in proxy:
            for cipher in ciphers:
                if proxy['cipher'] == cipher:
                    print('Found a proxy "No.{index}: {server}:{port}" named "{name}" has cipher: "{cipher}".'.format(
                        index=proxy_index + 1, server=proxy['server'], port=proxy['port'], name=proxy['name'],
                        cipher=cipher))
                    print('Now removing it...')
                    proxy_groups = rm_proxy_groups_proxies(proxy_groups, proxy['name'])
                    del proxies[proxy_index]
                    # 删除列表中元素后，下一元素序号会减一，因此为了不会跳过这一元素，遍历序号也应减一。
                    proxy_index -= 1
                else:
                    print('The proxy "No.{index}: {server}:{port}" named "{name}" has no cipher: "{cipher}".'.format(
                        index=proxy_index + 1, server=proxy['server'], port=proxy['port'], name=proxy['name'],
                        cipher=cipher))
        else:
            print('The proxy "No.{index}: {server}:{port}" named "{name}" has no param cipher.'.format(
                index=proxy_index + 1, server=proxy['server'], name=proxy['name'], port=proxy['port']))
        proxy_index += 1
    profile_data['proxy-groups'] = proxy_groups
    profile_data['proxies'] = proxies
    return profile_data


def rm_proxy_groups_proxies(proxy_groups, proxy_name):
    """移除代理组中的代理。

    :param proxy_groups: 列表：需移除代理的代理组。
    :param proxy_name: 字符串：移除代理依据的代理名。
    :return: 列表：移除代理后的代理组。
    """
    for proxy_group in proxy_groups:
        proxy_group_index = proxy_groups.index(proxy_group)
        for proxy_group_proxy in proxy_group['proxies']:
            proxy_group_proxy_index = proxy_group['proxies'].index(proxy_group_proxy)
            if proxy_group_proxy == proxy_name:
                del proxy_groups[proxy_group_index]['proxies'][proxy_group_proxy_index]
    return proxy_groups


def correct_clash_mode(profile_data, correct_mode_data):
    """更正 Clash 配置文件中的“mode”参数。

    :param profile_data: 字典：需处理的代理文件数据。
    :param correct_mode_data: 列表：需要更正的模式数据。
    :return: 字典：移除加密方式后的代理文件数据。
    """
    print('Correcting clash mode...')
    proxies = profile_data['proxies']
    correct_modes = correct_mode_data
    for proxy in proxies:
        for correct_mode in correct_modes:
            if 'plugin' in proxy and proxy.plugin == correct_mode.plugin and proxy.mode == correct_mode.match:
                proxy.mode = correct_mode.mode
    profile_data['proxies'] = proxies
    return profile_data


def rm_outdated_proxies(profile_data):
    """移除过时代理。

    :param profile_data: 字典：需处理的代理配置文件数据。
    :return: 字典：移除过时代理后的代理配置文件数据。
    """
    print('Removing outdated proxies...')
    proxies = profile_data['proxies']
    proxy_groups = profile_data['proxy-groups']
    proxies_servers = []
    checking_index = 0
    while checking_index < len(proxies):
        proxy = proxies[checking_index]
        print('Checking No.{index}: "{server}:{port}"...'.format(index=checking_index + 1, server=proxy['server'],
                                                                 port=proxy['port']))
        for proxy_server in proxies_servers:
            if determine_dict_in_another({'server': proxy['server'], 'port': proxy['port']}, proxy_server):
                existed_index = proxy_server['checking_index']
                print('Found a outdated proxy: No.{index}: "{server}:{port}".'.format(
                    index=existed_index + 1, server=proxy['server'], port=proxy['port']))
                print('Now replacing it with the latest one...')
                proxy_groups = rm_proxy_groups_proxies(proxy_groups, proxies[existed_index]['name'])
                profile_data['proxy-groups'] = proxy_groups
                del proxies[existed_index]
                profile_data['proxies'] = proxies
                # 删除列表中元素后，下一元素序号会减一，因此为了不会跳过这一元素，遍历序号也应减一。
                checking_index -= 1
        proxies_servers.append({'checking_index': checking_index, 'server': proxy['server'], 'port': proxy['port']})
        checking_index += 1
    print('Outdated proxies has been successfully removed!')
    return profile_data


def rename_proxies(profile_data):
    """对代理进行重命名。

    :param profile_data: 字典：需处理的代理文件数据。
    :return: 字典：重命名后的代理配置文件数据。
    """
    print('Renaming proxies...')
    proxies = profile_data['proxies']
    proxy_groups = profile_data['proxy-groups']
    proxy_index = 0
    while proxy_index < len(proxies):
        proxy = proxies[proxy_index]
        # 使用 http://ip-api.com 的 API 进行服务器信息查询。
        print('Getting No.{index}: "{server}" information...'.format(index=proxy_index, server=proxy['server']))
        ip_api_link = 'http://ip-api.com/json/' + proxy['server']
        req = Request(url=ip_api_link)
        resp = urlopen(req)
        resp_data = resp.read()
        encoding = resp.info().get_content_charset('utf-8')
        ip_info = json.loads(resp_data.decode(encoding))
        # 此时可判断域名是否存在。
        if 'country' not in ip_info:
            print('No such server: "{server}.'.format(server=proxy['server']))
            print('Now removing it...')
            proxy_groups = rm_proxy_groups_proxies(proxy_groups, proxies[proxy_index]['name'])
            del proxies[proxy_index]
            # 删除列表中元素后，下一元素序号会减一，因此为了不会跳过这一元素，遍历序号也应减一。
            proxy_index -= 1
            continue
        # 根据获取的信息更改代理名。
        country = ip_info.get('country')
        city = ip_info.get('city')
        flag = emoji.emojize(':' + country + ':')
        if country == 'Hong Kong' or country == 'Taiwan' or country == 'Macao':
            city = country
            country = 'China'
            flag = emoji.emojize(':' + country + ': :' + city + ':')
        if country == city:
            position = country
        else:
            position = country + ' ' + city
        # position = translate(position, 'en', 'zh-cn')
        # name = '{flag} {position} {index:0>3}'.format(flag=flag, position=position, index=proxy_index)
        name = '{position} {index:0>3}'.format(position=position, index=proxy_index)
        print(f'The server name is {name}.'.format(name=name))
        # 代理组中的代理名同步重命名。
        for proxy_group in proxy_groups:
            proxy_group_index = proxy_groups.index(proxy_group)
            for proxy_group_proxy in proxy_group['proxies']:
                proxy_group_proxy_index = proxy_group['proxies'].index(proxy_group_proxy)
                if proxy_group_proxy == proxy['name']:
                    proxy_groups[proxy_group_index]['proxies'][proxy_group_proxy_index] = name
        proxies[proxy_index]['name'] = name
        profile_data['proxies'] = proxies
        profile_data['proxy-groups'] = proxy_groups
        sleep(3)
        if proxy_index % 3 == 0:
            print('Sleeping for 5 seconds...')
            sleep(5)
        proxy_index += 1
    print('Proxies has been successfully renamed!')
    return profile_data


def sort_dict_list(dict_list, dict_keys):
    """对字典列表进行排序。

    :param dict_list: 列表：要排序的字典列表。
    :param dict_keys: 列表：排序依据的字典关键字。
    :return: 列表：排序后的字典列表。
    """
    print('Sorting dictionary...')
    for dict_key in dict_keys:
        dict_list = sorted(dict_list, key=lambda value: (value.__getitem__(dict_key)))
    print('Dictionary has been successfully sorted!')
    return dict_list


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
        print('The directory: "' + directory + '" has been successfully removed!')
    else:
        print('The directory "' + directory + '" dos not exits!')


def get_date(date_format):
    """根据格式获取当前时间。

    :param date_format: 字符串：时间格式。
    :return: 字符串：当前时间。
    """
    date = datetime.datetime.now().strftime(date_format)
    print(date)
    return date


def handle_link(link):
    """处理链接。

    :param link: 字符串：需处理的字符串。
    :return: 字符串：处理后的字符串。
    """
    print("Handle link...")
    patterns = re.findall(r"[$][(](.*?)[)]", link)
    if len(patterns) > 0:
        for pattern in patterns:
            print(pattern)
            keywords = re.findall(r"(.*?)[{]", pattern)
            for keyword in keywords:
                print(keyword)
                if keyword == 'date':
                    return str.replace(link, '$('+pattern+')', get_date(re.findall(r"[{](.*?)[}]", pattern)[0]))
                else: return link
    else: return link


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
    print('The link has been successfully saved!')


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
        print('The repetitive links has been successfully removed!')
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
    print('The links from tag="{tag}" and class="{tag_class}" has been successfully got!'.format(tag=tag,
                                                                                                 tag_class=tag_class))


def get_shared_links_from_tg_channels(tg_channel_name, shared_links_store_file, shared_link_begin_with):
    """从电报频道获取链接。

    :param tg_channel_name: 字符串：电报频道名。
    :param shared_links_store_file: 字符串：分享链接的存储文件。
    :param shared_link_begin_with: 字符串：分享链接的开头。
    :return: 0。
    """
    print('Getting links from telegram channel: "' + tg_channel_name + '"...')
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
    print('The links from telegram channel: "' + tg_channel_name + '" has been successfully got!')


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
        print('The links from "' + remote_file + '" has been successfully got!')
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
        print('The links from "' + source + '" has been successfully got!')
    else:
        print('Source is null!')


def get_shared_links_from_subscribe_links(subscribe_link, shared_links_store_file):
    """从订阅链接获取链接。

    :param: subscribe_link: 字符串：订阅链接。
    :param: shared_links_store_file: 字符串：存储链接的文件位置。
    :return: 0。
    """
    print('Getting links from "' + subscribe_link + '"...')
    subscribe_link = handle_link(subscribe_link)
    save_links(shared_links_store_file, subscribe_link)


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
    correct_plugin_opts_mode = profile_clash_config['correct-plugin-opts-mode']

    # 创建文件夹并删除过时链接文件。
    for directory in directories_config:
        mkdir(directories_config[directory])
        rm_dir_files(directories_config[directory])

    # 根据设置的 Profile 生成配置。
    for profile in config['profiles-sources']:
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
                                                    supported_shared_link_begin_with + "|" + supported_subscribe_link_begin_with)
                    elif source_type == 'subscribe-links':
                        get_shared_links_from_subscribe_links(source, shared_links_stored_file_path)
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
            print('Profile "' + profile_name + '" download complete!')
            # 对下载的配置文件进行操作。
            profile_data = load_yaml_data(profile_path, not_supported_yaml_tags)
            profile_data = rm_proxies_with_ciphers(profile_data, clash_not_supported_ciphers)
            profile_data = rm_outdated_proxies(profile_data)
            profile_data = correct_clash_mode(profile_data, correct_plugin_opts_mode)
            profile_data = rename_proxies(profile_data)
            proxies = profile_data['proxies']
            proxy_groups = profile_data['proxy-groups']
            proxies = sort_dict_list(proxies, ['name'])
            for proxy_group in proxy_groups:
                proxy_group_index = proxy_groups.index(proxy_group)
                proxy_group['proxies'].sort()
                proxy_groups[proxy_group_index] = proxy_group
            profile_data['proxies'] = proxies
            profile_data['proxy-groups'] = proxy_groups
            save_yaml_file(profile_data, profile_path)
            print('Profile "' + profile_name + '" update complete!')
        else:
            print('Profile "' + profile_name + '" update failed!')


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
        process = subprocess.run(args='./subconverter/linux64/subconverter')
    elif system_platform == 'win32':
        process = subprocess.run(['powershell', './subconverter/win64/subconverter.exe'])
    elif system_platform == 'darwin':
        process = subprocess.run(args='./subconverter/darwin64/subconverter')
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
