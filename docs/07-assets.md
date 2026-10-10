# 07 · 素材清单：字体 / BGM / 头像

---

## 字体：站酷快乐体

- 文件：`ZCOOLKuaiLe-Regular.ttf`（OFL 协议，**可商用**）
- 来源：google/fonts GitHub 仓库
- 为什么选它：活泼不端正，简体字形全（含"复"等曾缺字形的坑已被验证）
- 加载方式：`@font-face` 本地加载，**永远不要**在渲染时依赖 Google Fonts CDN
  （沙盒无外网会失败；生产环境 CDN 抽风会拖慢渲染）

```css
@font-face {
  font-family: 'ZCOOLKuaiLe';
  src: url('ZCOOLKuaiLe.ttf') format('truetype');
}
```

## BGM

- 当前曲目：创作者自选（`assets/bgm.mp3`，189s，44100Hz 立体声）
- 使用规则：**固定用这一首**，直到创作者主动通知换曲；每期裁剪到与视频等长 + 结尾淡出（见 [06](06-audio.md)）
- 备选来源（无 BGM 时）：freepd.com 的 CC0 曲库（via SoundSafari GitHub 镜像，直接 curl mp3，无需登录/署名）
- 底线：不用廉价合成 BGM

## IP 头像

- 原始头像：创作者提供的个人 IP 头像（jpg）
- 视频内用法：白边圆框贴纸，从左下角偏上位置**弹出**（带 spring 动效，不是淡入）
- 规范：头像出现只在片尾收束，不抢戏

## 素材目录约定

```
assets/
├── bgm.mp3              # 当前 BGM
├── ZCOOLKuaiLe.ttf      # 字体
└── avatar_sticker.png   # 处理好的头像贴纸（白边圆框）
```

所有素材进版本库（Git LFS 如果文件大），渲染机上不依赖外部下载。
