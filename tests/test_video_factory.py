import json
import tempfile
import unittest
from pathlib import Path

from video_factory import VideoJob, build_ffmpeg_command, load_jobs


class VideoFactoryTests(unittest.TestCase):
    def test_load_jobs_supports_jobs_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "jobs.json"
            config_path.write_text(
                json.dumps(
                    {
                        "jobs": [
                            {
                                "images": ["a.png", "b.png"],
                                "audio": "track.mp3",
                                "output": "result.mp4",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            jobs = load_jobs(str(config_path))

        self.assertEqual(1, len(jobs))
        self.assertEqual("result.mp4", jobs[0].output)

    def test_build_ffmpeg_command_for_multiple_images_and_audio(self) -> None:
        job = VideoJob(images=["a.png", "b.png"], audio="track.mp3", output="result.mp4")

        command = build_ffmpeg_command(job)

        self.assertIn("concat=n=2:v=1:a=0", " ".join(command))
        self.assertIn("-shortest", command)
        self.assertIn("result.mp4", command)

    def test_build_ffmpeg_command_single_image_without_audio(self) -> None:
        job = VideoJob(images=["a.png"], output="result.mp4")

        command = build_ffmpeg_command(job)

        self.assertIn("[0:v]scale=", " ".join(command))
        self.assertNotIn("-shortest", command)

    def test_load_jobs_rejects_empty_jobs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "jobs.json"
            config_path.write_text(json.dumps({"jobs": []}), encoding="utf-8")

            with self.assertRaises(ValueError):
                load_jobs(str(config_path))


if __name__ == "__main__":
    unittest.main()
