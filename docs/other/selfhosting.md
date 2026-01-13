---
title: Selfhosting FMHY
description: This guide will help you set up and run your own instance of FMHY locally.
---


自我创业

* 警报:警报
请注意,**必须** 将您的例子与官方网站(fmhy.net)区分开来,以避免混乱。
· :

这份指南将帮助您在当地建立和管理自己的FMHY实例。



要运行本地实例,您需要安装[Docker](https://docs.docker.com/get-docker/)和[Docker Composte](https://docs.docker.com/compose/stall/)。

安装两个命令后,运行以下命令:

```bash
git clone https://github.com/fmhy/edit.git
cd edit
sudo docker compose up --build
```

建造图像和启动集装箱可能需要几分钟时间,在4173号港口运行。

尼斯花

您可以使用[nix](https://nixos.org/)建立一个发展环境,我们有一个[flake](https://nixos.wiki/wiki/Flakes)设置了__CODE_BLlock_9__和__CODE_BLock_10__。

1. 叉入存储器,并用 CODE_BLOCK_11___复制到本地机器。
2. 运行 CODE_BLOCK_12__ 以更新片片锁定文件。
3. 运行 CODE_BLock_13__进入开发环境。
4. 作出改变。
5. 运行 CODE_BLOCK_14 退出开发环境。

手动

您需要安装以下设备:
- [声](https://git-scm.com/downloads)
- [Node.js] (https://nodejs.org/en/download/) - 安装版本25.2.1
- [pnpm 9.12.2+](https://pnpm.io/安插)

第一步 开启仓库

```bash
git clone https://github.com/fmhy/edit.git
cd edit
```

步骤2:安装依赖性

使用 pnpm 安装项目依赖关系 :

```bash
pnpm install
```

步骤3:发展模式

以开发模式运行项目:

```bash
# Start the documentation site in dev mode
pnpm docs:dev

# Start the API in dev mode (if needed)
pnpm api:dev
```

默认开发服务器将启动于 CODE_BLock_15 。

步骤4:建设生产基地

您需要更新 :
- 编号_BLock_16__:常数在_CODE_BLock_17__
- 编号_BLlock_18__: 实例名称
- 您的域名 - CODE_Block_19__:
- 编号BLlock_20__ : 描述您的例子
- 开放标记 - 开放标记
-`build`:构建选项(可以配置[环境变量](/其他/自我托管#环境变量))
- 编号Block_23__
- 编号Block_24__
- 编号Block_25__
- 编号Block_26__
- 编号Block_27__

建造生产项目:

```bash
# Build the documentation site
pnpm docs:build

# Build the API (if needed) using the Node.js preset
NITRO_PRESET=node pnpm api:build
```

第五步:预览制作构建

预览本地生产构建 :

```bash
# Preview the documentation site
pnpm docs:preview

# Preview the API (if needed)
pnpm api:preview
```

第六步:部署

更多信息,请参见[《邮报部署指南》](https://vitepress.dev/guide/deplove)。

API 部署

如果您想要部署 API 组件( 反馈系统) , 需要建立云辉工人和 KV 存储系统 。

先决条件

- [Cloudflare帐户](https://dash.cloudflare.com/sign-up)
- [Wrangler CLI](https:// developmenters.cloudflare.com/workers/wrangler/安装和更新/)

第一步:配置划线器

更新 CODE_BLOCK_28 更新您的云辉账户信息 :

1. 从“云辉”仪表板(右侧栏找到)获取账户编号。
2. 将编号编号为`CODE_BLock_29__中的 `CODE_BLock_30__ 中的 `CODE_BLock_29__ 值替换为您的账户编号。
3. 如果使用自定义域名,请保留 CODE_BLock_31__,并更新 CODE_BLock_32__ 部分。
4. 部署到 CODE_BLock_33__,设置 CODE_BLock_34__,删除 CODE_BLock_35__ 区域

第一步 2: 创建 KV 命名空间

创建数据存储的 KV 命名空间 :

```bash
npx wrangler kv:namespace create STORAGE
```

此命令将返回一个命名空间 ID。 复制此 ID, 并替换 CODE_ BLOCK_ 36__ 中的 CODE_ BLOCK_ 37__ 部分 。 CODE_ BLOCK_ 38__ (第14行) 。

** 注:** 如果要在不在当地运行 wrangler 的情况下部署,(例如,在 CI/CD 中),您需要:
1. 在云辉仪表板上手动创建 KV 命名空间
2. 更新叉口中的 CODE_BLock_39__ 和 CODE_BLock_40__ 中的 DCDE_BLock_41___ 数值。

步骤3:建设和部署

构建并部署 API :

```bash
# Build the API
pnpm api:build

# Deploy to Cloudflare Workers
pnpm api:deploy
```

API 将应用到您配置的域名或 CODE_BLock_42__ 子域 。

比率限制(可选)

限制费率的绑定要求通过“云辉”仪表板设置。您可以跳过这个选项进行基本部署,也可以稍后通过“限制时间”栏下的“工人仪表板”配置。

环境变量

构建时变量(用于文档)

建立文档站点时, 这些变量控制包含的内容 :

- - CODE_BLlock_43__ - 启用 NSFW 侧边栏条目(实验性)
- - - CODE_BLlock_44__ - 启用 API 组件用于反馈系统

运行时变量( API 工人的运行时间变量)

部署的云辉工人API使用这些变量:

- - CODE_BLlock_45__ - 用于发布反馈信息的Discord webhook URL(需要 API 反馈功能)

排除困难

1. 如果遇到Node.js版本问题,确保使用Node.js 21+
2. 与pnpm有关的问题,确保使用pnpm 9+
3. 如果遇到建筑问题,请尝试清除缓存:
    ```bash
    # Linux
    rm -rf docs/.vitepress/cache

    # PowerShell
    rm -r -fo docs/.vitepress/cache
    ```

反向代理

您应该能够使用此 vitepress 网站的任何反向代理, 但为 nginx 服务器找到合理的配置( https:// github. com/ fmhy/ edit/ blob/ main/. github/assets/ nginx. conf) 。