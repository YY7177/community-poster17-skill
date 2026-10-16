# 安装与使用

把整个 `community-poster-editable` 文件夹放到使用者的 Codex skills 目录（通常为 `~/.codex/skills/`），保持文件夹名称不变，然后新建一个 Codex 任务。当前流程只输出豆包生成的海报图片，不使用本地字体或编辑器。

使用者需要 Node.js 18+、Python 3.10+、网络连接和能在 Codex 中运行本地命令的环境。安装豆包脚本依赖：

```text
python -m pip install -r <skill目录>/scripts/requirements-doubao.txt
```

Nano Banana 运行代码已经随包放在 `vendor/88api-nano-banana/`，无需另装插件。首次使用时运行 `node <skill目录>/vendor/88api-nano-banana/scripts/generate.mjs --get-config`；未配置时由使用者提供自己的 **88API Key**，按随附插件的 `SKILL.md` 配置。配置写入使用者电脑的 `~/.codex/88api-nano-banana-config.json`，不要放进压缩包。普通 Google Gemini API Key 不能直接替代这个 88API Key。

豆包使用 `doubao-seedream-5-0-pro-260628`。Windows 使用者可运行 `scripts/set-ark-api-key.ps1` 隐藏输入自己的火山方舟 Key；其他系统设置环境变量 `COMMUNITY_POSTER_ARK_API_KEY`。两套 Key 相互独立。可用以下不付费检查确认本机配置：

```text
node <skill目录>/vendor/88api-nano-banana/scripts/generate.mjs --self-test
python <skill目录>/scripts/doubao_generate.py --check
```

制作海报时提供本次活动文案和社区图片，在 Codex 中选择三种参考风格之一。若宿主没有弹窗选择工具，回复 1、2 或 3 即可。默认中文、英文各请求一张；生图请求可能产生费用。提示词和结果写入当前工作区的 `outputs/community-poster-editable/`，不会写回 skill 目录。

本包不含任何用户的 API Key 或旧任务历史。转交前核对 `THIRD_PARTY_NOTICES.md` 中的插件及参考图片权限。
