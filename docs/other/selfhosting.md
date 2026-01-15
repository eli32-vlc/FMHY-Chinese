---
title: 自托管 FMHY
description: 本指南将帮助您在本地设置和运行自己的 FMHY 实例。
---

# 自托管

:::warning
请注意，您**必须**将您的实例与官方网站 (fmhy.net) 区分开来，以避免混淆。下面给出了这样做的步骤。
:::

本指南将帮助您在本地设置和运行自己的 FMHY 实例。

### Docker (实验性)

要运行本地实例，您需要安装 [Docker](https://docs.docker.com/get-docker/) 和 [Docker Compose](https://docs.docker.com/compose/install/)。

安装完成后，运行以下命令：

```bash
git clone https://github.com/fmhy/edit.git
cd edit
sudo docker compose up --build
```

构建镜像并启动容器可能需要几分钟时间，在端口 4173 上运行。

### Nix Flake

您可以使用 [nix](https://nixos.org/) 来设置开发环境，我们有一个 [flake](https://nixos.wiki/wiki/Flakes) 可以设置 `nodejs` 和 `pnpm`。

1. Fork 仓库并使用 `git clone https://github.com/fmhy/edit.git` 将其克隆到您的本地机器。
2. 运行 `nix flake update` 更新 flake 锁定文件。
3. 运行 `nix develop` 进入开发环境。
4. 进行您的更改。
5. 通过运行 `exit` 退出开发环境。

### 手动

您需要安装以下内容：
- [Git](https://git-scm.com/downloads)
- [Node.js](https://nodejs.org/en/download/) - 安装版本 25.2.1
- [pnpm 9.12.2+](https://pnpm.io/installation)

#### 步骤 1：克隆仓库

```bash
git clone https://github.com/fmhy/edit.git
cd edit
```

#### 步骤 2：安装依赖项

使用 pnpm 安装项目依赖项：

```bash
pnpm install
```

#### 步骤 3：开发模式

要在开发模式下运行项目：

```bash
# 在开发模式下启动文档站点
pnpm docs:dev

# 在开发模式下启动 API (如果需要)
pnpm api:dev
```

开发服务器将默认在 `http://localhost:5173` 启动。

#### 步骤 4：构建生产版本

您需要更新：
- `meta`: `docs/.vitepress/constants.ts` 中的常量
  - `name`: 您的实例名称
  - `hostname`: 您的域名
  - `description`: 您的实例描述
  - `tags`: Opengraph 标签
  - `build`: 构建选项 (可以使用 [环境变量](/other/selfhosting#environment-variables) 配置)
- `docs/index.md`
  - `title`
  - `description`
  - `hero.name`
  - `hero.tagline`

构建生产版本的项目：

```bash
# 构建文档站点
pnpm docs:build

# 使用 Node.js 预设构建 API (如果需要)
NITRO_PRESET=node pnpm api:build
```

#### 步骤 5：预览生产构建

在本地预览生产构建：

```bash
# 预览文档站点
pnpm docs:preview

# 预览 API (如果需要)
pnpm api:preview
```

#### 步骤 6：部署

查看 [VitePress 部署指南](https://vitepress.dev/guide/deploy) 获取更多信息。

### API 部署

如果您想部署 API 组件 (反馈系统)，您需要设置 Cloudflare Workers 和 KV 存储。

#### 先决条件

- 一个 [Cloudflare 账户](https://dash.cloudflare.com/sign-up)
- 全局安装 [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/install-and-update/)

#### 步骤 1：配置 Wrangler

使用您的 Cloudflare 账户信息更新 `wrangler.toml`：

1. 从 Cloudflare 仪表板获取您的账户 ID (位于右侧边栏)
2. 用您的账户 ID 替换 `wrangler.toml` 中的 `account_id` 值
3. 如果您使用自定义域名，请保持 `workers_dev = false` 并更新 `routes` 部分
4. 如果您部署到 `*.workers.dev`，请设置 `workers_dev = true` 并删除 `routes` 部分

#### 步骤 2：创建 KV 命名空间

为数据存储创建一个 KV 命名空间：

```bash
npx wrangler kv:namespace create STORAGE
```

此命令将返回一个命名空间 ID。复制此 ID 并替换 `wrangler.toml` 中 `[[kv_namespaces]]` 部分的 `id` 值 (第 14 行)。

**注意：** 如果您想在不运行本地 Wrangler 的情况下部署 (例如，在 CI/CD 中)，您需要：
1. 在 Cloudflare 仪表板中手动创建 KV 命名空间
2. 在您的 fork 中更新 `wrangler.toml` 中的 `account_id` 和 `id` 值

#### 步骤 3：构建和部署

构建并部署 API：

```bash
# 构建 API
pnpm api:build

# 部署到 Cloudflare Workers
pnpm api:deploy
```

API 将被部署到您配置的域名或 `*.workers.dev` 子域名。

#### 速率限制 (可选)

速率限制器绑定需要通过 Cloudflare 仪表板设置。对于基本部署，您可以跳过此步骤，或稍后通过 Workers 仪表板在"速率限制"部分进行配置。

#### 环境变量

##### 构建时变量 (用于文档)

这些变量控制构建文档站点时包含的内容：

- `FMHY_BUILD_NSFW` - 启用 NSFW 侧边栏条目 (实验性)
- `FMHY_BUILD_API` - 为反馈系统启用 API 组件

##### 运行时变量 (用于 API Worker)

这些变量由部署的 Cloudflare Worker API 使用：

- `WEBHOOK_URL` - 用于发布反馈消息的 Discord webhook URL (API 反馈功能必需)

#### 故障排除

1. 如果遇到 Node.js 版本问题，请确保您使用的是 Node.js 21+
2. 对于 pnpm 相关问题，请确保您使用的是 pnpm 9+
3. 如果遇到构建问题，请尝试清除缓存：
    ```bash
    # Linux
    rm -rf docs/.vitepress/cache

    # PowerShell
    rm -r -fo docs/.vitepress/cache
    ```

### 反向代理

您应该能够将任何反向代理与此 vitepress 网站一起使用，但在 [此处的仓库中](https://github.com/fmhy/edit/blob/main/.github/assets/nginx.conf) 找到了适用于 nginx 服务器的合理配置