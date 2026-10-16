"""Assemble style-aware poster prompts locally; never call a paid API."""
import argparse
import hashlib
import json
from math import gcd
from pathlib import Path

SECTIONS = (
    ("reference", "参考图与场景依据"),
    ("title", "艺术标题与字形"),
    ("elements", "主题元素与视觉动线"),
    ("information", "关键信息组合"),
    ("content", "内容与行动呈现"),
    ("footer", "提示、条件与落款"),
    ("finish", "整体成图要求"),
)


def nonempty(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Non-empty text required: {label}")
    return value.strip()


def assemble(plan):
    """Input structure checks are not a review of model-generated images."""
    task_id = nonempty(plan.get("task_id"), "task_id")
    canvas = plan.get("canvas", {"width": 1200, "height": 1500})
    width, height = canvas.get("width"), canvas.get("height")
    if any(type(v) is not int or v <= 0 for v in (width, height)):
        raise ValueError("Canvas width and height must be positive integers")
    ratio = f"{width // gcd(width, height)}:{height // gcd(width, height)}"
    languages = plan.get("languages", ["zh", "en"])
    if not isinstance(languages, list) or not languages or any(v not in ("zh", "en") for v in languages):
        raise ValueError("languages must contain zh and/or en")
    if len(set(languages)) != len(languages):
        raise ValueError("languages contains duplicates")
    style = plan.get("style", {})
    style_name = nonempty(style.get("name"), "style.name")
    medium = nonempty(style.get("medium"), "style.medium")
    palette = nonempty(style.get("palette"), "style.palette")
    scene = nonempty(plan.get("visual_scene"), "visual_scene")
    elements = nonempty(plan.get("visual_elements"), "visual_elements")
    facts = plan.get("facts")
    if not isinstance(facts, list) or not facts:
        raise ValueError("facts must be a non-empty list")
    ids = set()
    for fact in facts:
        fact_id = nonempty(fact.get("id"), "facts.id")
        if fact_id in ids:
            raise ValueError(f"Duplicate fact id: {fact_id}")
        ids.add(fact_id)
        for language in languages:
            nonempty(fact.get(language), f"facts.{fact_id}.{language}")

    shared = f"风格：{style_name}。表现媒介：{medium}。配色：{palette}。"
    visual = (
        f"制作一张{ratio}竖版社区风格场景参考图，供下一阶段海报生成使用，精致细节。\n"
        f"{shared}\n参考图1只约束社区可见场景关系，参考图2只约束风格媒介，"
        "不要复制风格案例的文字、品牌或历史事实。\n"
        f"场景：{scene}\n主题元素：{elements}\n"
        "形成统一的材质、光线与色彩。允许调整构图和裁切，不凭空改变入口或道路连接。"
        "这是无文字的风格场景素材，不是完整海报，不制作标题、日期、正文、信息卡、Logo或二维码。"
        "不强制留出文字空区，不做贴墙或展架mockup。\n"
    )
    outputs = {
        "nano-banana-prompt.txt": visual,
        "nano-banana-prompts.json": json.dumps([visual], ensure_ascii=False, indent=2) + "\n",
    }
    designs = plan.get("poster_sections", {})
    headings = ["规格与视觉风格"] + [title for _, title in SECTIONS] + ["上图文字清单"]
    for language in languages:
        language_name = "中文" if language == "zh" else "英文（地点等专名可保留给定中文）"
        spec = (
            f"制作一张{ratio}竖版完整{language_name}社区海报，目标{width}×{height}像素。"
            f"{shared}图像、艺术字和正文在同一张图中完整设计，具有精致平面设计感。"
        )
        design = designs.get(language, {})
        bodies = [spec]
        bodies.extend(nonempty(design.get(key), f"poster_sections.{language}.{key}") for key, _ in SECTIONS)
        inventory = "\n".join(f"- {json.dumps(fact[language].strip(), ensure_ascii=False)}" for fact in facts)
        bodies.append(
            "以下文案全部进入同一张海报，保持事实与条件；设计指令中的重复提及不表示重复印字。"
            "不印本段标题、引号或字段ID，不自行添加报名、费用、机构、电话、时间或二维码。\n" + inventory
        )
        prompt = "\n\n".join(f"【{i} · {heading}】\n{body}" for i, (heading, body) in enumerate(zip(headings, bodies), 1))
        outputs[f"poster-prompt-{language}.txt"] = prompt + "\n"
    manifest = {
        "task_id": task_id,
        "requested_canvas": {"width": width, "height": height, "aspect": ratio},
        "languages": languages,
        "style": style_name,
        "section_order": headings,
        "generation_requests_planned": {"nano_banana": 1, "doubao": len(languages)},
        "paid_api_called": False,
        "content_review": "not_requested",
        "postprocessing": "none",
        "files": {name: hashlib.sha256(value.encode("utf-8")).hexdigest() for name, value in outputs.items()},
    }
    outputs["prompt-manifest.json"] = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    plan = json.loads(args.input.read_text(encoding="utf-8-sig"))
    outputs = assemble(plan)
    # Refuse every collision before writing any file.
    if not args.overwrite:
        for name in outputs:
            if (args.output_dir / name).exists():
                parser.error(f"Output exists: {name}; choose a new version or use --overwrite")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name, value in outputs.items():
        (args.output_dir / name).write_text(value, encoding="utf-8")
    print(json.dumps({"files": [str((args.output_dir / name).resolve()) for name in outputs], "api_called": False}, ensure_ascii=False))


if __name__ == "__main__":
    main()
