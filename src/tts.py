"""TTS client for DTF:FTL."""

from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

TTS_URL = "http://192.168.0.134:7849/speak"
TTS_TIMEOUT = 3600
MIN_WAV_SIZE_BYTES = 1000

CHARACTER_TTS_VOICES = {
    "forbin": "forbin",
}


class TTSUnavailable(RuntimeError):
    pass


def get_tts_voice() -> str:
    char = os.environ.get("CHARACTER", "forbin").lower()
    return CHARACTER_TTS_VOICES.get(char, "forbin")


def prepare_text_for_tts(text: str) -> str:
    text = text.strip()
    if not text.startswith("—"):
        text = "— " + text
    if not text.endswith("—"):
        text = text + " —"
    return text


def validate_wav_bytes(data: bytes) -> tuple[bool, str]:
    if not data:
        return (False, "empty response")
    if len(data) < MIN_WAV_SIZE_BYTES:
        return (False, f"too small ({len(data)} bytes)")
    if data[:4] != b"RIFF":
        return (False, "invalid WAV header")
    return (True, "")


def text_to_speech(text: str, output_path: Path, voice: str | None = None) -> tuple[bool, str]:
    voice = voice or get_tts_voice()
    prepared = prepare_text_for_tts(text)
    try:
        response = requests.post(
            TTS_URL,
            headers={"Content-Type": "application/json"},
            json={"text": prepared, "voice": voice, "timeout": 0},
            timeout=(10, TTS_TIMEOUT),
        )
    except Exception as exc:
        return (False, f"request failed: {exc}")

    if response.status_code != 200:
        return (False, f"HTTP {response.status_code}: {response.text[:100]}")

    valid, error = validate_wav_bytes(response.content)
    if not valid:
        return (False, error)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(response.content)
    return (True, "")


def _tts_worker(args: tuple[str, str, Path, str]) -> tuple[str, Path | None, str]:
    name, text, output_path, voice = args
    success, error = text_to_speech(text, output_path, voice=voice)
    return (name, output_path if success else None, error)


def text_to_speech_parallel(
    segments: list[tuple[str, str]],
    output_dir: Path,
    voice: str | None = None,
    max_workers: int = 12,
) -> tuple[list[Path], dict[str, str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    voice = voice or get_tts_voice()

    work_items = [(name, text, output_dir / f"{name}.wav", voice) for name, text in segments]
    results: dict[str, Path | None] = {}
    failures: dict[str, str] = {}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_tts_worker, item): item[0] for item in work_items}
        for future in as_completed(futures):
            name, path, error = future.result()
            results[name] = path
            if path is None:
                failures[name] = error

    wav_files = [results[name] for name, _ in segments if results.get(name)]
    return wav_files, failures
