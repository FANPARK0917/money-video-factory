# 05 · 浏览器问题：Chromium 152 拦截 localhost（已解决）

> 现象：Remotion 4.0.534 渲染时访问 `http://localhost:3000`，被
> `ERR_BLOCKED_BY_LOCAL_NETWORK_ACCESS_CHECKS` 拦截。
> **结论先行**：换 Chrome for Testing **141.0.7390.122** 的 `chrome-headless-shell` 构建，一行命令解决。

---

## 背景

Chrome 142 起引入了 **Local Network Access（LNA）检查**：公网来源的页面访问本地网络（localhost/局域网）会被拦截。
Remotion 渲染时用无头浏览器访问自己起的 `localhost:3000`，在这版 Chromium 上正好撞枪口。

## 实测过程（2026-10-10）

在本机 Chromium 152（`/opt/meta-chromium/chrome`）上逐一实测，**全部无效**：

| 尝试 | 结果 |
|---|---|
| `--disable-web-security` | ❌ 依然拦截 |
| `--disable-features=LocalNetworkAccessChecks` | ❌ 关不掉（从二进制里抠出的 Finch 精确名称也试过） |
| `--no-proxy-server` | ❌ 依然拦截 |
| 上述组合 | ❌ 依然拦截 |
| wrapper 脚本注入 flag（`--browser-executable` 指向脚本） | ❌ 同上，flag 本身无效，脚本是死路 |

puppeteer 最小复现：`page.goto('http://localhost:3000')` 直接抛
`ERR_BLOCKED_BY_LOCAL_NETWORK_ACCESS_CHECKS`，确认是浏览器行为，与 Remotion 无关。

## 有效解法

LNA 检查是 Chrome **142** 才引入的，**141 没有**。用上一个大版本的无头构建即可绕开：

```bash
# 下载（Linux x64）
https://storage.googleapis.com/chrome-for-testing-public/141.0.7390.122/linux64/chrome-headless-shell-linux64.zip

# 使用
npx remotion render \
  --browser-executable=/path/to/chrome-headless-shell-linux64/chrome-headless-shell
# 或在代码里 Config.setBrowserExecutable(...)
```

**必须用 `chrome-headless-shell` 构建**，不能用完整版 Chrome 141：
Remotion 4 默认 `chromeMode: 'headless-shell'`，而完整版 Chrome 141 移除了旧 `--headless` 模式，会启动失败。

验证：`npx remotion still` 端到端输出正确 PNG。

## 备选：绕开 localhost

如果坚持用 HTML 路线（[03](03-route-html.md)），puppeteer 走 **`file://` 协议**直接打开本地 html，
全程不经过 localhost，天然免疫这个问题。这是生产环境当前在用的方式。

## 给后来人的建议

- 自己的电脑（Chrome 154+）跑 Remotion 同样会撞墙，**先装 141 headless-shell**，别在 flag 上浪费时间
- 关注 Remotion 官方对新版 Chrome LNA 的适配，未来可能不需要降级
