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

为了运行本地实例,您需要安装 KEEP46/KEEP和 KEEP47/KEEP.

安装后,运行以下命令:

```bash
git clone https://github.com/fmhy/edit.git
cd edit
sudo docker compose up --build
```

需要几分钟的时间来构建图像,

### 尼克斯·弗莱克

您可以使用KEEP48/KEEP来设置开发环境,我们有一个设置KEEP49/KEEP的KEEP9/KEEP和KEEP10/KEEP.

1. 叉存储库,并用 KEEP11/KEEP将其克隆到本地机器上.
2. 运行 KEEP12/KEEP以更新锁文件.
3. 运行 KEEP13/KEEP进入开发环境.
4. 改变自己的生活.
5. 通过运行 KEEP14/KEEP,离开开发环境.

### 按手动使用

您需要安装以下:
- KEEP50/KEEP
- KEEP51/KEEP - 安装版本 25.2.1
- KEEP52/KEEP

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

开发服务器将默认地启动在 KEEP15/KEEP.

#### 第四步: 建设生产

你需要更新:
- KEEP16/KEEP: 常在 KEEP17/KEEP
- KEEP18/KEEP:您的实例名称
- KEEP19/KEEP:您的域名
- KEEP20/KEEP:您的情况描述
- KEEP21/KEEP:开图标签
- KEEP22/KEEP: 构建选项 (可配置为 KEEP53/KEEP)
- KEEP23/KEEP
- KEEP24/KEEP
- KEEP25/KEEP
- KEEP26/KEEP
- KEEP27/KEEP

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

查看更多信息.

### 应用程序的部署

如果您想部署API组件 (反系统),您需要设置Cloudflare工作者和KV存储.

#### 条件

- KEEP55/KEEP
- KEEP56/KEEP全球安装

#### 步骤1:配置轮器

更新 KEEP28/KEEP,并使用Cloudflare帐户信息:

1. 从Cloudflare仪表板中获取帐户ID (在右侧中找到)
2. 取代您的账户ID的 KEEP29/KEEP值在 KEEP30/KEEP中
3. 如果您使用自定义域名,请保持KEEP31/KEEP,并更新KEEP32/KEEP部分
4. 如果您正在部署到 KEEP33/KEEP,设置 KEEP34/KEEP,然后删除 KEEP35/KEEP部分

#### 步骤 2: 创建KV名区

创建一个KV名字空间用于数据存储:

```bash
npx wrangler kv:namespace create STORAGE
```

这个命令将返回一个名字空间ID.复制这个ID,并在KEEP36/KEEP的KEEP37/KEEP部分 (行14) 中取代KEEP36/KEEP值.

** 注:** 如果您想在本地 (例如,在CI/CD中) 运行Wrangler的情况下部署,您需要:
1. 在Cloudflare仪表板中手动创建KV名字空间
2. 在叉上更新KEEP39/KEEP和KEEP40/KEEP的值

#### 第三步: 建立和部署

构建和部署API:

```bash
# Build the API
pnpm api:build

# Deploy to Cloudflare Workers
pnpm api:deploy
```

应用程序将部署到您配置的域名或KEEP42/KEEP子域名.

#### 利率限制 (可选)

通过Cloudflare仪表板设置速度限制器绑定.您可以跳过此项用于基本部署或在"速度限制"部分下通过Workers仪表板后设置.

#### 环境变量

##### 建时变量 (用于文档)

这些变量控制在构建文档网站时所包含的内容:

- KEEP43/KEEP - 启用NSFW侧行输入 (实验性)
- KEEP44/KEEP - 启用反系统的API组件

##### 运行时间变量 (用于API工作者)

应用程序使用了以下变量:

- KEEP45/KEEP - 为了发布反消息,Discord webhook URL (需要用于API反功能)

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

您应该能够使用任何反向代理,但找到一个合理的配置为 nginx 服务器