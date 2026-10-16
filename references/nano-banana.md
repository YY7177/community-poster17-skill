# Nano Banana：中间风格场景图

从本 skill 根目录读取 `vendor/88api-nano-banana/skills/88api-nano-banana/SKILL.md`，执行同目录内 `vendor/88api-nano-banana/scripts/generate.mjs`。这是随包复制的 1.3.6 插件快照，不需要在宿主 Codex 另装插件。需要 Node.js 18+ 及每位使用者自己的 88API Key；配置保存在使用者的 `~/.codex/88api-nano-banana-config.json`，不随包转交。只接受能调用 88api.ai 图像模型的 88API Key，不能直接换成 Google API Key。

先运行 `--get-config`。有凭证就复用，没有按插件配置流程处理。尊重其保存的模型与复杂任务的模型选择规则；单次选择用 `--model`，不更改全局默认。当前Nano Banana只负责无最终正文的风格图，不承担精准海报文字排版。

完整中英文海报prompt先准备好，再提交一张中间图：

```text
node <本skill>/vendor/88api-nano-banana/scripts/generate.mjs --batch <本次>/prompts/nano-banana-prompts.json --image <社区原图> --image <所选风格参考图> --aspect 4:5 --resolution 2K --output-dir <本次>/visuals
```

`--aspect`随用户规格，默认4:5。图1为社区场景依据，图2只约束表现媒介；参考总量遵守插件20MB限制。候选风格不付费生成；两语共用一次结果。实际生成图才是后续豆包第一参考，不能把输入案例图冒充生成结果。

按插件要求查看并展示保存图片，再交接到豆包；不跑旧锚点/美观质量清单或付费返修。记录真实模型、结果路径与状态，不把中间图当最终中文/英文海报。

`[NO-AUTO-RETRY]`、超时或未知受理状态不自动重发或换模型；用户明确重试按插件规则仅新发一次。失败保留prompt并停止依赖阶段，不静默改为直接文生图。成功的已有风格图可在用户下一次修改中复用。
