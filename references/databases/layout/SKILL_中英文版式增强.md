---
name: community-service-layout-design
description: Use this skill to design, evaluate, or revise the information layout of community-service posters by consulting the bundled community-service layout database. Apply it when the task involves community notices, public services, health guidance, emergency alerts, policy/rights information, activities, wayfinding, or similar public-information posters and Codex needs to check missing facts, build L1-L4 information hierarchy, select a layout pattern, place information modules, or evaluate readability. Do not use it as a visual-style database or to invent missing factual information.
---

# Community Service Information Layout Design

## Purpose

Use the community-service information layout database to convert raw service information into a clear, accurate, scannable poster layout.

Treat the database as a **layout decision knowledge base**, not as a template gallery.

The core process is:

`input facts -> completeness check -> information hierarchy -> reading path -> layout retrieval -> case validation -> layout blueprint -> readability check -> iteration`

Prioritize:

1. factual accuracy,
2. information completeness,
3. hierarchy and action clarity,
4. reading efficiency,
5. layout suitability,
6. visual quality.

Never sacrifice factual accuracy for visual effect.

---

## Required database

Use the bundled spreadsheet:

`references/社区服务信息版式数据库_最终增强版_完整填写.xlsx`

If the spreadsheet is stored elsewhere inside the skill folder, locate the file by name before proceeding.

The workbook contains four sheets:

- `具体版案例`
- `抽象版案例`
- `字段说明`
- `下拉选项`

The two case sheets use the same field structure so they can be compared directly.

Use:

- **抽象版案例** to select transferable layout structures.
- **具体版案例** to validate whether a structure works for a real information task.
- **字段说明** to understand field semantics and entry rules.
- **下拉选项** to preserve the database vocabulary when classifying a new task.

Do not copy example dates, organizations, contacts, prices, locations, or other factual content from the database into a new user task.

---

# Database model

The case database is organized into eight logical modules.

## 1. 案例基础

Use these fields to identify and understand a case:

- 案例ID
- 案例图片
- 案例名称
- 图片文件名（唯一）
- 案例类型
- 信息类型
- 服务主题
- 原文标题
- 发布机构
- 发布日期
- 目标受众
- 传播目标
- 语言
- 画布规格

Use this module for context and filtering. Do not let theme similarity override a better structural match.

---

## 2. 必需字段与缺失

Use these fields before any layout decision:

- 原始文案摘要
- 已包含关键字段
- 缺失关键字段
- 缺失等级
- 能否直接生成
- 需确认的问题
- 信息时效性
- 紧急程度

This module is a hard gate.

### Missing-information policy

Classify missing information as:

- `无缺失`
- `非关键缺失`
- `关键缺失`

Apply these rules:

```text
IF 关键事实缺失
THEN 不生成正式成品
AND 输出需确认的问题
AND 等待用户补充

IF 只有非关键缺失
THEN 可以继续做版式草案
BUT 不得虚构事实
AND 对未知内容使用明确占位或说明

IF 无缺失
THEN 进入信息层级分析
```

Treat the following as critical when required by the task:

- date/time
- location
- service eligibility
- fee/price
- action or registration method
- contact information
- official organization
- emergency instructions
- policy amount or policy condition

Never invent these fields.

---

## 3. 信息层级

Use these fields to determine visual priority:

- 信息量
- 信息分区/组数量
- 信息层级数量
- L1 核心识别层
- L2 关键行动层
- L3 补充说明层
- L4 来源联系层
- 层级清晰度

### L1-L4 model

#### L1 核心识别层

Answer:

`这是什么？`

Typical content:

- event/service name
- emergency type
- main notice
- main topic

L1 must be identifiable at first glance.

#### L2 关键行动层

Answer:

`居民下一步应该做什么？`

Typical content:

- date/time
- location
- registration
- immediate action
- target group
- service access

L2 must be easy to scan and act on.

#### L3 补充说明层

Answer:

`还需要理解哪些条件和细节？`

Typical content:

- service items
- rules
- steps
- conditions
- notes
- warnings

#### L4 来源联系层

Answer:

`从哪里确认、联系或继续操作？`

Typical content:

- organization
- phone
- QR code
- URL
- source
- version/date

### Hierarchy rule

Do not give all information equal visual weight.

Prefer:

`L1 > L2 > L3 > L4`

unless the task is an emergency, in which case immediate-action information in L2 may need equal or higher visual prominence than a descriptive title.

---

## 4. 版式结构

Use these fields to decide the structure:

- 阅读路径
- 一级版式类型
- 二级版式特征
- 构图方向
- 视觉焦点位置
- 核心信息逻辑
- 信息组织方式
- 信息叙事顺序
- 行动指令
- 是否含流程步骤
- 步骤数
- 标题位置
- 主视觉位置
- 核心信息位置
- 辅助信息位置
- CTA/联系方式位置
- 是否分栏
- 是否卡片化
- 是否编号
- 是否使用图标
- 是否使用色块强调

The database currently uses stable first-level layout categories such as:

- 单列聚焦型
- 分栏型
- 模块网格型
- 流程清单型
- 图文组合型
- 留白型
- 非对称型
- 分区型
- 导视地图型
- 混合模块型

Use the database vocabulary instead of inventing a new top-level category when an existing category fits.

---

## 5. 图文与空间

Use these fields to refine information placement:

- 图文比例
- 图文关系
- 强调方式
- 对齐方式
- 留白程度
- 信息密度
- 版式关键词

Important rule:

The image should support the information structure. Do not let decoration obstruct dates, locations, actions, contacts, or warnings.

---

## 6. 阅读评价

Use these fields as quality evidence:

- 字号可读性
- 色彩对比度
- 扫读效率
- 无障碍表现
- 综合评分
- 主要优点/可借鉴点
- 主要问题/局限/不适用场景

Do not choose a case only because its overall score is high.

First confirm structural suitability, then use these ratings to choose among suitable cases.

---

## 7. 适用与 Skill

Use these fields for retrieval and decision rules:

- 适用信息类型/场景
- 推荐使用条件
- 可转化为Skill的规则
- Skill标签

These are the most important fields for translating database knowledge into execution.

Treat `推荐使用条件` and `可转化为Skill的规则` as decision support, not absolute laws.

---

## 8. 来源与维护

Use these fields for traceability:

- 来源平台/机构
- 来源类型
- 来源链接或路径
- 版权与使用状态
- 采集人
- 采集日期
- 审核状态
- 备注

Prefer cases whose `审核状态` is reliable.

If a case is marked `需复核`, use its layout analysis but do not trust unresolved factual details without verification.

---

# Chinese and English layout rules

The final poster may be produced as either a Chinese version or an English version. Preserve the **same factual meaning and L1-L4 hierarchy**, but do not force the two languages into identical line breaks, text-box widths, or typographic proportions.

Treat language as a layout variable.

## Core bilingual principle

```text
same facts
+ same hierarchy
+ same action priority
!= identical typography
```

The Chinese and English versions should feel like the same information system, but each version must be typeset according to the reading habits and spatial characteristics of its language.

Do not solve bilingual adaptation by mechanically translating text into the same boxes.

---

## Chinese poster typography

Chinese text has relatively uniform square character widths and can tolerate compact modular composition, but dense blocks quickly become visually heavy.

For the Chinese version:

- Prefer clear visual grouping over long continuous paragraphs.
- Break long text into short clauses, labels, bullets, or modules when possible.
- Keep L1 and L2 concise. Avoid using full explanatory sentences as large display text.
- Chinese headings may use tighter line breaks than English, but avoid awkward single-character orphan lines.
- Keep punctuation attached to the relevant phrase; do not begin a line with closing punctuation.
- For dates, times, addresses, phone numbers, and service conditions, use consistent formatting throughout one poster.
- Use spacing, weight, size, alignment, and blocks to create hierarchy instead of inserting excessive manual spaces.
- Avoid compressing characters horizontally to fit a narrow box.
- For older audiences or emergency information, increase font size and line spacing and reduce decorative text treatments.

Recommended Chinese information behavior:

```text
L1: short topic / event / warning
L2: time + place + action + eligibility
L3: grouped explanation / steps / notes
L4: organization + phone + QR + source
```

---

## English poster typography

English uses words with highly variable lengths, visible inter-word spaces, ascenders/descenders, and stronger dependence on phrase-level line breaks. The English version usually needs more flexible text-box widths and more attention to line length.

For the English version:

### 1. Prefer left alignment for information-heavy content

Default to:

- left aligned,
- ragged right,
- consistent left edges.

Centered alignment is acceptable for short L1 titles or very short invitations, but avoid centering long instructions, schedules, addresses, or multi-line service details.

Avoid full justification for ordinary poster body copy because it can create uneven word spacing.

### 2. Break lines by phrase, not by visual convenience

Do not split a meaningful phrase when a better line break is available.

Prefer:

```text
Free Community
Health Screening
```

over:

```text
Free Community Health
Screening
```

when the second break weakens the phrase structure.

Keep together where possible:

- dates,
- time ranges,
- street names,
- phone numbers,
- short action phrases,
- article + noun combinations,
- preposition + short object when separation harms comprehension.

### 3. Avoid isolated short words

Avoid leaving a single short word on the last line of a heading or paragraph when it can be rewrapped naturally.

Especially avoid orphaned:

- `a`
- `an`
- `the`
- `to`
- `of`
- `for`
- `and`
- `or`

Do not force awkward tracking or scaling merely to eliminate an orphan.

### 4. Control capitalization

Use capitalization intentionally.

Recommended:

- **Title Case** for short event or service titles when appropriate.
- **Sentence case** for instructions, explanations, warnings, and service details.
- **ALL CAPS** only for very short labels, alerts, or category markers.

Do not use long ALL-CAPS paragraphs. They reduce word-shape recognition and scanning efficiency.

### 5. Keep body text readable

For English body copy:

- use sufficient line spacing,
- avoid overly tight tracking,
- avoid condensed type for long instructions,
- maintain clear distinction between heading, subheading, body, label, and CTA.

English text often needs a slightly wider measure than equivalent Chinese text.

If a translated English block becomes much longer than the Chinese block, first:

1. rewrite it more concisely without changing facts,
2. split it into modules,
3. widen the text area,
4. reduce nonessential decoration,
5. only then consider modest type-size adjustment.

Do not reduce critical information to an unreadably small size just to preserve the Chinese geometry.

### 6. Use consistent English punctuation and data formats

Within one poster, keep formatting consistent for:

- date style,
- time style,
- address style,
- phone number grouping,
- units,
- ranges,
- capitalization,
- punctuation.

Do not mix multiple date conventions in one poster.

When the required audience or locale is known, follow that locale's convention. If it is not known, choose one clear convention and use it consistently.

### 7. Keep labels concise

English UI-like labels and information headers should usually be short:

- `Date`
- `Time`
- `Location`
- `Eligibility`
- `How to Join`
- `Contact`
- `Important`
- `What to Bring`

Use labels to improve scanability instead of repeating full explanatory sentences.

---

## Chinese vs English layout adaptation

When producing two separate language versions, use the following adaptation logic.

| Dimension | Chinese version | English version |
| --- | --- | --- |
| Text width | Can work in relatively compact blocks | Often needs wider blocks |
| Line break unit | Character/phrase aware | Word/phrase aware |
| Default body alignment | Left aligned or structured modules | Left aligned / ragged right |
| Centered text | Works for short display text | Use mainly for short titles |
| Long instructions | Break into short clauses/modules | Break into bullets/modules; avoid long centered copy |
| Heading scale | Can be very compact and bold | Allow more horizontal width; avoid forced squeezing |
| All caps | Not applicable | Use sparingly |
| Tracking | Usually controlled through normal CJK spacing | Avoid excessive positive/negative tracking |
| Orphans | Avoid single-character awkward lines | Avoid isolated short words |
| Information boxes | May be narrower | May need expansion or fewer columns |

The two versions may use different:

- line breaks,
- module widths,
- number of text lines,
- column proportions,
- title size,
- spacing,
- visual balance.

They should keep the same:

- factual content,
- information priority,
- L1-L4 assignment,
- required action,
- critical CTA visibility,
- overall layout family unless the translation makes that family unsuitable.

---

## Language-specific layout decision

After Step 4 builds the L1-L4 hierarchy, run a language adaptation check.

```text
IF language = Chinese
THEN optimize for compact grouping, clear CJK hierarchy, and short modular phrases

IF language = English
THEN optimize for phrase-level line breaks, wider text measures, left alignment, and word-based scanning

IF both Chinese and English versions are required
THEN create two layout blueprints from the same hierarchy
AND allow typography and module geometry to adapt independently
```

Do not treat the English version as a direct text replacement inside the Chinese layout.

---

## Translation and content-preservation rules

When converting between Chinese and English:

- preserve facts exactly,
- preserve numbers exactly unless unit conversion is explicitly required,
- preserve names and official terms accurately,
- do not add promotional claims,
- do not omit restrictions, eligibility, warnings, or exceptions,
- do not translate QR codes, phone numbers, URLs, codes, or identifiers,
- keep action language explicit.

If an official English name is unavailable, do not invent an authoritative official translation. Use a clearly neutral descriptive translation or ask for confirmation when the name is legally or institutionally important.

For emergency, policy, legal, medical, fee, and eligibility information, prioritize semantic accuracy over stylistic fluency.

---

## Bilingual quality gate

Before finalizing either language version, check:

### Chinese version

- no dense uninterrupted paragraph blocks when modularization is possible,
- no awkward single-character line,
- date/time/contact formats are consistent,
- L1/L2 remain visually dominant,
- important text is not compressed to fit.

### English version

- no awkward word or phrase breaks,
- no isolated short final-line word when avoidable,
- no long centered body copy,
- no long ALL-CAPS copy,
- no excessive tracking or horizontal compression,
- line length and leading remain readable,
- date/time/address formatting is internally consistent.

### Cross-language consistency

- same facts,
- same L1-L4 hierarchy,
- same action priority,
- same required warnings and restrictions,
- same CTA prominence,
- no information added or lost during translation.

If one language fails readability, adapt its layout independently rather than forcing visual symmetry.

# Workflow

Follow this sequence for every community-service poster information-layout task.

## Step 1. Parse the user input

Extract only information explicitly provided by the user or trusted source.

Create an internal brief containing:

```text
信息类型:
服务主题:
原文标题:
发布机构:
发布日期:
目标受众:
传播目标:
语言:
画布规格:

核心事实:
- 时间:
- 地点:
- 服务对象:
- 服务内容:
- 行动方式:
- 联系方式:
- 费用/资格:
- 注意事项:
```

Do not invent missing values.

---

## Step 2. Run the completeness gate

Compare the input with the database fields:

- 已包含关键字段
- 缺失关键字段
- 缺失等级
- 能否直接生成
- 需确认的问题

Output one of:

```text
A. 可以直接生成
B. 需确认后生成
C. 不能生成
```

If the result is B or C, ask only for the missing facts that materially affect the layout or correctness.

Do not ask the user to decide visual details that the skill can infer from the database.

---

## Step 3. Classify the information task

Determine:

- 信息类型
- 信息时效性
- 紧急程度
- 目标受众
- 传播目标
- 信息量

Use the vocabulary in `下拉选项`.

When information is ambiguous, prefer the classification that best reflects the user's required action rather than the visual appearance.

Example:

- “停水通知” -> notification / urgent service information
- “免费义诊报名” -> public service / participation
- “暴雨避险” -> emergency / immediate action
- “社区活动招募” -> participation / registration

---

## Step 4. Build L1-L4 information hierarchy

Assign every information item to one of four layers:

```text
L1 = first-glance identity
L2 = action / time / place / participation
L3 = explanation / conditions / steps
L4 = source / contact / organization
```

Then determine:

- 信息分区/组数量
- 信息层级数量
- 核心信息逻辑

Examples:

```text
公告型:
事件 -> 时间 -> 影响范围 -> 行动 -> 联系方式

服务型:
服务是什么 -> 服务对象 -> 服务内容 -> 时间地点 -> 参与方式 -> 联系方式

应急型:
风险 -> 立即行动 -> 禁止行为 -> 避险地点 -> 紧急联系

流程型:
目标 -> Step 1 -> Step 2 -> Step 3 -> 材料/条件 -> 联系方式
```

Do not proceed to layout selection until the hierarchy is stable.

---

## Step 5. Determine the reading path

Choose a dominant reading path based on information relationships:

- 从上到下
- Z形
- F形
- 中心向外
- 网格扫描
- 跳跃式
- 路径导向

General guidance:

```text
IF information is sequential
THEN prefer 从上到下 / F形 / 流程路径

IF several same-level modules exist
THEN prefer 网格扫描

IF two strong information anchors exist
THEN consider Z形 / 对角结构

IF one central topic branches to several related points
THEN consider 中心向外

IF the task includes map/location navigation
THEN prefer 路径导向
```

---

## Step 6. Retrieve abstract layout candidates first

Read `抽象版案例`.

Filter in this order:

1. 信息量
2. 信息层级数量
3. 阅读路径
4. 一级版式类型
5. 二级版式特征
6. 信息组织方式
7. 构图方向
8. 适用信息类型/场景
9. 推荐使用条件
10. 主要问题/局限/不适用场景

Exclude a candidate if its limitations conflict with the current task.

Keep 1-3 strong candidates.

### Selection logic

Prefer structural fit over topic similarity.

For example:

```text
IF 4+ same-level information modules
THEN search 模块网格型 / 卡片结构

IF medium information volume + single dominant topic + clear hierarchy
THEN search 单列聚焦型

IF two major information groups must be compared or separated
THEN search 分栏型

IF the task has ordered steps or multi-day schedule
THEN search 流程清单型

IF main image and information must jointly carry meaning
THEN search 图文组合型

IF information is limited and hierarchy should feel calm
THEN search 留白型

IF route, service point, or location is the core task
THEN search 导视地图型
```

---

## Step 7. Validate with concrete cases

Read `具体版案例`.

Find examples similar in:

- 信息类型
- 服务主题
- 目标受众
- 传播目标
- 信息量
- 信息层级数量
- 阅读路径
- 一级版式类型
- 适用信息类型/场景

Use concrete cases to answer:

- Has this structure worked in a real information task?
- Where were L1-L4 placed?
- How were time/location/action/contact highlighted?
- Was the information density acceptable?
- What problems or limitations were observed?
- Which part is worth borrowing?

Do not copy the concrete case's factual content or visual identity.

Borrow structure, not facts.

---

## Step 8. Produce the layout blueprint

Before generating the final poster, produce an explicit layout plan.

Use this format:

```text
## Layout Blueprint

信息类型:
信息量:
信息层级:
阅读路径:
推荐一级版式:
推荐二级结构:

L1:
- 内容:
- 位置:
- 强调方式:

L2:
- 内容:
- 位置:
- 强调方式:

L3:
- 内容:
- 位置:
- 组织方式:

L4:
- 内容:
- 位置:

主视觉:
- 位置:
- 与文字关系:

版式结构:
- 分栏:
- 卡片化:
- 编号:
- 图标:
- 色块强调:

图文比例:
对齐方式:
留白程度:
信息密度:
CTA位置:

参考抽象案例:
参考具体案例:
```

If the task is going directly to image generation or design implementation, use this blueprint as the layout constraint.

---

## Step 9. Apply quality gates

Check all of the following before finalizing.

### Accuracy gate

- no invented dates
- no invented locations
- no invented contacts
- no invented prices
- no invented eligibility conditions
- no modified official facts

### Completeness gate

Confirm all critical user-provided facts appear in the layout.

### Hierarchy gate

Check:

- L1 is instantly identifiable
- L2 is easy to act on
- L3 does not overpower L1/L2
- L4 remains findable

### Scan gate

A viewer should be able to find:

- what
- when
- where
- what to do
- how to contact

without reading every sentence.

### Layout gate

Confirm:

- selected layout matches information volume
- reading path is intentional
- important information is not buried in decoration
- CTA/contact is findable
- whitespace is sufficient
- dense modules are grouped consistently

### Accessibility gate

Check:

- text size is readable
- contrast is sufficient
- information is not communicated by color alone
- older or high-risk audiences are not given excessively small or dense text

---

## Step 10. Iterate

If a quality gate fails, revise the specific module instead of rebuilding the entire poster.

Use this mapping:

```text
missing fact
-> return to Step 2

hierarchy confusion
-> return to Step 4

poor reading flow
-> return to Step 5

wrong layout family
-> return to Step 6

structure works but real-world fit is weak
-> return to Step 7

placement or density problem
-> return to Step 8
```

---

# Retrieval priority

When several database cases look relevant, rank them in this order:

1. no conflict with limitations,
2. matching information volume,
3. matching hierarchy depth,
4. matching reading path,
5. matching layout family,
6. matching information organization,
7. matching scenario / audience / goal,
8. better readability and scan scores,
9. clearer reusable rules.

Do not rank by visual attractiveness alone.

---

# Rule interpretation

Prefer explicit rule fields over inferred similarity.

Example:

```text
Database rule:
当存在3项以上平行日程时，按日期排序成等宽条目，每条只保留日期、名称、时间。

Apply:
IF current task contains 3+ same-level schedule items
THEN use a repeated schedule-row pattern
AND keep each row structurally consistent
AND avoid writing long paragraph descriptions inside each row
```

Another example:

```text
Database rule:
当核心主题必须第一眼识别且信息层级不超过4层时，调用单列聚焦型。

Apply:
IF one dominant topic + medium information volume + <=4 hierarchy levels
THEN shortlist 单列聚焦型
AND place the primary title in a dominant upper-area position
AND place execution information toward the lower portion
```

---

# Special handling by task type

## Emergency / high-risk information

Prioritize:

1. danger or alert state,
2. immediate action,
3. prohibited action,
4. safe location,
5. emergency contact.

Reduce decorative complexity.

Use high scan efficiency and strong separation of action modules.

## Service / healthcare information

Prioritize:

1. service name,
2. service audience,
3. service items,
4. time and location,
5. participation method,
6. contact.

Keep the tone clear and trustworthy.

## Notice / maintenance information

Prioritize:

1. what is happening,
2. when,
3. affected area,
4. what residents should do,
5. contact.

Use a stable, fast-scanning structure.

## Activity / recruitment information

Prioritize:

1. event identity,
2. date/location,
3. highlights,
4. participation conditions,
5. registration or CTA.

Allow stronger visual expression only after execution information remains clear.

## Guidance / process information

Prioritize:

1. goal,
2. ordered steps,
3. required materials or conditions,
4. warnings,
5. contact/source.

Use numbering, cards, lists, or flow structures when useful.

## Wayfinding / service-location information

Prioritize:

1. target location,
2. route or entry,
3. service points,
4. opening time,
5. contact.

Use path-oriented or map-oriented structure when location is the primary task.

---

# Output requirements

For an information-layout task, return at least:

1. information completeness result,
2. L1-L4 hierarchy,
3. selected layout family,
4. reading path,
5. layout blueprint,
6. database case references by case ID/name,
7. reasons for selection,
8. risks or limitations,
9. final validation result.

If generating the poster itself, preserve the same hierarchy in the output.

---

# Prohibited behavior

Do not:

- treat the database as a one-to-one template library,
- copy factual content from a reference case,
- invent missing facts,
- choose a layout only because it looks attractive,
- use visual-style labels as substitutes for layout structure,
- hide time/location/contact information inside complex imagery,
- reuse abstract example dates or text in a real poster,
- ignore a case's `主要问题/局限/不适用场景`,
- trust unresolved factual fields in a `需复核` case as authoritative.

---

# Maintenance rule

When new tested cases are added to the database:

1. keep case IDs unique,
2. keep image filenames unique,
3. preserve the same field vocabulary,
4. update `推荐使用条件`,
5. update `可转化为Skill的规则`,
6. record failures as limitations,
7. promote a rule only after it works across multiple relevant tests.

Treat the database as iterative design knowledge, not a fixed truth.
