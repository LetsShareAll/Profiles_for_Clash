# [Profiles_for_Clash](https://github.com/Shuery-Shuai/Profiles_for_Clash "Shuery-Shuai/Profiles_for_Clash: Profiles can be used in Clash for Windows, Clash for Android and so on.")

使用 Python 自动获取一些可用于 _Clash for Windows_、_Clash for Android_ 等应用的配置文件。

> **警告**：通过使用特殊方式访问外网时请**严格遵守当地法律法规**，**禁止借此进行传播“黄、赌、毒”等违法犯罪活动**。节点均来自网络收集，由网友免费提供，请**勿使用节点进行 BT 下载**。

## 配置说明

### 配置项解释

#### Profiles 配置

Clash 配置文件的有关设置。

`profiles`：

|  参数   |   子参数    |                         示例值                          | 解释                                  | 备注             |
| :-----: | :---------: | :-----------------------------------------------------: | :------------------------------------ | :--------------- |
|  name   |     ——      |                    `'Profiles Name'`                    | 生成的配置文件的名称。                | ——               |
| sources |      ↓      |                           ——                            | 配置文件的来源。                      | ——               |
|   ——    |    pages    |                 `'/path/to/page.html'`                  | 来自网页。                            | ——               |
|   ——    | tg-channels |                 `'TelegramChannelName'`                 | 来自电报频道。                        | 正在努力适配中…… |
|   ——    |    files    |                    `'/path/to/file'`                    | 来自订阅。                            | 正在努力适配中…… |
|   ——    | subscribes  | `- type: 'subscribe-type'` `link: '/path/to/subscribe'` | `type`：订阅类型。 `link`：订阅链接。 | 正在努力适配中…… |

#### Sub Converter 配置

Sub Converter 设置。详见 [Sub Converter 文档](https://github.com/tindy2013/subconverter/blob/master/README-cn.md "subconverter/README-cn.md at master · tindy2013/subconverter")。

`sub-converter`：

|     参数     | 子参数 |  默认值   | 解释                                                                                                          | 备注                                                                                                                                                                                                    |
| :----------: | :----: | :-------: | :------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
|    target    |   ——   | `'clash'` | 想要生成的配置类型。                                                                                          | 详见 [Sub Converter 支持类型](https://github.com/tindy2013/subconverter/blob/master/README-cn.md#%E6%94%AF%E6%8C%81%E7%B1%BB%E5%9E%8B "subconverter/README-cn.md at master · tindy2013/subconverter")。 |
|    config    |   ——   |   `''`    | 外部配置的地址 (包含分组和规则部分)，当此参数不存在时使用程序的主程序目录中的配置文件，参考的链接见下方表格。 | 详见 [Sub Converter 外部配置](https://github.com/tindy2013/subconverter/blob/master/README-cn.md#%E5%A4%96%E9%83%A8%E9%85%8D%E7%BD%AE "subconverter/README-cn.md at master · tindy2013/subconverter")。 |
|    emoji     |   ——   | `'true'`  | 用于设置节点名称是否包含 Emoji。                                                                              | 对于 Emoji 的设置请勿随意更改，日后可能会使用其他方法更改节点名称！                                                                                                                                     |
|  add_emoji   |   ——   | `'false'` | 用于在节点名称前加入 Emoji。                                                                                  | 对于 Emoji 的设置请勿随意更改，日后可能会使用其他方法更改节点名称！                                                                                                                                     |
| remove_emoji |   ——   | `'true'`  | 用于设置是否删除节点名称中原有的 Emoji。                                                                      | 对于 Emoji 的设置请勿随意更改，日后可能会使用其他方法更改节点名称！                                                                                                                                     |

`config`：

|   配置名称   |                    配置描述                    |                                                    配置链接                                                    |
| :----------: | :--------------------------------------------: | :------------------------------------------------------------------------------------------------------------: |
| no-url-test  |                   Universal                    |  <https://cdn.jsdelivr.net/gh/SleepyHeeead/subconverter-config@master/remote-config/universal/no-urltest.ini>  |
|   url-test   |                   Universal                    |   <https://cdn.jsdelivr.net/gh/SleepyHeeead/subconverter-config@master/remote-config/universal/urltest.ini>    |
|    maying    |                   Customized                   |   <https://cdn.jsdelivr.net/gh/SleepyHeeead/subconverter-config@master/remote-config/customized/maying.ini>    |
|    y-too     |                   Customized                   |    <https://cdn.jsdelivr.net/gh/SleepyHeeead/subconverter-config@master/remote-config/customized/ytoo.ini>     |
| flower-cloud |                   Customized                   | <https://cdn.jsdelivr.net/gh/SleepyHeeead/subconverter-config@master/remote-config/customized/flowercloud.ini> |
|   nyan-cat   |                   Customized                   |   <https://cdn.jsdelivr.net/gh/SleepyHeeead/subconverter-config@master/remote-config/customized/nyancat.ini>   |
|  nexitally   |                   Customized                   |  <https://cdn.jsdelivr.net/gh/SleepyHeeead/subconverter-config@master/remote-config/customized/nexitally.ini>  |
|   so-cloud   |                   Customized                   |   <https://cdn.jsdelivr.net/gh/SleepyHeeead/subconverter-config@master/remote-config/customized/socloud.ini>   |
|     ark      |                   Customized                   |     <https://cdn.jsdelivr.net/gh/SleepyHeeead/subconverter-config@master/remote-config/customized/ark.ini>     |
|  ssr-cloud   |                   Customized                   |  <https://cdn.jsdelivr.net/gh/SleepyHeeead/subconverter-config@master/remote-config/customized/ssrcloud.ini>   |
|   net-ease   | Special：网易云音乐解锁。仅规则，No-URL-Test。 |    <https://cdn.jsdelivr.net/gh/SleepyHeeead/subconverter-config@master/remote-config/special/netease.ini>     |
|    basic     |         Special：仅 GEOIP CN + Final。         |     <https://cdn.jsdelivr.net/gh/SleepyHeeead/subconverter-config@master/remote-config/special/basic.ini>      |

> **提示**：更多配置可前往 [Sub Converter Config](https://github.com/SleepyHeeead/subconverter-config "SleepyHeeead/subconverter-config") 查看。

#### Others 配置

其他设置。

`others`：

|                参数                 |       子参数        |                           默认值                           | 解释                       | 备注         |
| :---------------------------------: | :-----------------: | :--------------------------------------------------------: | :------------------------- | :----------- |
|             directories             |          ↓          |                             ——                             | 关于文件夹的设置。         | ——           |
|                 ——                  |   links-store-dir   |                        `'./links'`                         | 保存链接文件的文件夹位置。 | ——           |
|                 ——                  | profiles-store-dir  |                      `'../Profiles'`                       | 保存配置文件的文件夹位置。 | ——           |
|                 ——                  | temp-file-store-dir |                         `'./temp'`                         | 临时保存文件的文件夹位置。 | ——           |
|  supported-shared-link-begin-with   |         ——          | `'ss://.*\|ssr://.*\|vmess://.*\|vless://.*\|trojan://.*'` | 受支持的分享链接的开头。   | 正则表达式。 |
| supported-subscribe-link-begin-with |         ——          |                 `'http://.*\|https://.*'`                  | 受支持的订阅链接的开头。   | 正则表达式。 |

### 配置示例

```yaml
profiles:
  - name: "Profile Name"
    sources:
      pages:
        - "/path/to/page.html"

      tg-channels:
        - "TelegramChannelName"

      files:
        - "/path/to/file"

      subscribes:
        - type: "subscribe-type"
          link: "/path/to/subscribe"

sub-converter:
  target: "clash"
  config: ""
  emoji: "true"
  add_emoji: "false"
  remove_emoji: "true"

others:
  directories:
    links-store-dir: "./links"
    profiles-store-dir: "../Profiles"
    temp-file-store-dir: "./temp"

  supported-shared-link-begin-with: "ss://.*|ssr://.*|vmess://.*|vless://.*|trojan://.*"
  supported-subscribe-link-begin-with: "http://.*|https://*"
```

## 配置文件及其来源

“Public from V9999”来自 [Alvin9999](https://github.com/Alvin9999 "Github@Alvin9999 (自由上网)")在项目 [new-pac](https://github.com/Alvin9999/new-pac "Alvin9999/new-pac: 科学上网/自由上网/翻墙/软件/方法，一键翻墙浏览器，免费shadowsocks/ss/ssr/v2ray/goflyway账号/节点分享，vps一键搭建脚本/教程。")中的分享。

“Public from FQD”来自[翻墙党](https://fanqiangdang.com "翻墙论坛 | 翻墙党社区 - Powered by Discuz!")在群组 [SS 节点公益发放](https://t.me/ssList "Telegram@ssList")、[SSR 节点免费发放](https://t.me/ssrList "Telegram@ssrList")、[V2ray,Vmess 节点免费发放](https://t.me/V2List "Telegram@V2List")中的分享。

> **提示**：本项目所有配置均通过 [tiny2013](https://github.com/tindy2013 "Github@tindy2013 (Tindy X)") 开发的 [subconverter](https://github.com/tindy2013/subconverter "tindy2013/subconverter: Utility to convert between various subscription format.") 自动生成。
>
> **注意**：本项目配置均来自网络，若有侵权，请提出，会尽快删除。

## 配置使用教程

[点击前往](https://github.com/Shuery-Shuai/Profiles_for_Clash/wiki#%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6 "Home · Shuery-Shuai/Profiles_for_Clash Wiki")
