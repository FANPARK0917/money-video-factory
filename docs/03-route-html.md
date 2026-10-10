# 03 · HTML 路线：render(t) + 截图（生产环境在用）

> 这是经过 6 版迭代验证的成熟路线：省钱陷阱 v6 成片（30s，1920×1080）即用此路线生产。
> 优点：零构建、依赖少、不挑浏览器；缺点：截图 plumbing 要自己维护。

---

## 原理

```
index.html 暴露 window.render(t)
      │  t = 秒数，纯函数，无 rAF，无随机（随机数用 seeded）
      ▼
puppeteer 打开 file://index.html
      │  对每一帧：page.evaluate(`render(${t})`) → 截图
      ▼  30fps × 30s = 900 张 PNG
ffmpeg -framerate 30 -i frame_%04d.png → 无声视频
      │  + 音频轨道（见 06）
      ▼
成片 mp4（H.264 + AAC）
```

## 文件结构

```
video-v2/
├── html/
│   ├── index.html            # 核心：所有场景 + render(t)
│   ├── ZCOOLKuaiLe.ttf       # 站酷快乐体（@font-face 本地加载）
│   └── avatar_sticker.png    # IP 头像贴纸
└── shot.js                   # 截图脚本
```

## index.html 要点

```js
// 纯时间函数：给定 t（秒），摆好这一秒的全部画面
window.render = function(t) {
  // 1. 按 t 计算每个场景的局部进度（带 0.45s 转场重叠）
  // 2. 用 easing 函数驱动位移/缩放/透明度
  // 3. 所有文字绘制前先做 raw-progress 门控（raw > 0 才画），
  //    避免 easing  epsilon 导致"鬼影文字"
};
```

关键规范：

- **纯函数**：同样 t 必须输出同样画面。随机数用 seeded PRNG，不许用 `Math.random()`。
- **不用 rAF**：渲染由外部逐帧调用 `render(t)` 驱动，与浏览器刷新率解耦。
- **转场重叠 0.45s**：场景 A 的淡出和场景 B 的淡入有 0.45 秒重叠，衔接更顺。
- **字体**：`@font-face` 加载本地 `ZCOOLKuaiLe.ttf`（OFL，可商用），不用 Google Fonts（沙盒无外网，生产环境也可能抽风）。

## shot.js 要点

```js
// node shot.js test  → 渲染 5 张 QA 静帧
// node shot.js full  → 渲染全部 900 帧
// node shot.js range 12.0 18.5 → 只渲 12~18.5 秒（改局部时用）
```

- 用 puppeteer-core 驱动系统 Chromium，走 **`file://` 协议**（不经过 localhost，天然绕开 [05](05-browser-fix.md) 的拦截问题）
- 截图节奏：1920×1080 约 0.5s/帧，900 帧 ≈ 7~8 分钟
- 帧文件存 `/tmp` 以外的持久目录（`/tmp` 会被系统清理，见 [08](08-pitfalls.md)）

## ffmpeg 组装

```bash
# 视频
ffmpeg -framerate 30 -i frames/frame_%04d.png \
  -c:v libx264 -pix_fmt yuv420p -preset veryfast \
  silent.mp4

# 音频见 06，完成后合并
ffmpeg -i silent.mp4 -i final_audio.m4a \
  -c:v copy -c:a aac -shortest output.mp4
```

`-preset veryfast`：1080×1920 下 medium 预设约 1fps，veryfast 是实用选择。

---

## 什么时候选这条路线

- 机器浏览器环境不可控（比如只有新版 Chromium）
- 想零构建、最快开工
- 分镜以 2D 贴纸/排版动效为主，不需要真 3D
