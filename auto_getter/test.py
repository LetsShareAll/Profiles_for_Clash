import json
from time import sleep
from urllib.request import urlopen, Request

from googletrans import Translator
import emoji as emoji
import yaml

config_file = 'config.yml'


def save_yaml_file(dict_content, yaml_file_path):
    """保存字典至 YAML 文件

    :param dict_content: 字典：要保存的字典内容。
    :param yaml_file_path: 字符串：要保存的文件。
    :return: 0。
    """
    yaml_file = open(yaml_file_path, 'w')
    yaml_file.write(yaml.dump(dict_content))
    yaml_file.close()


def sort_dict_list(dict_list, dict_keys):
    """对字典列表进行排序。

    :param dict_list: 列表：要排序的字典列表。
    :param dict_keys: 列表：排序依据的字典关键字。
    :return: 列表：排序后的字典列表。
    """
    for dict_key in dict_keys:
        dict_list = sorted(dict_list, key=lambda value: (value.__getitem__(dict_key)))
    return dict_list


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


def rm_proxy_groups_proxies(proxy_groups, proxy_name):
    """移除代理组中的代理。

    :param proxy_groups: 列表：需移除代理的代理组。
    :param proxy_name: 字符串：移除代理依据的代理名。
    :return: 列表：移除代理后的代理组。
    """
    print('Removing "' + proxy_name + '"...')
    for proxy_group in proxy_groups:
        for proxy_group_proxy in proxy_group['proxies']:
            if proxy_group_proxy == proxy_name:
                proxy_group_index = proxy_groups.index(proxy_group)
                proxy_group_proxy_index = proxy_group['proxies'].index(proxy_group_proxy)
                del proxy_groups[proxy_group_index]['proxies'][proxy_group_proxy_index]
    return proxy_groups


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


def main():
    # 读取设置。
    config_path = './' + config_file
    config = load_yaml_data(config_path, [])
    # 其他设置。
    others_config = config['others']
    directories_config = others_config['directories']
    not_supported_yaml_tags = others_config['not-supported-yaml-tags']
    # 配置设置。
    profile_config = config['profile']
    profile_clash_config = profile_config['clash']
    clash_not_supported_ciphers = profile_clash_config['not-supported-ciphers']
    # 测试设置。
    profiles_stored_dir = './test'
    profile_path = profiles_stored_dir + '/test.yml'

    # 执行操作。
    profile_data = load_yaml_data(profile_path, not_supported_yaml_tags)
    print(len(profile_data['proxies']))
    profile_data = rm_proxies_with_ciphers(profile_data, clash_not_supported_ciphers)
    print(len(profile_data['proxies']))
    # 对配置进行排序操作。
    proxies = profile_data['proxies']
    proxy_groups = profile_data['proxy-groups']
    proxies = sort_dict_list(proxies, ['name'])
    for proxy_group in proxy_groups:
        proxy_group_index = proxy_groups.index(proxy_group)
        proxy_group['proxies'].sort()
        proxy_groups[proxy_group_index] = proxy_group
    profile_data['proxies'] = proxies
    profile_data['proxy-groups'] = proxy_groups

    # 保存配置。
    save_yaml_file(profile_data, profile_path)


if __name__ == '__main__':
    main()
