# 脚本使用教程

## 基本使用

### Github Actions

1. 进入 [`Settings` -> `Personal access tokens`](https://github.com/settings/tokens "Personal access tokens") 设置。
2. 点击 `Generate new token`。
3. 输入密码并点击 `Confirm passwrod`。
4. 至少勾选 `repo`、`workflow`、`gist` 项。
5. 点击 `Generate token` 并复制 `Token`。
6. `Fork` 本仓库。
7. 进入你 `Fork` 的仓库。
8. 进入仓库 `Settings` 页面。
9. 找到并进入 `Security` -> `Secrets` -> `Actions` 分页。
10. 点击 `New repository secret`。
11. `Name` 为 `ACCESS TOKEN`，`Value` 为刚刚复制的 `Token`。
12. 点击 `Add secret`。
13. 进入 `Actions` 页面。
14. 选择任意一个 `workflow`。
15. 右侧点击 `Run workflow`。
16. 等待脚本执行完成。

### 本地执行

#### 下载发布的版本后执行

1. 前往 `Release` 页面。
2. 下载 `Profile for Clash Auto Getter.zip`。
3. 解压 `Profile for Clash Auto Getter.zip`。
4. 根据系统双击 `run` 脚本运行。
   - **Linux** or **macOS**：运行 `run.sh`。
   - **Windows**：运行 `run.ps1`。

#### 克隆本项目后执行

1. 克隆本项目。

   ```sh
   git clone https://github.com/LetsShareAll/Profiles_for_Clash.git
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

## 高级使用

即在运行脚本前根据[脚本设置](/guide/script/config "脚本设置")设置项目后运行本项目。

## 配置使用教程

[配置文件](/guide/clash/profile "配置文件")。
