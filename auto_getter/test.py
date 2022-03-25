import json
from time import sleep
from urllib.request import urlopen

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


def determine_dict_in_another(dict_included, dict_including):
    """判断一部字典是否包含另一部字典。

    :param dict_included: 字典：被包含的字典。
    :param dict_including: 字典：包含另一部字典的字典。
    :return: 布尔：是否包含字典。
    """
    dict_a_set = set(dict_included.items())
    dict_b_set = set(dict_including.items())
    return dict_a_set.issubset(dict_b_set)


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


def rename_proxies(proxies):
    """对代理进行重命名。

    :param proxies: 列表：需处理的代理。
    :return: 列表：重命名后的代理。
    """
    print('Renaming proxies...')
    for proxy in proxies:
        index = proxies.index(proxy)
        # 使用 http://ip-api.com 的 API 进行 IP 信息查询。
        ip_api_link = 'http://ip-api.com/json/' + proxy['server']
        resp = urlopen(ip_api_link)
        resp_data = resp.read()
        encoding = resp.info().get_content_charset('utf-8')
        ip_info = json.loads(resp_data.decode(encoding))
        # 此时可判断域名是否存在。
        if 'country' not in ip_info:
            print('No such server: "{server}.'.format(server=proxy['server']))
            print('Now removing it...')
            del proxies[index]
            continue
        country = ip_info.get('country')
        city = ip_info.get('city')
        flag = emoji.emojize(':' + country + ':')
        position = country + ' ' + city
        # position = translate(position, 'en', 'zh-cn')
        name = '{flag} {position} {index}'.format(flag=flag, position=position, index=index)
        proxies[index]['name'] = name
        sleep(3)
    return proxies


def main():
    config_path = './' + config_file
    config = load_yaml_data(config_path, [])
    others_config = config['others']
    directories_config = others_config['directories']
    not_supported_yaml_tags = others_config['not-supported-yaml-tags']
    profiles_stored_dir = directories_config['profiles-stored-dir']
    profile_path = profiles_stored_dir + '/Public from FQD.yml'
    profile_config = config['profile']
    profile_clash_config = profile_config['clash']
    clash_not_supported_ciphers = profile_clash_config['not-supported-ciphers']
    profile_data = load_yaml_data(profile_path, not_supported_yaml_tags)
    proxies = profile_data['proxies']
    proxies = rm_proxies_with_ciphers(proxies, clash_not_supported_ciphers)
    proxies = rm_outdated_proxies(proxies)
    proxies = rename_proxies(proxies)
    proxies = sort_dict_list(proxies, ['name'])
    profile_data['proxies'] = proxies
    save_yaml_file(profile_data, profile_path)


if __name__ == '__main__':
    main()
