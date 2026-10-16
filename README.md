# community-poster17-skill

`community-poster17-skill` 是在 Codex 中根据社区活动文案和参考图片制作中英文社区服务海报的项目。它提供本地风格参考图，使用随包附带的 88API Nano Banana 生成场景参考，再调用火山方舟豆包 Seedream 5.0 Pro 生成带文字的完整海报。

当前包内 `SKILL.md` 的 Codex 调用名仍是 `community-poster-editable`，因此下文的安装目录和调用示例使用这个内部名称。

> 当前版本默认交付模型生成的图片，**不附带可视化编辑器或可编辑工程文件**。`SKILL.md` 是 Codex 执行流程的依据；本 README 面向安装和使用者。

## 环境要求

- 可运行本地命令的 Codex 环境，以及网络连接。
- Node.js 18 或更新版本。
- Python 3.10 或更新版本。
- 可调用 88api.ai 图像模型的 **88API Key**，以及火山方舟豆包图像模型的 **Ark API Key**。两种 Key 不能互换；生成请求可能收费。

## 安装与配置

1. 将整个 `community-poster-editable` 文件夹放入 Codex 的 skills 目录，通常是 `~/.codex/skills/community-poster-editable/`。保留 `SKILL.md`、`references/`、`scripts/` 和 `vendor/` 的相对位置，然后新建一个 Codex 对话。
2. 安装豆包脚本依赖：

   ```text
   python -m pip install -r <skill目录>/scripts/requirements-doubao.txt
   ```

3. 配置 88API Key。Nano Banana 脚本已经随包提供，无需单独安装插件。先检查配置；未配置时，按照 `vendor/88api-nano-banana/skills/88api-nano-banana/SKILL.md` 的指引设置 Key：

   ```text
   node <skill目录>/vendor/88api-nano-banana/scripts/generate.mjs --get-config
   ```

4. 配置 Ark API Key。Windows 可使用 `scripts/set-ark-api-key.ps1` 隐藏输入；其他系统设置环境变量 `COMMUNITY_POSTER_ARK_API_KEY`。
5. 运行不收费的本地检查：

   ```text
   node <skill目录>/vendor/88api-nano-banana/scripts/generate.mjs --self-test
   python <skill目录>/scripts/doubao_generate.py --check
   ```

详细安装说明见 skill 目录中的 `PORTABLE_SETUP.md`。API Key 只保存在使用者自己的配置或环境变量中，不应写入 skill、提示词、输出文件或分享包。

## 在 Codex 中使用

在消息中调用 `$community-poster-editable`，并提供活动文案与可用图片。建议写清活动名称、主办方、时间、地点、项目、参加方式、注意事项，以及必须原样使用的 Logo 或文字。缺少地点时，skill 不会自行编造。

示例：

```text
$community-poster-editable
根据附件中的社区活动通知和现场照片制作中英文海报。
请以通知原文为准，保留活动名称、日期、地点和参加方式。
如有主办方标识，请使用附件中的原始 Logo。
```

默认流程如下：

1. Codex 从本地风格库选出三张参考图供使用者选择。使用者已经指定风格时直接沿用。
2. Codex 锁定活动事实，生成 Nano Banana 场景提示词和中英文完整海报提示词。
3. Nano Banana 生成一张中间场景图，供两种语言共用。
4. 豆包依次生成中文和英文完整海报。默认每种语言请求一次，不自动增加付费版本或重试。
5. Codex 展示并保存接口返回的原始图片。修改旧海报时另存新版本。

默认规格是中文、英文各一张 **4:5 竖版**，请求尺寸为 **1200×1500**。使用者明确指定的语言、比例、尺寸和参考方式优先。

## 输入、输出与限制

| 项目 | 当前版本的行为 |
| --- | --- |
| 文案 | 以用户提供的活动资料为事实来源；参考图中的旧日期、地点、电话、机构和二维码不会当作活动事实。 |
| 图片 | 可使用社区现场图、指定风格图和其他参考图。用户图片会在生成时发送到相应的外部图像服务。 |
| 输出 | 默认保存到当前工作区的 `outputs/community-poster-editable/<task-id>/`；保留提示词、运行记录和模型返回图片。 |
| 文字准确性 | 默认交付模型原图，不做 OCR、逐字校对、补字或重新排版。因此模型生成的文字可能有误。 |
| Logo 一致性 | 模型生成流程无法保证像素级复刻。必须完全一致时，应明确要求使用原始 SVG 或其他源文件，并采用适合精确嵌入的成图方式。 |
| 可编辑性 | 当前版本默认不生成 HTML、可视化编辑器、字体包或分层文件。 |
| 失败处理 | 请求失败或是否已受理不明确时停止，不自动重发；已完成的语言版本会单独交付。 |

## 目录与许可

- `SKILL.md`：Codex 的执行规则。
- `PORTABLE_SETUP.md`：便携安装步骤。
- `references/`：内容、风格、提示词和模型接入说明及参考库。
- `scripts/`：提示词构建、风格检索与豆包生成脚本。
- `vendor/88api-nano-banana/`：随包附带的 Nano Banana 运行代码。
- `THIRD_PARTY_NOTICES.md`、`LICENSE`：第三方资源说明与许可。

分享便携包前，请核对 `THIRD_PARTY_NOTICES.md`，并删除任何个人 API Key、凭证文件和旧任务输出。
