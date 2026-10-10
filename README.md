# 🏭 Money Video Factory · 省钱短视频云端工厂

> 每天早上 6 点自动生产一条 40 秒内的省钱主题横屏短视频。
> 全流程代码化：AI 写分镜代码 → 逐帧渲染 → 质检 → 合成 → 交付，人只负责收成片。

这套仓库是**完整可复用的"代码做视频"工作流文档**：从方法论、两条渲染路线、工具清单，到 5 个真实踩过的坑。
无论你是创作者想自己搭，还是 AI 智能体想接单照做，都能直接用。

---

## 📖 文档导航

| 文档 | 内容 |
|---|---|
| [01 管线总览](docs/01-pipeline.md) | 7 个阶段：触发 → 调研 → 分镜 → 拍摄 → 质检 → 音频 → 交付 |
| [02 方法论](docs/02-method.md) | skill 工作流：三方案 → brief → 分镜 → 静帧 QA → 成片 |
| [03 HTML 路线](docs/03-route-html.md) | `render(t)` + puppeteer 截图 + ffmpeg（生产环境在用） |
| [04 Remotion 路线](docs/04-route-remotion.md) | React 分镜组件 + 官方渲染（已解锁） |
| [05 浏览器问题](docs/05-browser-fix.md) | Chromium 152 拦截 localhost 的实测结论与解法 |
| [06 音频处理](docs/06-audio.md) | BGM 等长/淡出、"啵"音效合成、amix 24dB 大坑 |
| [07 素材清单](docs/07-assets.md) | 字体、BGM、IP 头像的来源与规范 |
| [08 天坑清单](docs/08-pitfalls.md) | 5 个已交学费的坑 + 经验法则 |
| [09 AI 接单指南](docs/09-agent-guide.md) | **给 AI 智能体**：接到需求后一步一步怎么做 |
| [10 Brief 模板](docs/10-brief-template.md) | 分镜 brief 模板 + 真实示例 |

---

## ⚡ 30 秒看懂

```
每天 06:00 (cron)
   │  全网搜省钱技巧/坑钱套路，对照黑名单避开重复题材
   ▼
写分镜 brief（钩子 4s → 3~4 个点 → 收束 6s，总 ≤40s）
   │  纯时间函数 render(t)：第几秒 = 哪一帧画面
   ▼
puppeteer 逐帧截图（30fps）→ 静帧 QA → 转场 QA → 响度 QA
   │  BGM 截到等长 + 结尾淡出，numpy 叠加"啵"音效
   ▼
ffmpeg 合成 H.264 + AAC → 发附件 → 题材记入黑名单
```

## 🛠 核心工具（5 个就能开工）

| 工具 | 作用 |
|---|---|
| Node.js 18+ | 运行 Remotion / 截图脚本 |
| Remotion **或** HTML + puppeteer | 渲染引擎（二选一，见 03 / 04） |
| Chrome for Testing 141 headless-shell | 给 Remotion 用的浏览器（绕开新版拦截，见 05） |
| AI 写代码工具（Claude / Codex / 任意智能体） | 把 brief 写成可渲染的分镜代码 |
| FFmpeg | 组装视频、处理音频 |

素材：站酷快乐体（OFL 可商用）+ 自选 BGM + 个人 IP 头像，详见 [07](docs/07-assets.md)。

## 🎨 审美底线

- 不用廉价合成 BGM、僵硬端正的字体、莫名悬浮的数字、强广告感
- 偏好：活泼字体、错位/旋转/贴纸式排版、有层次的 2.5D 动效
- 每个数字必须有小票、算式或具体消费情境解释，不许凭空出现

## 🤖 给 AI 智能体的一句话

先读 [09 AI 接单指南](docs/09-agent-guide.md)，它规定了你接到"做一条视频"需求后的完整动作序列和交付检查清单。

---

*本项目由真人创作者 + AI 搭档实战打磨，2026-10。*
