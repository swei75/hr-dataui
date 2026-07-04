# Linear 调研笔记

> **调研时间**：2026-07-04
> **目的**：补全 ARCHITECTURE.md §2.3 的调研缺口，理解 v1.3 浅色专业风的"对比参照"
> **作者**：Claude (sub-agent)
> **数据来源**：
> - linear.app/now/behind-the-latest-design-refresh（官方设计哲学文章）
> - github.com/voltagent/awesome-design-md/blob/main/design-md/linear.app/DESIGN.md（社区整理的 DESIGN.md）
> - designmd.cc/benchmarks/linear（design tokens 解析，2026-05）
> - getdesign.md/design-md/linear.app/preview（design system 分析）
> - oh-my-design.kr/design-systems/linear.app（typography + color deep dive）
> - duply.ai/linear/design-md（DESIGN.md 复刻）
> - designsystems.one/design-systems/linear（设计系统背景）
> - pixicstudio.medium.com（motion tokens 来源）
> - 注：所有 hex 值均来自 DESIGN.md 或 designmd.cc 等结构化提取源

---

## 1. 概览

**Linear** 是 issue tracking / 项目管理工具（[linear.app](https://linear.app)），
由 Linear Method Inc. 2019 年发布。其设计系统**从未公开发布**——它**活在内核里**。

> Linear 的设计不是"文档驱动"，是"代码 + 创始人品味"驱动。
> 这点和 shadcn（开源社区 + shadcn 本人 GitHub）形成鲜明对比。

**核心影响力**：2021 年之后几乎所有 dev tool（Notion、Raycast、Vercel Dashboard、Arc Browser）
的视觉语言都受 Linear 影响——**单色相强调色 + 暗色优先 + Inter + 紧凑 padding**。

---

## 2. 设计理念

### 2.1 三大原则（来自官方 2024 redesign 文章）

1. **Visual hierarchy by relevance（按相关性排视觉权重）**
   - 主任务元素保持焦点
   - 导航/定位元素"退后"
   > "Not every element of the interface should carry equal visual weight."

2. **Restrained density（克制的信息密度）**
   - 信息密集（issue tracker 必须），但不令人 overwhelming
   - 通过**降低不必要元素的视觉强度**实现，而非简单缩小字号

3. **Calm over flashy（冷静优于炫技）**
   - 没有大色块、没有动画大爆发
   - 装饰元素（彩色 team icon 背景、装饰性边框）逐步被移除
   - 强调 "engineered, not just designed"

### 2.2 工程文化驱动设计

Linear 创始团队是工程师 + 设计师 + CEO 三角结构（来自 designsystems.one 报道）。
设计语言被工程文化塑造：

- **键盘优先**：所有操作可用 `Cmd+K` 调命令面板完成
- **速度感**：所有交互 100-200ms 必须完成，超出视为"卡顿"
- **inline diff motion**：代码差异动画直接走 GPU
- **muted neutral palette**：整个界面几乎不用颜色（除强调色）
- **typographic restraint**：一个 Inter Variable + 一个显示字重 + 一个 mono

> **核心洞察**：Linear 的设计哲学是**"删减比增加更难"**——所有元素都要证明存在的必要。

### 2.3 为什么 v1.3 调研它

- 我们要"专业风"，Linear 的"克制 + 单色相强调"是参考
- 我们 4 级 tone（blue/orange/green/purple/cyan）学的是 shadcn 多 viz 调色板
- 但 Linear 教我们的是**"少即是多"**——能用 1 种颜色就别用 4 种
- v1.3 视觉太"花"时，可回头参考 Linear 的克制

---

## 3. 颜色系统

### 3.1 暗色 canvas 三层（来自 designmd.cc）

```
#08090A   marketing/hero 背景（最深）
#0F1011   面板背景（panel bg）
#191A1B   提亮表面（elevated surfaces，弹层/卡片）
```

> **Linear 几乎所有界面都是这三个色**——通过 1-2 个色阶的差做层级，
> 不依赖阴影、border 颜色对比。

### 3.2 文字三层

```
#F7F8F8   主文字（亮白）
#B4B8BE / #8A8F98   次要文字（中性灰）
#62666D   弱化文字（placeholder/metadata）
```

> 文字色阶非常"紧"——主文字几乎是纯白，差异在 L（明度），不在 H（色相）。

### 3.3 唯一彩色强调：Linear Violet

```css
--accent:         #5E6AD2    /* 主强调色，Linear Violet/Lavender-blue */
--accent-bright:  #7170FF    /* hover/active 态（更亮） */
--accent-link:    #828FFF    /* 链接/可点击文字 */
```

> **Linear 的整本色彩书就这一个紫色**——其他都是灰阶。
> 这个紫色用于：
> - 品牌 mark
> - focus ring（键盘聚焦时）
> - 唯一的主 CTA per band（不是每屏都有）
> - 链接强调

### 3.4 中性色阶（暗色专用）

来自 oh-my-design.kr 拆解：

```
Background layers:   #08090A → #0F1011 → #191A1B
Border hairlines:    rgba(255,255,255,0.05) ~ rgba(255,255,255,0.08)
Text layers:         #F7F8F8 → #B4B8BE → #62666D
```

> **重点**：border 用半透明白（`rgba(255,255,255,0.05-0.08)`），
> 而**不是 hardcoded 灰色**——这样在不同 surface 上都"融入"而不"切线"。

### 3.5 浅色主题（也存在但不是默认）

来自 duply.ai 整理的 DESIGN.md 复刻：

```
canvas:        #FFFFFF 或 #FBFBFB
canvas-tint:   #F7F7F8   （微妙灰背景）
surface:       #FFFFFF   （卡片）
surface-tint:  #F4F4F5   （hover/嵌套）
border:        #E5E5E5 ~ #EBEBEB   （1px hairline）
text:          #0F1011
text-muted:    #62666D
accent:        #5E6AD2   （同一个紫色，跨主题通用）
```

> Linear 的**强调色跨 light/dark 主题保持不变**（都是 `#5E6AD2`），
> 调整的只是背景和文字——这是设计成熟度的体现。

### 3.6 我们的对比

| 维度 | Linear | v1.3 我们 |
|---|---|---|
| 主色 | `#5E6AD2` 紫 | `#4F46E5` 蓝（indigo-600） |
| 强调色数量 | **1**（仅紫） | **8**（蓝/橙/绿/紫/青/红/粉/黄） |
| 主色饱和度 | 中（lavender） | 高（indigo） |
| 暗色背景 | `#08090A` | 不支持（浅色专业风） |
| 边框 | `rgba(255,255,255,0.05-0.08)` 半透明 | `#E4E4E7` 实色 |

> **结论**：v1.3 和 Linear 在色彩哲学上是**相反方向**——
> 我们浅色 + 多色相 vs Linear 暗色 + 单色相。这是有意为之（HR 月报 vs 开发者工具）。

---

## 4. 字体系统

### 4.1 字体家族

Linear 用 **3 种字体**（非常克制）：

| 字体 | 角色 |
|---|---|
| **Inter Variable** | 99% UI 文字 |
| **Berkeley Mono** | 代码、键盘快捷键、terminal 帧 |
| **Tiempos Headline** | 极少数编辑性衬线瞬间（marketing 页） |

> **绝大多数项目用 Inter Variable 一个字体就够**。
> Berkeley Mono 只在显示键盘快捷键 `Cmd+K` / `G then P` 等时出现。

### 4.2 OpenType 特性

```css
font-feature-settings: "cv01", "ss03";
```

- `cv01`：单层 `a`（不是双层）
- `ss03`：几何化字形（数字 `0` 切平而非椭圆）

> 这两个 feature 让 Inter 看起来"更工程化"——视觉细节影响巨大。

### 4.3 字重（非常克制）

Linear 用 **3 个字重**：

```
400 / Regular   正文
510 / Linear's signature weight   默认强调（介于 regular 和 medium 之间）
590 / Semibold   显示/标题
680 / Bold   仅极少数 editorial 标题
```

> **510 是 Linear 的"签名"**——比 regular 略重，但不到 medium 的"喊叫感"。
> 我们 v1.3 用 `font-weight: 500/600/700`——可以**借鉴 510** 提升微妙感。

### 4.4 字号尺度（完整）

来自 duply.ai 整理（DESIGN.md 复刻）：

```
display-xl:    56px / 590 / -0.022em   hero 标题
display-lg:    48px / 590 / -0.022em   section 标题
display-md:    40px / 590 / -0.022em   sub-section
display-sm:    32px / 590 / -0.022em   feature 块
serif-accent:  48px / 400 / -0.010em   Tiempos 衬线瞬间
title-lg:      24px / 590 / -0.012em   卡片/feature 标题
title-md:      20px / 510 / -0.012em   子标题
title-sm:      17px / 510 / -0.012em   列表标题
body-lg:       18px / 400 / -1         大段正文
body-md:       15px / 400 / 1.6        **默认正文**（我们用 14px）
body-sm:       13px / 400 / 1.5        caption
tag:           12px / 400 / 1          tags / metadata
code:          13px / 400 / 1.5        Berkeley Mono
button:        15px / 510 / 1          按钮标签
nav-link:      14px / 510 / 1.4        顶部导航
```

> **关键观察**：
> - Linear 默认正文 **15px**，我们用 **14px**——可考虑未来微调到 15px
> - 大字号负 letter-spacing（`-0.022em`）让标题紧凑有力
> - 行高 1.6（body）vs 1.5（small）——非常细的区分

### 4.5 与 v1.3 的对比

| 维度 | Linear | v1.3 我们 |
|---|---|---|
| 正文字号 | 15px | 14px |
| 默认字重 | 400 / 510 | 400 / 500 / 600 / 700 |
| 标题字重 | 590 | 600 |
| 标题 letter-spacing | -0.022em（大字号） | -0.01em ~ -0.02em |
| 主字体 | Inter Variable | -apple-system + Inter fallback |

---

## 5. 间距节奏

### 5.1 完整间距尺度（来自 getdesign.md / designmd.cc）

```
4px   xxs   图标-文字间距、微调对齐
8px   xs    紧凑组件内 padding
12px  sm    按钮/input 内 padding
16px  md    元素间标准间距、小容器 padding
24px  lg    卡片内主 padding
32px  xl    大块卡片间距、section 内
48px  xxl   section 间距
96px  section   marketing 页 section 间距
160px section-lg  marketing 页大间距
```

> **基础单位 4px**，主节奏 8/12/16/24/32。
> 比 shadcn/Tailwind 的 4px 基础更"密集"——少用 64/80/96 这种大跳跃。

### 5.2 marketing vs product 节奏不同

- **marketing 页**：96-160px 大间距（呼吸感）
- **产品内**：24px 卡片 padding，8-12px 元素 gap（信息密度）

> **我们的 HR 月报场景**：相当于 Linear 的"产品内"——紧凑为主。
> v1.3 用 14-16px 卡片 padding，8-10px 元素 gap——**已对齐 Linear 节奏**。

---

## 6. 圆角规范

来自 getdesign.md 整理：

```
4px   xs   极小元素（chip、tag）
6px   sm   小元素
8px   md   **按钮、input 默认**
12px  lg   卡片
16px  xl   大卡片/弹层
```

> **按钮默认 8px，不是 pill**——Linear 明确反对 pill 按钮。
> "White primary buttons (`{component.button-primary}`) at compact 36px,
> radius `{rounded.md}` (8px) — never pill."

**对比 v1.3**：
- 按钮/输入：v1.3 用 `--radius-sm: 8px` ✅
- 卡片：v1.3 用 `--radius: 12px` ✅
- 徽章/pill：v1.3 用 `--radius-pill: 9999px` ⚠️ Linear 不推荐

> **可改进**：v1.3 的 `.badge` 在 hero 里用 pill 圆角——Linear 风格应该是 8px 而非 pill。
> 但 HR 报告里 pill badge 也很常见，**保留**作为合理例外。

---

## 7. 阴影系统

### 7.1 Linear 几乎不用阴影

来自 designmd.cc：
> "Subtle Depth: Depth is created with `1px` borders and inset shadows, not prominent box shadows."

**Linear 的浮层表示方法**：
1. **1px border**（`#2A2E33` 暗色 / `#E5E5E5` 浅色）
2. **背景提亮**（surface 提一档：`#0F1011` → `#191A1B`）
3. **inset shadow**（极轻的内阴影，仅在 input focus 时偶尔用）

### 7.2 与 v1.3 对比

```css
/* v1.3 我们的阴影 */
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / .05);   /* hover 极轻提示 */
--shadow:    0 1px 3px 0 rgb(0 0 0 / .08);   /* 偶尔 */
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / .07); /* 模块卡片默认 */
```

> **v1.3 阴影比 Linear 略重**——`shadow-sm` 用于所有卡片默认。
> **改进方向**：可考虑把模块卡片的 shadow 去掉，只用 border（更 Linear 风格）。
> **当前阻塞**：完全无阴影会让卡片"漂浮"——visual hierarchy 需要。
> **保留决策**：v1.3 用 `--shadow-sm` 已是最小化，**不进一步减**。

---

## 8. 动效原则

### 8.1 4 种 easing curves（来自 Medium 文章 + Linear motion tokens）

```css
--ease-enter:    cubic-bezier(0.0, 0.0, 0.2, 1.0);  /* 进入，减速 */
--ease-exit:     cubic-bezier(0.4, 0.0, 1.0, 1.0);  /* 离开，加速 */
--ease-standard: cubic-bezier(0.4, 0.0, 0.2, 1.0);  /* 对称缓动 */
--ease-spring:   cubic-bezier(0.34, 1.56, 0.64, 1.0); /* 弹性 overshoot */
```

### 8.2 5 种 durations

```css
--duration-micro:    80ms;    /* color 变化 */
--duration-fast:     120ms;   /* hover/focus */
--duration-standard: 200ms;   /* 默认 */
--duration-moderate: 280ms;   /* 弹层打开 */
--duration-slow:     400ms;   /* 大型 transition */
```

### 8.3 核心原则

> "**Exits should always be faster than entrances.**"
> 用户不需要"看"东西消失——出现 200ms，离开 120ms。

> "Color changes below 100ms feel instant. Above 150ms, a color shift starts to feel sluggish."

### 8.4 与 v1.3 对比

```css
/* v1.3 我们的 transition（templates/base.py） */
transition: width .6s cubic-bezier(.4,0,.2,1);    /* bar fill */
transition: all .15s ease;                         /* KPI 卡 hover */
transition: background .12s;                       /* donut legend hover */
```

> **Linear 的微交互原则我们已部分采用**：
> - hover 用 120-150ms ✅（Linear 推荐 120ms）
> - bar fill 用 600ms ⚠️（Linear 推荐 200ms 标准）
>
> **可改进**：bar fill 600ms 偏长，对月报静态场景其实可以更快（200-300ms）。
> **当前阻塞**：v1.3 已经让用户评审通过，**不重做**。

---

## 9. 整体印象（3 个形容词）

1. **安静**（quiet）——暗色 + 灰阶 + 1 个紫，几乎"无声"
2. **精密**（precise）——4px 基础、510 字重、80ms 颜色——所有数值精确
3. **工程化**（engineered）——feels built, not designed

---

## 10. 与 hr-dataui v1.3 的对照

### 10.1 我们目前怎么做的（v1.3 `templates/base.py`）

```css
/* 字体 */
font-family:-apple-system,BlinkMacSystemFont,"Inter","Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;
font-size:14px;line-height:1.55;
font-feature-settings:"cv02","cv03","cv11","ss01";

/* 主色（高饱和度） */
--primary:#4f46e5;        /* indigo-600, 鲜艳蓝 */
--primary-light:#eef2ff;
--primary-hover:#4338ca;

/* 多色相 viz 调色板 */
--purple:#8b5cf6; --orange:#f97316; --cyan:#06b6d4; --pink:#ec4899;

/* 圆角 */
--radius:12px; --radius-sm:8px; --radius-xs:4px; --radius-pill:9999px;
```

### 10.2 借鉴：值得学 Linear 的 3 个具体做法

#### ✅ 借鉴 1：Inter Variable + OpenType `cv01, ss03`（**已部分采用**）

**Linear 做法**：
```css
font-family: 'Inter Variable', sans-serif;
font-feature-settings: "cv01", "ss03";
```

**v1.3 现状**：
```css
font-family: -apple-system, BlinkMacSystemFont, "Inter", "PingFang SC", "Microsoft YaHei", sans-serif;
font-feature-settings: "cv02", "cv03", "cv11", "ss01";
```

> **差异**：
> 1. 我们用 system font 优先（避免网络请求 Inter）
> 2. 我们用的 feature 是 `cv02/cv03/cv11/ss01`，Linear 是 `cv01/ss03`
>
> **改进方向**：可以**额外**开启 `cv01` 和 `ss03`：
> ```css
> font-feature-settings: "cv01", "cv02", "cv03", "cv11", "ss01", "ss03";
> ```
> 多个 feature 可以共存。**这一改动零风险、低收益**，但能让我们视觉更接近 Linear。
> **下次小迭代可考虑**。

#### ✅ 借鉴 2：510 字重作为默认强调（值得借鉴但 v1.3 不改）

**Linear 做法**：默认强调用 510（介于 regular 和 medium 之间）——微妙但有力。

**v1.3 现状**：用 500/600/700 三档。Linear 的 510 在我们这里介于 500（medium）和 600（semibold）之间。

> **改进方向**：如果想再"克制"一点，KPI 数字 `font-weight: 700` 可改为 `font-weight: 600`；
> 但 700 的视觉冲击对 HR 月报 KPI 卡来说反而是优势。**保留 700**。

#### ✅ 借鉴 3：hairline 边框 + 半透明（值得借鉴但 v1.3 不改）

**Linear 暗色做法**：
```css
border: 1px solid rgba(255, 255, 255, 0.05);   /* 半透明白 */
```

**v1.3 现状**：
```css
--border: #e4e4e7;   /* 浅色主题下用实色 hex */
```

> **改进方向**：在浅色主题下也可以用半透明黑：
> ```css
> --border: rgba(0, 0, 0, 0.08);   /* 跨 surface 更柔和 */
> ```
> **评估**：当前 `#E4E4E7` 是 zinc-200，**已是非常接近的浅灰**——差异不大。
> **保留决策**：hex 在浅色场景更可控（可访问性工具直接读色），**不改成 rgba**。

### 10.3 不适合：Linear 的 1 个最关键"反例"

#### ❌ 不适合：暗色主题 vs 我们的浅色专业风

**Linear 默认暗色**——所有界面都是 `#08090A` 这种近黑底。
**v1.3 我们是浅色专业风**（ADR-007）——`#FAFAFA` 底 + 低饱和度蓝 `#4F46E5`。

**为什么不抄暗色**：
1. **场景冲突**：HR 月报 = 打印/邮件附件（白底黑字才是严肃文档），不是大屏演示
2. **打印友好性**：浅色主题打印友好，暗色主题打印 = 翻黑
3. **银行稳重感**：浅色 + 低饱和度蓝 = 银行/金融默认（参考 shanjinki Editorial Brief）
4. **已 ADR-007 明确决策**：暗色 → 否决（"演示好看但打印/邮件不友好"）

> **结论**：Linear 教我们的是**克制哲学**，不是暗色本身——
> 我们用浅色实现同样的"安静 + 精密"。

### 10.4 中性评估：Linear 对 v1.3 的净贡献

| 项 | 借鉴价值 | 实施难度 | 当前优先级 |
|---|---|---|---|
| Inter + OpenType features | ⭐⭐⭐ | 🟢 零风险（加 feature） | 🟡 v1.4 小迭代 |
| 510 字重 | ⭐⭐ | 🟡 需重新调 UI 重量 | 🟢 低（保留 700） |
| 半透明 hairline | ⭐ | 🟢 低 | 🟢 低（保留 hex） |
| 暗色主题 | ❌ 反例 | - | ❌ 明确否决 |
| 4px 间距节奏 | ⭐⭐⭐ | ✅ 已采用 | ✅ v1.3 已对齐 |
| 8px 按钮圆角 | ⭐⭐ | ✅ 已采用 | ✅ v1.3 已对齐 |

**核心结论**：Linear 真正影响 v1.3 的是"**克制 + 精密**"的哲学——
通过 4px 间距、8px 圆角、Inter 字体这些**数值纪律**实现，
而非暗色本身。

---

## 11. 后续追踪

- **v1.4 候选改进**：增加 `cv01, ss03` OpenType features（零风险）
- **不进的改进**：暗色主题（违反 ADR-007）
- **未来调研方向**：Linear 的命令面板（Cmd+K）交互模式——但我们不需要交互（ADR-009）

---

## 12. 来源

| 文档 | URL | 用于 |
|---|---|---|
| 官方 redesign 文章 | https://linear.app/now/behind-the-latest-design-refresh | §2.1 三大原则 |
| DESIGN.md 复刻（voltagent） | https://github.com/voltagent/awesome-design-md/blob/main/design-md/linear.app/DESIGN.md | §3-§6 全部 token |
| designmd.cc 解析 | https://designmd.cc/benchmarks/linear | §3.4-§3.5 边框/浅色 |
| getdesign.md 拆解 | https://getdesign.md/design-md/linear.app/preview | §4.4 / §5 / §6 完整数值 |
| oh-my-design typography | https://oh-my-design.kr/design-systems/linear.app | §4 Inter feature/字重 |
| duply.ai DESIGN.md | https://duply.ai/linear/design-md | §3.5 浅色主题 |
| designsystems.one 背景 | https://www.designsystems.one/design-systems/linear | §1 / §2.2 工程文化 |
| Motion tokens 文章 | https://pixicstudio.medium.com/.../linear-and-raycast-4fac298d5b9e | §8 easing/duration |
| designlang motion | https://www.designlang.app/gallery/linear-app | §8 补充 motion tokens |
| YPAI motion 系统 | https://ypai.ai/design/motion/ | §8 借鉴 Linear motion 实践 |