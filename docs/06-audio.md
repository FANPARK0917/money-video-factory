# 06 · 音频处理：BGM + 音效 + 24dB 大坑

> BGM 用创作者自选曲目（拒绝廉价合成 BGM）。
> 音效（"啵"、闷响）用 numpy 在时域合成、直接叠加。

---

## BGM 处理三步

```bash
# 1. 裁剪到与视频等长（例：30s）
ffmpeg -i bgm.mp3 -t 30 bgm_cut.mp3

# 2. 响度标准化 + 结尾 2s 淡出
ffmpeg -i bgm_cut.mp3 \
  -af "loudnorm,afade=t=out:st=28:d=2" \
  bgm_final.m4a
```

- BGM **必须**与视频等长，不许出现"视频播完了音乐还在响"或反之
- 结尾淡出 2s，避免戛然而止
- `loudnorm` 保证每期响度一致

## "啵"音效：numpy 时域叠加

数字/卡片弹出时的"啵"、"省"印章落下的闷响，用 numpy 合成短音效，
在**时域直接加到 BGM 波形上**，再一次性编码：

```python
import numpy as np

bgm, sr = load_audio("bgm_final.m4a")      # shape: (samples,)
sfx = synth_pop(sr, freq=600, dur=0.15)    # 合成 0.15s 的"啵"

out = bgm.copy()
pos = int(4.2 * sr)                        # 第 4.2 秒弹出
out[pos:pos+len(sfx)] += sfx * 0.8

peak = np.abs(out).max()
assert peak < 1.0, "削波了，先衰减"
write_audio("final_mix.m4a", out, sr)
```

实测：混音峰值 0.913，无削波，无需额外压限。

## ⚠️ 大坑：ffmpeg amix 会让 BGM 越放越大

**血的教训（v5，2026-10-10）**：用户反馈"前面没啥声音，后面最后那么大"。
实测 30 秒内响度爬升约 **24dB**。

原因：用 ffmpeg `amix` 混入 20 个短音效时，`amix` 会随着短输入流结束
**动态改变归一化除数**，导致 BGM 一路变大。

```bash
# ❌ 错误示范：不要这样混多路短音效
ffmpeg -i bgm.mp3 -i pop1.wav -i pop2.wav ... -filter_complex amix=inputs=21 out.mp3
```

**正确做法**：永远用上面的 numpy 时域叠加，一次编码。
`amix` 只适合路数固定、时长相同的少数输入。

## 交付前响度检查

把成片按每 2 秒一段算 RMS，画曲线：相邻段最大差值应在音乐自身动态范围内
（实测正常值约 4~5dB）。如果看到单调爬坡，回去查混音链路。
