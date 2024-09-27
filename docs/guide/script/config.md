# 脚本设置

## 设置项解释

### `profiles` 设置

Clash 配置文件的有关设置。

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
```

| 参数        | 示例值                                                                   | 解释                                       | 备注               |
| :---------- | :----------------------------------------------------------------------- | :----------------------------------------- | :----------------- |
| name        | `'Profile Name'`                                                         | 生成的配置文件的名称。                     | ——                 |
| sources     | ——                                                                       | 配置文件的来源。                           | ——                 |
| pages       | `'/path/to/page.html'`                                                   | 来自网页。                                 | ——                 |
| tg-channels | `'TelegramChannelName'`                                                  | 来自电报频道。                             | 目前不是特别完美。 |
| files       | `'/path/to/file'`                                                        | 来自订阅。                                 | 正在努力适配中……   |
| subscribes  | `- type: 'subscribe-type'`<br />&ensp;&ensp;`link: '/path/to/subscribe'` | `type`：订阅类型。<br />`link`：订阅链接。 | 正在努力适配中……   |

### `sub-converter` 设置

Sub Converter 设置。详见 [Sub Converter 文档](https://github.com/tindy2013/subconverter/blob/master/README-cn.md "subconverter/README-cn.md at master · tindy2013/subconverter")。

```yaml
sub-converter:
  target: "clash"
  config: ""
  emoji: "true"
  add_emoji: "false"
  remove_emoji: "true"
```

| 参数         | 默认值    | 解释                                                                                                          | 备注                                                                                                                                                                                                    |
| :----------- | :-------- | :------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| target       | `'clash'` | 想要生成的配置类型。                                                                                          | 详见 [Sub Converter 支持类型](https://github.com/tindy2013/subconverter/blob/master/README-cn.md#%E6%94%AF%E6%8C%81%E7%B1%BB%E5%9E%8B "subconverter/README-cn.md at master · tindy2013/subconverter")。 |
| config       | `''`      | 外部配置的地址 (包含分组和规则部分)，当此参数不存在时使用程序的主程序目录中的配置文件，参考的链接见下方表格。 | 详见 [Sub Converter 外部配置](https://github.com/tindy2013/subconverter/blob/master/README-cn.md#%E5%A4%96%E9%83%A8%E9%85%8D%E7%BD%AE "subconverter/README-cn.md at master · tindy2013/subconverter")。 |
| emoji        | `'true'`  | 用于设置节点名称是否包含 Emoji。                                                                              | 对于 Emoji 的设置请勿随意更改，日后可能会使用其他方法更改节点名称！                                                                                                                                     |
| add_emoji    | `'false'` | 用于在节点名称前加入 Emoji。                                                                                  | 对于 Emoji 的设置请勿随意更改，日后可能会使用其他方法更改节点名称！                                                                                                                                     |
| remove_emoji | `'true'`  | 用于设置是否删除节点名称中原有的 Emoji。                                                                      | 对于 Emoji 的设置请勿随意更改，日后可能会使用其他方法更改节点名称！                                                                                                                                     |

#### 可用 `config`

| 配置名称     | 配置描述                                       | 配置链接                                                                                                            |
| :----------- | :--------------------------------------------- | :------------------------------------------------------------------------------------------------------------------ |
| no-url-test  | Universal                                      | <https://fastly.jsdelivr.net/gh/SleepyHeeead/subconverter-config@gh-pages/remote-config/universal/no-urltest.ini>   |
| url-test     | Universal                                      | <https://fastly.jsdelivr.net/gh/SleepyHeeead/subconverter-config@gh-pages/remote-config/universal/urltest.ini>      |
| maying       | Customized                                     | <https://fastly.jsdelivr.net/gh/SleepyHeeead/subconverter-config@gh-pages/remote-config/customized/maying.ini>      |
| y-too        | Customized                                     | <https://fastly.jsdelivr.net/gh/SleepyHeeead/subconverter-config@gh-pages/remote-config/customized/ytoo.ini>        |
| flower-cloud | Customized                                     | <https://fastly.jsdelivr.net/gh/SleepyHeeead/subconverter-config@gh-pages/remote-config/customized/flowercloud.ini> |
| nyan-cat     | Customized                                     | <https://fastly.jsdelivr.net/gh/SleepyHeeead/subconverter-config@gh-pages/remote-config/customized/nyancat.ini>     |
| nexitally    | Customized                                     | <https://fastly.jsdelivr.net/gh/SleepyHeeead/subconverter-config@gh-pages/remote-config/customized/nexitally.ini>   |
| so-cloud     | Customized                                     | <https://fastly.jsdelivr.net/gh/SleepyHeeead/subconverter-config@gh-pages/remote-config/customized/socloud.ini>     |
| ark          | Customized                                     | <https://fastly.jsdelivr.net/gh/SleepyHeeead/subconverter-config@gh-pages/remote-config/customized/ark.ini>         |
| ssr-cloud    | Customized                                     | <https://fastly.jsdelivr.net/gh/SleepyHeeead/subconverter-config@gh-pages/remote-config/customized/ssrcloud.ini>    |
| net-ease     | Special：网易云音乐解锁。仅规则，No-URL-Test。 | <https://fastly.jsdelivr.net/gh/SleepyHeeead/subconverter-config@gh-pages/remote-config/special/netease.ini>        |
| basic        | Special：仅 GEOIP CN + Final。                 | <https://fastly.jsdelivr.net/gh/SleepyHeeead/subconverter-config@gh-pages/remote-config/special/basic.ini>          |

:::tip 提示
更多配置可前往 [Sub Converter Config](https://github.com/SleepyHeeead/subconverter-config "SleepyHeeead/subconverter-config") 查看。
:::

:::tip 提示
默认规则不一定好用，此时可以考虑对配置文件进行规则设置。

:::details 建议添加规则

```yaml
rules:
  - DOMAIN-SUFFIX,tencentcs.com,DIRECT # 腾讯云
  - DOMAIN-SUFFIX,pufei.org,DIRECT # 扑飞漫画
  - DOMAIN,res.img.jituoli.com,DIRECT # 扑飞漫画图床
  - DOMAIN-SUFFIX,qyi.io,DIRECT # 浅忆博客
```

:::

### `profile` 设置

配置文件的相关设置。

```yaml
profile:
  clash:
    not-supported-ciphers:
      - "rc4"
```

| 参数                  | 默认值    | 解释                   | 备注 |
| :-------------------- | :-------- | :--------------------- | :--- |
| clash                 | ——        | clash 配置文件的设置。 | ——   |
| not-supported-ciphers | `- 'rc4'` | 不受支持的加密方式     | ——   |

### `others` 配置

其他设置。

```yaml
others:
  directories:
    shared-links-stored-dir: "./links"
    profiles-stored-dir: "../Profiles"
    temp-file-stored-dir: "./temp"

  supported-shared-link-begin-with: "ss://.*|ssr://.*|vmess://.*|vless://.*|trojan://.*"
  supported-subscribe-link-begin-with: "http://.*|https://*"
  not-supported-yaml-tags:
    - "str"
```

| 参数                                | 默认值                                                     | 解释                       | 备注         |
| :---------------------------------- | :--------------------------------------------------------- | :------------------------- | :----------- |
| directories                         | ——                                                         | 关于文件夹的设置。         | ——           |
| shared-links-stored-dir             | `'./links'`                                                | 保存链接文件的文件夹位置。 | ——           |
| profiles-stored-dir                 | `'../Profiles'`                                            | 保存配置文件的文件夹位置。 | ——           |
| temp-file-stored-dir                | `'./temp'`                                                 | 临时保存文件的文件夹位置。 | ——           |
| supported-shared-link-begin-with    | `'ss://.*\|ssr://.*\|vmess://.*\|vless://.*\|trojan://.*'` | 受支持的分享链接的开头。   | 正则表达式。 |
| supported-subscribe-link-begin-with | `'http://.*\|https://.*'`                                  | 受支持的订阅链接的开头。   | 正则表达式。 |
| not-supported-yaml-tags             | `- 'rc4'`                                                  | 不受支持的 YAML 标签。     | ——           |

## 设置示例

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

profile:
  clash:
    not-supported-ciphers:
      - "rc4"

others:
  directories:
    shared-links-stored-dir: "./links"
    profiles-stored-dir: "../Profiles"
    temp-file-stored-dir: "./temp"

  supported-shared-link-begin-with: "ss://.*|ssr://.*|vmess://.*|vless://.*|trojan://.*"
  supported-subscribe-link-begin-with: "http://.*|https://*"
  not-supported-yaml-tags:
    - "str"
```
