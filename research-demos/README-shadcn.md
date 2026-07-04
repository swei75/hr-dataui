# shadcn/ui 调研笔记

> **调研时间**：2026-07-04
> **目的**：补全 ARCHITECTURE.md §2.3 的调研缺口，为 v1.3 视觉决策提供回溯材料
> **作者**：Claude (sub-agent)
> **数据来源**：
> - ui.shadcn.com/docs/theming（官方主题文档）
> - ui.shadcn.com/docs/components/base/typography（官方排版示例）
> - github.com/shadcn-ui/ui/apps/v4/registry/themes.ts（v4 默认 neutral 主题源码）
> - colorfyi.com/blog/shadcn-ui-color-customization（HSL 通道解释）
> - llmbestpractices.com/frontend/shadcn-theming（语义 token 实践）
> - 2026-03 Easton Blog / 2026-06 llmbestpractices（OKLCH 迁移资料）
> - 注：所有数值均为多源交叉验证，HSL/OKLCH 默认值来自 v4 registry 源码

---

## 1. 概览

**shadcn/ui 不是传统组件库**——它是 shadcn（Vercel 前工程师）2023 年发布的"复制粘贴式组件集合"：

- 不是 `npm install shadcn-ui`
- 是 `npx shadcn@latest add button`，把组件源码直接拷到你的 `components/ui/` 目录
- 底层依赖：**Tailwind CSS + Radix UI primitives**（无障碍键盘/焦点/ARIA 由 Radix 处理）
- 视觉由 **CSS 变量 + Tailwind utility** 组合，主题切换改 `:root` 一个文件即可

> 这意味着：**你拥有组件源码，可以改任何一行**——这是和 MUI / Ant Design 最本质的区别。

---

## 2. 设计理念

### 2.1 复制粘贴模式 vs npm 依赖

| 维度 | shadcn/ui | 传统组件库（MUI / Ant Design） |
|---|---|---|
| 集成方式 | 源码拷到你的目录 | `npm install` |
| 体积 | 0（按需添加） | 全量打包（~100KB+） |
| 定制能力 | 完全可控（你拥有源码） | 通过 theme/props 受限 |
| 升级路径 | 手动同步（Git diff） | `npm update` |
| 学习曲线 | 中（要懂 Tailwind + Radix） | 低到中 |
| 适合谁 | 想要"专业风 + 自己掌控"的项目 | 快速原型 / 标准化产品 |

### 2.2 设计哲学（shadcn 本人原话提炼）

- **"Beautiful defaults, full control"**——默认值已经好看，但你随时可以改
- **语义 token 优先**——不是 `--primary-500` 这种色阶 token，而是 `--primary` 这种角色 token
- **Composition over configuration**——组件由小片段组合，而非一个巨型 prop 列表
- **无障碍先行**——Radix 提供 WAI-ARIA 完整支持，键盘导航/焦点环/屏幕阅读器都内置

### 2.3 为什么 v1.3 调研它

- shanjinki 没有结构化的设计 token，全是 hardcoded 颜色
- 我们要做"专业风"，需要一套**可继承、可覆盖**的 token 系统
- shadcn 的 CSS variable 命名思路和我们 §6 ADR-007 的 "4 级 tone + 12-col grid" 完美契合

---

## 3. 颜色系统

### 3.1 v4 默认 neutral 主题（OKLCH 格式）

从 `shadcn-ui/ui/apps/v4/registry/themes.ts` 直接抄：

```css
:root {
  --background:        oklch(1 0 0);          /* 纯白 */
  --foreground:        oklch(0.145 0 0);      /* 近黑 #18181b-ish */
  --card:              oklch(1 0 0);
  --card-foreground:   oklch(0.145 0 0);
  --popover:           oklch(1 0 0);
  --popover-foreground:oklch(0.145 0 0);
  --primary:           oklch(0.205 0 0);      /* 主色默认 = 近黑 */
  --primary-foreground:oklch(0.985 0 0);     /* 主色上的文字 = 近白 */
  --secondary:         oklch(0.97 0 0);      /* 浅灰 */
  --secondary-foreground:oklch(0.205 0 0);
  --muted:             oklch(0.97 0 0);
  --muted-foreground:  oklch(0.556 0 0);     /* 灰 */
  --accent:            oklch(0.97 0 0);
  --accent-foreground: oklch(0.205 0 0);
  --destructive:       oklch(0.577 0.245 27.325);  /* 红 */
  --destructive-foreground: oklch(0.985 0 0);
  --border:            oklch(0.922 0 0);
  --input:             oklch(0.922 0 0);
  --ring:              oklch(0.708 0 0);
  --radius:            0.625rem;             /* 10px, 旧版 v3 是 0.5rem = 8px */
}
```

### 3.2 旧版 v3 默认主题（HSL 通道格式，更易理解）

```css
:root {
  --background:        0 0% 100%;            /* 纯白 */
  --foreground:        222.2 84% 4.9%;       /* hsl(222.2, 84%, 4.9%) ≈ #0A0A0F */
  --primary:           222.2 47.4% 11.2%;    /* 近黑偏蓝 */
  --primary-foreground:210 40% 98%;
  --secondary:         210 40% 96.1%;        /* 浅蓝灰 */
  --muted:             210 40% 96.1%;
  --muted-foreground:  215.4 16.3% 46.9%;
  --accent:            210 40% 96.1%;
  --destructive:       0 84.2% 60.2%;        /* 红 */
  --border:            214.3 31.8% 91.4%;
  --input:             214.3 31.8% 91.4%;
  --ring:              222.2 84% 4.9%;
  --radius:            0.5rem;               /* 8px */
}
```

> **HSL 通道存储的小心机**：存的是 `222.2 84% 4.9%`（三段），不是完整 `hsl(...)`。
> 这样 Tailwind 可以合成 opacity：`hsl(var(--primary) / 0.5)` → 透明 50% 的主色。

### 3.3 主色 hex

**shadcn 默认主色不是"鲜艳蓝"，而是** `oklch(0.205 0 0)` ≈ **`#0F0F11`**（**近黑**）。
所有"primary button"长这样：**黑底白字**。非常简洁。

> 这点和 Linear 形成对比——Linear 用 `#5E6AD2` 紫色作为唯一彩色强调。
> shadcn 的"无色"哲学："颜色由用户品牌定义，库本身不强制色彩。"

### 3.4 中性色阶

shadcn **没有显式的 50-900 色阶**——只有 `background / foreground / muted / muted-foreground / border / input` 6 个语义层。
这是**和 Tailwind 默认调色板的关键差异**：

| 维度 | shadcn | Tailwind 默认 |
|---|---|---|
| 调色板 | 语义（6 层） | 色阶（zinc-50 ~ zinc-950） |
| 适用场景 | 组件内统一 | 设计稿 / utility 引用 |
| 改主题难度 | 改 1 个文件 | 改 n 个 utility class |

### 3.5 CSS variable 命名约定

**核心规则**：每个角色有 2 个 token
- `--{role}`：背景色（surface）
- `--{role}-foreground`：在该 surface 上的文字/图标色

**为什么这样设计**：
1. **可访问性自动保证**——`bg-primary` 永远配 `text-primary-foreground`，对比度由库设计者保证
2. **暗色模式自动**——`.dark` 块只需覆盖这些变量，组件代码零改动
3. **品牌替换简单**——把 `--primary` 改成你品牌的 OKLCH，全站主色随之变

**完整 token 清单**：

| Variable | 用途 |
|---|---|
| `--background` / `--foreground` | 页面背景 + 默认文本 |
| `--card` / `--card-foreground` | 卡片 surface |
| `--popover` / `--popover-foreground` | 弹层 surface |
| `--primary` / `--primary-foreground` | 主按钮/主行动 |
| `--secondary` / `--secondary-foreground` | 次按钮 |
| `--muted` / `--muted-foreground` | 弱化/禁用态 |
| `--accent` / `--accent-foreground` | hover/强调态 |
| `--destructive` / `--destructive-foreground` | 危险/删除 |
| `--border` | 默认边框 |
| `--input` | 表单输入边框 |
| `--ring` | focus ring |
| `--chart-1` ~ `--chart-5` | 数据可视化 5 色 |

### 3.6 图表调色板（chart-1 ~ chart-5）

shadcn v4 neutral 主题默认 5 色（来自 `themes.ts`）：

```css
--chart-1: oklch(0.809 0.105 251.813);   /* 浅蓝 */
--chart-2: oklch(0.623 0.214 259.815);   /* 中蓝 */
--chart-3: oklch(0.546 0.245 262.881);   /* 深蓝 */
--chart-4: oklch(0.488 0.243 264.376);   /* 更深蓝 */
--chart-5: oklch(0.424 0.199 265.638);   /* 最深蓝 */
```

> **重点**：默认是**单色相渐变**（全是蓝色，从浅到深），
> 不是 Tailwind 默认那种"红橙黄绿青蓝紫"彩虹色——更克制、更专业。

---

## 4. 字体系统

### 4.1 默认字体栈

shadcn 默认用 **Inter**（通过 `@fontsource-variable/inter` 引入）：
```css
font-family: 'Inter Variable', sans-serif;
```

可选替代（来自 `preset/presets.ts`）：
- **Geist**（Vercel 自家字体，Nova preset 默认）
- **Figtree**（Maia preset）
- **JetBrains Mono**（Lyra preset，单 mono 主题）
- **Noto Sans + Playfair Display**（Sera preset，衬线+无衬线搭配）

### 4.2 中文支持

shadcn 官方**没有内置中文 fallback**——社区方案是改 `tailwind.config.js`：
```js
fontFamily: {
  sans: ['Inter', '"PingFang SC"', '"Microsoft YaHei"', 'sans-serif'],
}
```

### 4.3 排版 utility 范式（来自官方 Typography 示例）

shadcn **不在组件里 hardcode 字号**——所有排版靠 Tailwind utility：

```tsx
<h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight text-balance">
  {/* 36px / 800 / -0.025em（Tailwind 默认 tracking-tight） */}
</h1>
<h2 className="mt-10 scroll-m-20 border-b pb-2 text-3xl font-semibold tracking-tight">
  {/* 30px / 600 / -0.025em */}
</h2>
<p className="text-xl leading-7 text-muted-foreground">
  {/* 20px / 1.75 行高 / muted 灰 */}
</p>
<small className="text-sm leading-none font-medium">
  {/* 14px / 1.0 / 500 */}
</small>
```

**排版节奏（Tailwind 默认尺度）**：
- `text-xs` 12px
- `text-sm` 14px（**默认正文**）
- `text-base` 16px
- `text-lg` 18px
- `text-xl` 20px（**副标题常用**）
- `text-2xl` 24px
- `text-3xl` 30px
- `text-4xl` 36px（**H1 常用**）
- `text-5xl` 48px
- `text-6xl` 60px

> **结论**：shadcn 没有"完整排版系统"（没有 role→size 的强映射），靠 utility class 按需取用。

---

## 5. 间距节奏

shadcn **不强制间距尺度**——沿用 Tailwind 默认：
- 基础单位：**0.25rem = 4px**
- 完整尺度：`0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, ...`（对应 `p-1`, `p-2`, ..., `p-24`）
- 实际项目常用：`p-2` (8px), `p-4` (16px), `p-6` (24px), `p-8` (32px)

**可通过 theme override 改默认间距尺度**：
```css
:root {
  --spacing: 0.2rem;   /* 改成 0.2rem = 3.2px 基础单位 */
}
```

---

## 6. 圆角规范

| 版本 | `--radius` 默认值 | 对应 px |
|---|---|---|
| v3 (HSL) | `0.5rem` | **8px** |
| v4 (OKLCH) | `0.625rem` | **10px** |

> 注：v3 文档中也有写 `--radius: 0.5rem` 的"标准"配置，但 v4 registry 默认偏大。

**组件级覆盖**：
```css
.rounded-sm { border-radius: calc(var(--radius) - 4px); }  /* 6px / 4px */
.rounded-md { border-radius: calc(var(--radius) - 2px); }  /* 8px / 6px */
.rounded-lg { border-radius: var(--radius);                /* 8px / 10px */
```

---

## 7. 阴影系统

shadcn **默认几乎不用阴影**——靠**border + surface 提亮**做层级：

```css
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / .05);    /* 仅极轻提示 */
--shadow:    0 1px 3px 0 rgb(0 0 0 / .08);    /* hover 时偶尔用 */
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / .07);  /* popover/dialog 偶尔用 */
```

> **设计哲学**："shadows should be subtle. Use borders more than shadows."

实际项目中：
- Card：`border` + `bg-card`，**0 阴影**
- Popover/Dialog：极轻 `shadow-md` 暗示浮层
- Hover 状态：边框颜色加深（`border → border-strong`），不上阴影

---

## 8. 整体印象（3 个形容词）

1. **克制**（restrained）——近黑主色、无装饰阴影、字号克制
2. **可组合**（composable）——CSS variable + Tailwind utility，按需取用
3. **可继承**（ownable）——你不是"用 shadcn"，你是"用 shadcn 拷过来的代码"

---

## 9. 与 hr-dataui v1.3 的对照

### 9.1 我们目前怎么做的（v1.3 `templates/base.py`）

```css
:root {
  --bg:#fafafa;       /* zinc-50 */
  --surface:#ffffff;  /* white */
  --surface-2:#f4f4f5;/* zinc-100 */
  --border:#e4e4e7;   /* zinc-200 */
  --text:#18181b;     /* zinc-900 */
  --text-muted:#52525b; /* zinc-600 */
  --primary:#4f46e5;  /* indigo-600 —— 鲜艳蓝 */
  --primary-light:#eef2ff;
  --primary-hover:#4338ca;
  --success:#10b981;  /* 绿 */
  --warning:#f59e0b;  /* 黄 */
  --danger:#ef4444;   /* 红 */
  --radius:12px;       /* 12px —— 比 shadcn 大 */
}
```

### 9.2 借鉴：值得学 shadcn 的 3 个具体做法

#### ✅ 借鉴 1：`--primary` / `--primary-foreground` 双 token 模式

**shadcn 做法**：
```css
--primary: 222.2 47.4% 11.2%;     /* 主色背景 */
--primary-foreground: 210 40% 98%; /* 主色上的文字 */
```

**我们的现状**：
```css
--primary: #4f46e5;
--primary-light: #eef2ff;   /* 浅版，但用在哪没明确 */
--primary-hover: #4338ca;
```

**改进方向**（不立即改，记录在 §10 后续）：
- 把 `--primary-light` 改名 `--primary-foreground-bg`（或 `--primary-soft`）
- 把 `--primary-hover` 改名 `--primary-active`
- 用 semantic 命名，而非按"颜色深度"命名

> ⚠️ **注意**：CLAUDE.md §9 写"改文档同步改代码"——这个改进必须先经用户批准。

#### ✅ 借鉴 2：HSL 通道存储 + alpha 合成

**shadcn 做法**（v3）：
```css
--primary: 222.2 47.4% 11.2%;   /* 不带 hsl() */
background-color: hsl(var(--primary) / 0.5);  /* 调用时合成透明度 */
```

**我们的现状**：直接存 hex，无法做透明合成。

**如果未来需要"主色 20% 透明背景"**——只能新增 `--primary-20` 这种 token，
无法 `rgba(var(--primary-rgb), 0.2)` 这样按需合成。

**改进方向**：v2.0 时考虑迁移到 OKLCH（v4 已用）或 HSL 通道（v3）。
**当前阻塞**：v1.3 已在用户审批的范围内，**不重做**。

#### ✅ 借鉴 3：图表调色板用"单色相渐变"

**shadcn 做法**：chart-1 ~ chart-5 全部是蓝色（hsl 251~265），只是 L（明度）不同。

**我们的现状**：v1.3 viz 用 `tone-blue/orange/green/purple/cyan/red` 6 个**完全不同的色相**。

```
.bar-row-fill.tone-orange{background:var(--orange)}  /* #f97316 */
.bar-row-fill.tone-green{background:var(--success)}  /* #10b981 */
.bar-row-fill.tone-purple{background:var(--purple)}  /* #8b5cf6 */
.bar-row-fill.tone-cyan{background:var(--cyan)}      /* #06b6d4 */
```

> 这其实**符合 shadcn "新派"做法**（chart-1~5 单色相），但我们是 HR 多模块场景，
> 不同模块需要**语义区分**（人事=绿、培训=紫），所以"彩虹"反而是合理选择。
>
> **保留 v1.3 多色相决策**——但记录："如果未来某个模块要扩展 5+ 子分类，
> 改用 shadcn 单色相渐变方案"。

### 9.3 不适合：shadcn 的 3 个"我们做不到"的特性

#### ❌ 不适合 1：Tailwind 依赖

shadcn 的 CSS variable 通过 Tailwind utility `bg-primary` 暴露。
我们自研 CSS（ADR-004），**完全没有 Tailwind**——每个 utility 都要手写 class。

**结论**：shadcn 的"token + utility class"模式我们只能学 token，utility 这层没法复用。

#### ❌ 不适合 2：Radix UI 无障碍层

shadcn 的 Dialog / Dropdown / Popover 等交互组件用 Radix UI 提供键盘/焦点/ARIA。
我们没有交互（ADR-009 钻取 YAGNI），**不需要**这层。

#### ❌ 不适合 3：HSL/OKLCH 默认值需要 Tailwind 配置

shadcn 的 HSL 通道要 `hsl(var(--primary) / alpha)` 配合 Tailwind 的 `<alpha-value>` 才有效。
我们手写 CSS，可以直接用 hex——没必要走 HSL 通道再合成的弯路。

### 9.4 中性评估：shadcn 对 v1.3 的净贡献

| 项 | 借鉴价值 | 实施难度 | 当前优先级 |
|---|---|---|---|
| name/foreground 双 token | ⭐⭐⭐ | 🟢 低（重命名） | 🟡 待 v2.0 评估 |
| HSL 通道存储 | ⭐⭐ | 🟡 中（CSS 全面改写） | 🟢 低 |
| 单色相图表渐变 | ⭐ | 🟢 低（仅 1 个 viz 改） | 🟢 低 |
| 极简阴影 | ⭐⭐⭐ | 🟢 低（已在做） | ✅ v1.3 已采用 |

**核心结论**：shadcn 真正影响 v1.3 的是"**克制的视觉哲学**"（近黑主色 + 无装饰阴影），
而非它的 token 实现细节——后者借鉴但**不复制**。

---

## 10. 后续追踪

- **v2.0 候选改进**：token 命名规范化（`primary`/`primary-foreground`/`primary-soft`）
- **不进 v1.4 的原因**：v1.3 用户刚评审通过，重命名 = 引入新风险（CLAUDE.md §7）
- **未来调研方向**：shadcn v4 完整 preset 系统（Nova/Vega/Maia 等 6 个风格）的选型决策

---

## 11. 来源

| 文档 | URL | 用于 |
|---|---|---|
| Theming 官方文档 | https://ui.shadcn.com/docs/theming | §3 / §6 / §7 |
| Tailwind Colors 转换 | https://ui.shadcn.com/colors | §3.2 |
| v4 themes.ts 源码 | https://github.com/shadcn-ui/ui/blob/main/apps/v4/registry/themes.ts | §3.1 默认值 |
| Typography 官方示例 | https://ui.shadcn.com/docs/components/base/typography | §4.3 |
| ColorFYI 解析 | https://colorfyi.com/blog/shadcn-ui-color-customization | §3.2 HSL 通道 |
| llmbestpractices theming | https://llmbestpractices.com/frontend/shadcn-theming | §3.5/§3.6 |
| Easton Blog OKLCH 迁移 | https://eastondev.com/blog/en/posts/dev/20260326-shadcn-ui-theme-customization/ | §3.1 OKLCH |
| v4 config 源码 | https://github.com/shadcn-ui/ui/blob/main/apps/v4/registry/config.ts | §4.1 字体预设 |