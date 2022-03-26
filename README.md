# [Profiles_for_Clash](https://github.com/Shuery-Shuai/Profiles_for_Clash "Shuery-Shuai/Profiles_for_Clash: Profiles can be used in Clash for Windows, Clash for Android and so on.")

使用 Python 自动获取一些可用于 _Clash for Windows_、_Clash for Android_ 等应用的配置文件。

> **警告**：通过使用特殊方式访问外网时请**严格遵守当地法律法规**，**禁止借此进行传播“黄、赌、毒”等违法犯罪活动**。节点均来自网络收集，由网友免费提供，请**勿使用节点进行 BT 下载**。

## 脚本使用教程

### 基本使用

#### Github\_Actions

1. `Fork` 本项目。
2. 进入你 `Fork` 的仓库。
3. 进入 `Actions` 页面。
4. 选择任意一个 `workflow。`
5. 右侧点击 `Run workflow`。
6. 等待脚本执行完成。

#### 本地执行

##### 下载发布的版本后执行

1. 前往 `Release` 页面。
2. 下载 `Profile for Clash Auto Getter.zip`。
3. 解压 `Profile for Clash Auto Getter.zip`。
4. 根据系统双击 `run` 脚本运行。
   - **Linux** or **macOS**：运行 `run.sh`。
   - **Windows**：运行 `run.ps1`。

##### 克隆本项目后执行

1. 克隆本项目。

   ```sh
   git clone https://github.com/Shuery-Shuai/Profiles_for_Clash.git
   ```

2. 进入 `auto_getter` 目录。

   ```sh
   cd ./Profiles_for_Clash/auto-getter
   ```

3. 安装 Python 依赖包。

   ```sh
   pip install -r requirements.txt
   ```

4. 运行脚本

   ```sh
   python ./main.py
   ```

5. 等待脚本运行完成。

### 高级使用

即在运行脚本前根据[脚本设置](https://github.com/Shuery-Shuai/Profiles_for_Clash/wiki/%E8%84%9A%E6%9C%AC%E8%AE%BE%E7%BD%AE '脚本设置 · Shuery-Shuai/Profiles_for_Clash Wiki')设置项目后运行本项目。

## 配置使用教程

[配置文件 WIKI](https://github.com/Shuery-Shuai/Profiles_for_Clash/wiki/%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6 '配置文件 · Shuery-Shuai/Profiles_for_Clash Wiki')
