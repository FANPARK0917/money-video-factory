# money-video-factory

自动化产出视频（vibe coding）的小工具：用一个 JSON 配置批量调用 `ffmpeg` 生成视频。

## 使用方式

1. 安装 `ffmpeg`
2. 新建 `video_jobs.json`：

```json
{
  "jobs": [
    {
      "images": ["assets/scene1.png", "assets/scene2.png"],
      "audio": "assets/music.mp3",
      "output": "dist/video.mp4",
      "seconds_per_image": 3,
      "resolution": "1280x720",
      "fps": 30
    }
  ]
}
```

3. 运行：

```bash
python video_factory.py --config video_jobs.json
```