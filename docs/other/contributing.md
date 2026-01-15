---
title: 贡献指南
description: 如何为项目做贡献。
next: false
prev: false
---

# 贡献指南

> [!INFO] 注意
> 如果您在我们的 [Discord](https://github.com/fmhy/FMHY/wiki/FMHY-Discord) 中，其中一些步骤会更容易。它每周五开放。

在这里您可以找到一些想开始贡献的人的一般指导原则。有多种方式可以做到这一点：

- [链接提交](#submissions)
- [报告现有站点](#reporting-a-site)
- [如何编辑和预览更改](#making-changes)
- [寻找新站点](https://www.reddit.com/r/FREEMEDIAHECKYEAH/wiki/find-new-sites/)

## 提交

> [!INFO] 注意
> 对于对维基进行的重大更改，例如精简努力或页面/部分的重组，您必须先通过 [Discord](https://github.com/fmhy/FMHY/wiki/FMHY-Discord) 与我们讨论，然后再打开 [拉取请求](https://github.com/fmhy/edit/pulls)。

**不要提交以下任何内容：**

- **💰️ 付费 / 试用站点** - 我们不接受任何仅付费或免费试用的条目，但某些付费 [VPN](/privacy#vpn) 和 [Debrid](/downloading#debrid-leeches) 除外。
- **🕹️ 模拟器** - 已在 [索引站点](/gaming#emulators) 上列出。
- **🌐 网络浏览器** - 好的开源浏览器已经列出，所以我们只接受 [索引](/internet-tools#browser-tools)、注重隐私的和好的移动浏览器。
- **🔻 雷池** - 除非现有的 [雷池列表](/downloading#debrid-leeches) 中没有列出，否则不要提交这些。
- **🐧 Linux 发行版** - 已在 [索引站点](/linux-macos#linux-distros) 上列出。
- **🌍 非英语软件** - 我们不添加非英语软件站点（APK、游戏、种子等），除非它们有非常好的声誉。
- **🗂️ 编程库** - 它们太多了，有更好的地方可以找到它们。
- **🎲 挖矿 / 投注站点** - 不要提交任何与投注、挖矿、BINs、CCs 等相关的内容。
- **🎮 多人游戏破解** - 不要提交任何在多人游戏中提供不公平优势的破解或漏洞。
- **🖥️ 自定义操作系统** - 我们不建议人们使用这些。

### 添加一个站点

对于提交新链接，请遵循以下步骤：

- 确保它还没有在维基中。最简单的方法是使用 `ctrl+f` 在我们的 [单页](https://api.fmhy.net/single-page) 中检查。
- 不要一次提交一堆未经测试的链接。尽量只发送您真正觉得可能值得添加的内容。
- 通过反馈系统、[GitHub](https://github.com/fmhy/edit) 或加入我们的 [Discord](https://github.com/fmhy/FMHY/wiki/FMHY-Discord) 联系我们。请注意，我们必须自己检查站点，因此使用问题而不是拉取请求会更简单。
- 您可以选择性地包含社交、工具或任何其他附加信息以及条目。

### 报告一个站点

> [!INFO] 注意
> 如果是紧急情况，您可以通过我们的反馈系统请求邀请。

对于现有条目的更改，请遵循以下步骤：

- 通过反馈系统、[GitHub](https://github.com/fmhy/edit) 或加入我们的 [Discord](https://github.com/fmhy/FMHY/wiki/FMHY-Discord) 联系我们。
- 使用反馈系统时，如果需要，可以留下联系方式。只有受信任的员工才能查看此信息。
- 如果您想报告站点移除或星标更改，您必须包括详细说明为什么应接受您的更改。

### 链接测试

所有添加都必须首先在 [Discord](https://github.com/fmhy/FMHY/wiki/FMHY-Discord) 上经过我们的测试过程。

您可以帮助我们测试新站点，以确定其用途、安全性以及是否适合维基。

请记住，某些站点（如盗版站点）需要更多的测试/审查才能添加。

### 格式规则

维基将始终存在一些变化，这可能是由于例外情况、布局/结构或 markdown 本身的灵活性造成的。

出于这些原因，有太多条件和细微差别需要满足，因此很难制定易于遵循的指南。但是，您通常可以通过查看现有链接的结构来了解。

请注意，我们确实尝试按从最佳到最差的顺序排列章节，如果多条链接在同一行上，则只有 **粗体** 的才被视为星标。

如果您不确定，请在 [Discord](https://github.com/fmhy/FMHY/wiki/FMHY-Discord) 上的维基频道询问，并等待工作人员回复。

## 进行更改

关于各种编辑维基和预览更改的方法的说明。

### GitHub 编辑器

您可以使用内置的网络编辑器，有两种方法：

1. 找到您要编辑的文件，查找编辑图标（铅笔图标）并点击，然后进行更改。

    ![Edit Button](https://files.catbox.moe/7w3hnm.png)

2. 完成后，点击"提交更改..."然后点击"提议更改"。可选择添加提交描述。

3. 您现在应该看到显示所有编辑的比较页面。点击"创建拉取请求"，填写描述更改的框，然后点击提交。

**或者**

1. 通过点击右上角的"Fork"按钮派生存储库。

2. 导航到您的派生主页，然后在键盘上按 `.` (句号) 键。这将在 `github.dev` 上以类似 VSCode 的环境打开存储库。

3. 进行更改，然后通过源代码控制选项卡提交。

    ![Source Control](https://files.catbox.moe/pa571v.png)

4. 回到您的派生主页，点击"贡献"然后点击"打开拉取请求"。

5. 您现在应该看到显示所有编辑的比较页面。点击"创建拉取请求"，填写描述更改的框，然后点击提交。

### 开发环境

如果您要处理网站本身，或只是想预览网站和任何更改，您可以通过设置开发环境来实现。

#### GitHub Codespaces

这会在浏览器中创建一个环境 [(每月有 60 小时免费配额)](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces#free-and-billed-use-by-personal-accounts)。要使用 Codespaces，请按照以下步骤操作：

1. 通过点击右上角的"Fork"按钮派生存储库。

2. 导航到您的派生主页，点击上方存储库中的绿色"Code"按钮，打开"Codespaces"选项卡并点击"Create codespace"。

3. 您可能需要等待 ~5-10 分钟让 codespace 加载。

    ![Codespace Status](https://files.catbox.moe/5bp38f.png)

4. 一旦加载完成，运行 `pnpm i && pnpm docs:dev` 启动预览。然后当它出现时，点击右下角的"在浏览器中打开"。

5. 进行更改并提交。

6. 要关闭它，再次点击"Code"按钮，在 codespace 旁边的 `...` 下拉菜单中点击"Stop codespace"。

#### 本地实例

在本地存储库中进行更改可能需要对 Git 有基本了解。您可以在 [此处](/educational#developer-learning) 找到学习资源。

有关手动设置的更多信息可在 [此处](/other/selfhosting) 找到。
