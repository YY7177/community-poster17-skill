"""Generate with the user's official Ark model and save the result locally."""
import argparse
import base64
import json
import mimetypes
import os
import re
import sys
from datetime import datetime
from importlib.metadata import version
from pathlib import Path
from uuid import uuid4

MODEL = "doubao-seedream-5-0-pro-260628"
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
KEY_VARIABLE = "COMMUNITY_POSTER_ARK_API_KEY"


def api_key():
    key = os.environ.get(KEY_VARIABLE, "").strip()
    if not key and sys.platform == "win32":
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as handle:
                key = str(winreg.QueryValueEx(handle, KEY_VARIABLE)[0]).strip()
        except (FileNotFoundError, OSError):
            pass
    return key


def reference(value):
    if value.startswith(("https://", "http://", "data:image/")):
        return value
    path = Path(value).resolve()
    if not path.is_file():
        raise ValueError(f"Reference image does not exist: {path}")
    if path.stat().st_size > 30 * 1024 * 1024:
        raise ValueError("Reference image exceeds 30 MB")
    mime = mimetypes.guess_type(str(path))[0]
    if mime not in {"image/png", "image/jpeg", "image/webp", "image/bmp", "image/tiff", "image/gif", "image/heic", "image/heif"}:
        raise ValueError("Unsupported reference image format")
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def image_extension(data):
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if data.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        return ".webp"
    raise ValueError("Response is not a recognized image; metadata is preserved")


def failure_details(exc):
    """Keep service diagnostics, without logging credentials or request headers."""
    details = {"error_type": type(exc).__name__, "http_status": getattr(exc, "status_code", None)}
    body = getattr(exc, "body", None)
    if isinstance(body, dict):
        error = body.get("error", body)
        if isinstance(error, dict):
            key = api_key()
            for field in ("code", "message", "request_id"):
                value = error.get(field)
                if isinstance(value, str):
                    if key:
                        value = value.replace(key, "[REDACTED]")
                    details[field] = re.sub(r"ark-[A-Za-z0-9_-]+", "[REDACTED]", value)
    return details


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt-file", type=Path)
    parser.add_argument("--image", action="append", default=[])
    parser.add_argument("--size", default="2K")
    parser.add_argument("--no-watermark", action="store_true", help="Disable the visible generated-image watermark when requested")
    parser.add_argument("--output-dir", type=Path, default=Path.cwd() / "outputs" / "doubao")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    from volcenginesdkarkruntime import Ark
    key = api_key()
    if args.check:
        print(json.dumps({"sdk_version": version("volcengine-python-sdk"), "api_key_configured": bool(key), "model": MODEL}, ensure_ascii=False))
        return 0
    if not args.prompt_file:
        parser.error("--prompt-file is required")
    prompt = args.prompt_file.read_text(encoding="utf-8-sig").strip()
    if not prompt:
        raise ValueError("Prompt must not be empty")
    if len(args.image) > 10:
        raise ValueError("This model accepts at most 10 reference images")
    if args.size not in {"1K", "1.5K", "2K"}:
        try:
            width, height = map(int, args.size.split("x"))
        except ValueError:
            raise ValueError("Size must be 1K, 1.5K, 2K, or WIDTHxHEIGHT") from None
        if min(width, height) <= 0 or not 921600 <= width * height <= 4624220 or not 1 / 16 <= width / height <= 16:
            raise ValueError("Size exceeds this model's pixel or aspect-ratio limits")
    watermark = not args.no_watermark
    request = dict(model=MODEL, prompt=prompt, response_format="url", size=args.size, stream=False, watermark=watermark)
    if args.image:
        request["image"] = [reference(value) for value in args.image]
    if args.dry_run:
        print(json.dumps({"dry_run": True, "model": MODEL, "size": args.size, "watermark": watermark, "reference_images": len(args.image), "api_key_configured": bool(key), "api_called": False}, ensure_ascii=False))
        return 0
    if not key:
        raise ValueError(f"{KEY_VARIABLE} is missing. Run scripts/set-ark-api-key.ps1 locally first.")
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid4().hex[:8]
    metadata_path = output_dir / f"{prefix}.json"
    with Ark(base_url=BASE_URL, api_key=key, timeout=300.0, max_retries=0) as client:
        response = client.images.generate(**request)
    metadata = {"model": MODEL, "prompt": prompt, "size": args.size, "watermark": watermark, "references": [str(Path(value).resolve()) if not value.startswith(("https://", "http://", "data:")) else "remote_or_inline_image" for value in args.image], "response": response.model_dump(mode="json"), "files": []}
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    if not response.data:
        raise ValueError(f"No image returned. Metadata: {metadata_path}")
    import httpx
    for index, item in enumerate(response.data, start=1):
        url = getattr(item, "url", None)
        encoded = getattr(item, "b64_json", None)
        if encoded:
            data = base64.b64decode(encoded)
        elif url:
            downloaded = httpx.get(url, timeout=120.0, follow_redirects=True)
            downloaded.raise_for_status()
            data = downloaded.content
        else:
            raise ValueError(f"No image data returned. Metadata: {metadata_path}")
        image_path = output_dir / f"{prefix}-{index}{image_extension(data)}"
        image_path.write_bytes(data)
        metadata["files"].append(str(image_path))
        metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"files": metadata["files"], "metadata": str(metadata_path), "model": MODEL}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
    except Exception as exc:
        print(json.dumps(failure_details(exc), ensure_ascii=False), file=sys.stderr)
        print("No automatic generation retry. Check output metadata if present.", file=sys.stderr)
        raise SystemExit(1)
