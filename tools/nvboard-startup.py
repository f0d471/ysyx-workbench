#!/usr/bin/env python3
"""Compile the upstream NVBoard example and observe a bounded WSLg startup."""
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parent.parent
if Path(os.environ.get("NEMU_HOME", "")).resolve() != root / "nemu":
    raise RuntimeError("Use the YSYX WSL sandbox entrypoint")
if os.environ.get("SDL_VIDEODRIVER") != "x11" or not os.environ.get("DISPLAY"):
    raise RuntimeError("Use sandbox.ps1 -Action Run -Gui for this startup check")
subprocess.run(["make", "-C", root / "nvboard/example"], check=True, cwd=root)
example = root / "nvboard/example"
if not (example / "resource/picture.hex").is_file():
    raise RuntimeError("The upstream NVBoard picture resource is missing")
process = subprocess.Popen([example / "build/top"], cwd=example,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           text=True)
try:
    output, _ = process.communicate(timeout=5)
except subprocess.TimeoutExpired:
    process.terminate()
    try:
        output, _ = process.communicate(timeout=3)
    except subprocess.TimeoutExpired:
        process.kill()
        output, _ = process.communicate()
    print(output, end="", flush=True)
    if any(marker in output.lower() for marker in ("assertion", "get error", "file not found", "%warning")):
        raise RuntimeError("NVBoard reported an initialization error")
    print("NVBOARD_STARTED_5_SECONDS (bounded startup only; terminated by probe)")
else:
    print(output, end="", flush=True)
    raise RuntimeError(f"NVBoard exited before the observation ended: {process.returncode}")
