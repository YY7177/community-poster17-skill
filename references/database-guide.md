# 当前参考库：风格逐图卡与抽象版式卡

制作海报时只使用两套活跃资料：97 张风格原图对应的简明 Markdown 卡，以及按需使用的 25 张抽象版式图对应的 Markdown 卡。`theme` 库、layout 具体版、原始表格和旧索引保留供归档追溯，**不进入日常检索、阅读和构图**。活动主题与事实以用户本次资料为准。

| 用途 | 快速索引 | 阅读的卡片 | 必要时核对 |
| --- | --- | --- | --- |
| 视觉风格 | [style-raw-index.json](catalog/style-raw-index.json)、`scripts/style_shortlist.py` | `databases/style/cases/Sxx-Rxx.md` | 最终三个候选的 `databases/style/images/raw/` 原图；已有的 12 张详细卡可作补充 |
| 信息版式 | [layout-abstract-index.json](catalog/layout-abstract-index.json) | `databases/layout/abstract-cases/` 中与图片同名的 Markdown | 仅当卡片不足以判断细节时看对应抽象版原图 |

从本 skill 根目录运行：

```text
python scripts/style_shortlist.py --task-id TASK_ID --outputs OUTPUTS_ROOT
python scripts/catalog.py --library style-raw --query "纸感 插画" --limit 6
python scripts/catalog.py --library layout-abstract --query "非对称 留白" --limit 6
```

`catalog.py` 不指定 `--library` 时仅搜索上述两套活跃索引。`--query` 是文字检索，匹配排序不代表审美质量。旧的 `theme`、`layout`、`style` 索引仍可由维护者显式指定用于追溯，但制作海报时不使用。

## 读取与判断

1. 先按用户资料划分 L1 识别、L2 时间地点与参与、L3 活动项目和必要说明、L4 来源与联系；依据阅读路径压缩文字，不从参考图搬用事实。
2. 风格短名单先读至少四个家族的简明卡，再打开最终三个候选原图核对画面和适配性。尽量跨家族并避开近期重复。97 张卡记录了图片名称、所属家族、缩略图视觉速记、初筛备注、尺寸和图片路径；其中只有原有 12 张另有较详细分析。速记和初筛备注不能称作逐图高清复核。三张原图在 Codex 对话里逐张展示，配宿主三选一弹窗；不调用风格选择页脚本。
3. 需要构图启发时只读抽象版式卡，按当前信息量、图文关系与受众选择可迁移的组织方法，并将决定写入完整海报prompt。卡片保留源表的设计字段与图片链接；转换本身不代表图片经过新一轮视觉审核。可按需核对抽象版原图，不打开具体版案例。
4. 记录三张实际展示的风格图、是否查看原图、最终选择和借鉴点。旧案例中的日期、地点、机构、电话、二维码或专业建议都不是本次事实。无需为最终豆包成图执行旧版图片核验。

## 维护

`python scripts/build_reference_cards.py` 根据保留的风格清单、[视觉速记](databases/style/视觉速记.json)、风格原图和抽象版式旧索引重建两套简明卡及新索引；`--check` 检查它们是否与源文件一致。原始图片、旧详细卡、theme 文件、具体版文件与索引都不删除。新增风格图片时先补对应速记，再重建和检查。参考图的使用与转交权限须单独确认。
