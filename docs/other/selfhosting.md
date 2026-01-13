---
title: Selfhosting FMHY
description: This guide will help you set up and run your own instance of FMHY locally.
---


# 自主托管

警告
请注意,您必须****将您的实例与官方网站 (fmhy.net) 区分起来,以避免混.
其他:

本指南将帮助您在本地设置和运行您自己的FMHY实例.

### 试验室

运行本地实例,您需要安装 [Docker](https://docs.docker.com/get-docker/)和 [Docker Compose](https://docs.docker.com/compose/install/).

安装后,运行以下命令:

```bash
git clone https://github.com/fmhy/edit.git
cd edit
sudo docker compose up --build
```

需要几分钟的时间来构建图像,

### 尼克斯·弗莱克

您可以使用 [nix](https://nixos.org/)来设置开发环境,我们有一个 [flake](https://nixos.wiki/wiki/Flakes)设置了 `nodejs`和 `pnpm`.

1. 叉存储库,并用`git clone https://github.com/fmhy/edit.git`将其克隆到本地机器上.
2. 运行 `nix flake update`更新锁文件.
3. 运行 `nix develop`进入开发环境.
4. 改变自己的生活.
5. 通过运行 `exit` 离开开发环境.

### 按手动使用

您需要安装以下:
- 保护的
- 保护_51__ - 安装版本 25.2.1
- 保护的

#### 步骤1:克隆存储库

```bash
git clone https://github.com/fmhy/edit.git
cd edit
```

#### 步骤 2: 安装依赖

使用 pnpm 安装项目依赖性:

```bash
pnpm install
```

#### 步骤3:发展模式

为了在开发模式下运行项目:

```bash
# Start the documentation site in dev mode
pnpm docs:dev

# Start the API in dev mode (if needed)
pnpm api:dev
```

开发服务器将默认地启动在 `http://localhost:5173`.

#### 第四步: 建设生产

你需要更新:
- 保护_16__: 在 __ 保护_17__ 中恒定
- `name`:您的实例名称
- 您的域名
- `description`:您的实例描述
- 保护_21__: 开放图标
- `build`: 构建选项 (可以配置为 [Environment Variables](/other/selfhosting#environment-variables))
- 保护的
- 保护的24
- 保护的25
- 保护的
- 保护的

为了生产项目:

```bash
# Build the documentation site
pnpm docs:build

# Build the API (if needed) using the Node.js preset
NITRO_PRESET=node pnpm api:build
```

#### 步骤5: 预览制作构建

为了预览本地生产建筑:

```bash
# Preview the documentation site
pnpm docs:preview

# Preview the API (if needed)
pnpm api:preview
```

#### 步骤 6:部署

查看PROTECTED_54__更多信息.

### 应用程序的部署

如果您想部署API组件 (反系统),您需要设置Cloudflare工作者和KV存储.

#### 条件

- 保护的55
- 已在全球范围内安装

#### 步骤1:配置轮器

更新您的Cloudflare帐户信息:

1. 从Cloudflare仪表板中获取帐户ID (在右侧中找到)
2. 替换在 `wrangler.toml` 中的 `account_id`值,用您的帐户ID
3. 如果您使用自定义域名,请保留 `workers_dev = false`,并更新 `routes`部分
4. 如果您正在将其部署到 `*.workers.dev`,设置 `workers_dev = true`,然后删除 `routes`部分

#### 步骤 2: 创建KV名区

创建一个KV名字空间用于数据存储:

```bash
npx wrangler kv:namespace create STORAGE
```

这个命令将返回一个名字空间ID.复制这个ID,并在 `wrangler.toml` (行14) 的 `[[kv_namespaces]]`部分中取代 `id`值.

** 注:** 如果您想在本地 (例如,在CI/CD中) 运行Wrangler的情况下部署,您需要:
1. 在Cloudflare仪表板中手动创建KV名字空间
2. 在叉中更新`account_id`和 `id`值

#### 第三步: 建立和部署

构建和部署API:

```bash
# Build the API
pnpm api:build

# Deploy to Cloudflare Workers
pnpm api:deploy
```

应用程序将部署到您配置的域名或`*.workers.dev`子域名.

#### 利率限制 (可选)

通过Cloudflare仪表板设置速度限制器绑定.您可以跳过此项用于基本部署或在"速度限制"部分下通过Workers仪表板后设置.

#### 环境变量

##### 建时变量 (用于文档)

这些变量控制在构建文档网站时所包含的内容:

- 系统的安全性,安全性,安全性,安全性,安全性,安全性,安全性,安全性,安全性,安全性,安全性,安全性,安全性,安全性,安全性,安全性,安全性,安全性,安全性,安全性,安全性,安全性,安全性,安全性,安全性,安全性等等.
- 保护_44__ - 启用反系统的API组件

##### 运行时间变量 (用于API工作者)

应用程序使用了以下变量:

- 为了发布反消息,Discord webhook URL (需要用于API反功能)

#### 解决问题

1. 如果遇到Node.js版本问题,请确保您正在使用Node.js 21+
2. 对于PNPM相关的问题,请确保您使用PNPM 9+
3. 如果遇到构建问题,请尝试清除缓存:
    ```bash
    # Linux
    rm -rf docs/.vitepress/cache

    # PowerShell
    rm -r -fo docs/.vitepress/cache
    ```

### 逆转代理

您应该能够使用任何反向代理,但找到一个合理的配置为 nginx 服务器 [in the repo here](https://github.com/fmhy/edit/blob/main/.github/assets/nginx.conf)