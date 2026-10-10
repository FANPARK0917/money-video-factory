# 04 · Remotion 路线：React 分镜（已解锁）

> Remotion 是 React 视频框架：写组件，它负责在无头浏览器里逐帧渲染、编码。
> 曾因 Chromium 152 拦截 localhost:3000 而不可用，**2026-10-10 已找到实测有效的解法**（见 [05](05-browser-fix.md)）。

---

## Remotion 到底在干什么

`npx remotion render` 背后：

1. Webpack 打包你的 React 组件
2. 起本地服务（localhost:3000）托管页面
3. 启动无头 Chromium，**逐帧**访问：第 N 帧就把播放器拨到第 N 帧，等画面稳定后截图
4. 截图流灌进 ffmpeg，编码 H.264；`<Audio>` 标签的音频一并混入

看出来了：底层就是 skill 说的"逐帧截图 + FFmpeg"，只是产品化了。
你不用写截图脚本、不用管编码参数，白嫖组件化、Studio 实时预览、`spring()`/`interpolate()` 动画函数。

## 与 HTML 路线的心智映射

| HTML 路线 | Remotion 路线 |
|---|---|
| `window.render(t)` | `useCurrentFrame()`（当前第几帧） |
| 手写 easing | `interpolate()` / `spring()` |
| shot.js 截图 | 内置渲染（`npx remotion render`） |
| 手动抽静帧 | `npx remotion still`（单帧，原生支持） |
| 改完重新截图看效果 | Remotion Studio（浏览器拖时间轴实时预览） |
| ffmpeg 手动混 BGM | `<Audio src={staticFile('bgm.mp3')}/>` |

## 项目结构（最小可用）

```
remotion/
├── src/
│   ├── index.ts          # 注册 Composition
│   ├── Video.tsx         # 总 Composition：<Sequence> 排每幕
│   └── scenes/
│       ├── Hook.tsx      # 0-4s 钩子
│       ├── Point1.tsx    # 每个点一幕
│       └── Outro.tsx     # 收束
└── public/
    ├── ZCOOLKuaiLe.ttf   # 本地字体（@font-face + staticFile()）
    └── bgm.mp3
```

```tsx
// 每幕 = 纯函数的 React 组件，frame 决定一切
export const Point1: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const x = interpolate(t, [0, 1], [200, 0], { easing: Easing.out(Easing.cubic) });
  // ... 按 t 摆画面，和 render(t) 一模一样的心智
};
```

## 字体：必须走本地

沙盒/无外网环境下 `@remotion/google-fonts` 会在渲染时失败。正确做法：

1. ttf 扔进 `public/`
2. CSS 里 `@font-face` + Remotion 的 `staticFile('ZCOOLKuaiLe.ttf')` 引用

## 渲染命令（含浏览器解法）

```bash
npx remotion render \
  --browser-executable=~/browsers/chrome-headless-shell-linux64/chrome-headless-shell

npx remotion still --frame=150  # 静帧 QA 用
```

浏览器二进制：Chrome for Testing **141.0.7390.122** 的 `chrome-headless-shell` 构建。
**必须用 headless-shell 版**：Remotion 4 默认 `chromeMode: 'headless-shell'`，
完整版 Chrome 141 移除了旧 `--headless`，会启动失败。下载地址：

```
https://storage.googleapis.com/chrome-for-testing-public/141.0.7390.122/linux64/chrome-headless-shell-linux64.zip
```

原理详见 [05](05-browser-fix.md)。

## 什么时候选这条路线

- 想 vibe 得最爽：AI 只写 React 分镜，脏活全交给 Remotion
- 需要频繁预览迭代（Studio 比截图循环快一个数量级）
- 团队协作：组件化分镜比单个大 html 好维护
