#!/usr/bin/env python3
"""Minimal CLI to automate batch video rendering with ffmpeg."""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class VideoJob:
    images: list[str]
    output: str
    audio: str | None = None
    seconds_per_image: int = 3
    resolution: str = "1280x720"
    fps: int = 30

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "VideoJob":
        images = payload.get("images")
        output = payload.get("output")
        if not images or not isinstance(images, list):
            raise ValueError("Each job must include a non-empty 'images' list.")
        if not output or not isinstance(output, str):
            raise ValueError("Each job must include a non-empty 'output' path.")
        return cls(
            images=[str(path) for path in images],
            output=output,
            audio=payload.get("audio"),
            seconds_per_image=int(payload.get("seconds_per_image", 3)),
            resolution=str(payload.get("resolution", "1280x720")),
            fps=int(payload.get("fps", 30)),
        )


def load_jobs(config_path: str) -> list[VideoJob]:
    with Path(config_path).open("r", encoding="utf-8") as file:
        payload = json.load(file)
    job_payloads = payload.get("jobs") if isinstance(payload, dict) else payload
    if not isinstance(job_payloads, list) or not job_payloads:
        raise ValueError("Config must contain a non-empty list of jobs.")
    return [VideoJob.from_dict(item) for item in job_payloads]


def build_ffmpeg_command(job: VideoJob) -> list[str]:
    command: list[str] = ["ffmpeg", "-y"]

    for image in job.images:
        command.extend(["-loop", "1", "-t", str(job.seconds_per_image), "-i", image])

    if job.audio:
        command.extend(["-i", job.audio])

    if len(job.images) == 1:
        video_filter = f"[0:v]scale={job.resolution},fps={job.fps},format=yuv420p[v]"
    else:
        input_streams = "".join(f"[{index}:v]" for index in range(len(job.images)))
        video_filter = (
            f"{input_streams}concat=n={len(job.images)}:v=1:a=0,"
            f"scale={job.resolution},fps={job.fps},format=yuv420p[v]"
        )

    command.extend(["-filter_complex", video_filter, "-map", "[v]"])
    if job.audio:
        command.extend(["-map", f"{len(job.images)}:a", "-shortest", "-c:a", "aac"])

    command.append(job.output)
    return command


def run_job(job: VideoJob) -> None:
    command = build_ffmpeg_command(job)
    subprocess.run(command, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Automate batch video rendering with ffmpeg.")
    parser.add_argument(
        "--config",
        default="video_jobs.json",
        help="Path to a JSON config file with a 'jobs' list.",
    )
    args = parser.parse_args()

    for job in load_jobs(args.config):
        run_job(job)


if __name__ == "__main__":
    main()
