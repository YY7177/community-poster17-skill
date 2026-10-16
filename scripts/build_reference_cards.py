"""Build concise, image-linked style and abstract-layout cards from existing inventories.

This is a metadata conversion. It does not claim a new visual review of every image.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "references"
STYLE = REF / "databases/style"
LAYOUT = REF / "databases/layout"
CATALOG = REF / "catalog"
STYLE_CASES = STYLE / "cases"
ABSTRACT_CASES = LAYOUT / "abstract-cases"
FAMILIES = {
    "S01": "摄影写实",
    "S02": "手绘肌理插画",
    "S03": "扁平图形插画",
    "S04": "立体造型与材质",
    "S05": "拼贴与混合媒介",
    "S06": "字体与抽象图形",
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_or_check(path, value, check):
    if check:
        if not path.is_file() or path.read_text(encoding="utf-8") != value:
            raise ValueError(f"missing or stale generated case: {path}")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8")


def style_rows():
    inventory = (STYLE / "素材全量清单.md").read_text(encoding="utf-8")
    visual_notes = json.loads((STYLE / "视觉速记.json").read_text(encoding="utf-8"))
    rows = []
    for line in inventory.splitlines():
        if not re.match(r"^\| S\d\d-R\d\d \|", line):
            continue
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) != 6:
            raise ValueError(f"unexpected style inventory row: {line[:100]}")
        image_id, filename, family_text, status, note, links = parts
        match = re.fullmatch(r"(S\d\d) → (S\d\d)", family_text)
        if not match:
            raise ValueError(f"unexpected family mapping: {family_text}")
        image = STYLE / "images/raw" / f"{image_id}.jpg"
        if not image.is_file():
            raise FileNotFoundError(image)
        with Image.open(image) as picture:
            width, height = picture.size
        detailed = re.search(r"cases/(S\d\d-C\d\d)\.md", links)
        rows.append({
            "id": image_id, "name": filename, "original_family": match[1],
            "family": match[2], "family_name": FAMILIES[match[2]], "status": status, "screening_note": note,
            "visual_note": visual_notes[image_id],
            "image": f"references/databases/style/images/raw/{image_id}.jpg",
            "card": f"references/databases/style/cases/{image_id}.md",
            "detailed_card": (f"references/databases/style/cases/{detailed[1]}.md" if detailed else None),
            "width": width, "height": height, "sha256": sha256(image),
        })
    raw_images = list((STYLE / "images/raw").glob("*.jpg"))
    if len(rows) != len(raw_images) or len({r["id"] for r in rows}) != len(rows):
        raise ValueError(f"inventory/image mismatch: {len(rows)} rows, {len(raw_images)} images")
    if set(visual_notes) != {row["id"] for row in rows}:
        raise ValueError("visual note IDs do not match style inventory")
    return rows


def style_card(row):
    detailed = (f"- 已有详细视觉卡：[{Path(row['detailed_card']).stem}]({Path(row['detailed_card']).name})\n"
                if row["detailed_card"] else "- 详细视觉分析：尚未建立；此卡只整理图片与现有初筛记录。\n")
    duplicate = "- 此文件与库中另一张图完全重复，选择时只保留一个。\n" if "重复文件" in row["status"] else ""
    return (f"# {row['id']} · {row['name']}\n\n"
            f"![{row['id']} 原图](../images/raw/{row['id']}.jpg)\n\n"
            f"- 原文件名：{row['name']}\n"
            f"- 原分类：{row['original_family']} · {FAMILIES[row['original_family']]}\n"
            f"- 初筛建议类：{row['family']} · {FAMILIES[row['family']]}\n"
            f"- 原图尺寸：{row['width']}×{row['height']} px\n"
            f"- 缩略图视觉速记：{row['visual_note']}\n"
            f"- 现有初筛状态：{row['status']}\n"
            f"- 现有初筛意见：{row['screening_note']}\n"
            f"{detailed}{duplicate}\n"
            "这张卡用于按名称、画面速记、分类和初筛意见快速找图。视觉速记来自整组缩略图观察，"
            "不替代逐张高清复核；来源标题也不是图面内容或作者授权的证明。实际选作风格参考前，"
            "应打开本卡中的原图，确认画面、适用性与近期重复。"
            "参考图里的机构、日期、人物和文案不能成为新海报的事实。\n")


def abstract_rows():
    layout_index = json.loads((CATALOG / "layout-index.json").read_text(encoding="utf-8"))
    rows = [row for row in layout_index if row["kind"] == "abstract"]
    abstract_images = list((LAYOUT / "版式海报案例/抽象版25").glob("*.jpg"))
    if len(rows) != len(abstract_images) or len({r["image"] for r in rows}) != len(rows):
        raise ValueError(f"index/image mismatch: {len(rows)} rows, {len(abstract_images)} images")
    return rows


def abstract_card(row):
    image = ROOT / row["image"]
    if not image.is_file():
        raise FileNotFoundError(image)
    image_link = f"../版式海报案例/抽象版25/{image.name}"
    fields = row.get("fields", {})
    selections = [
        ("阅读路径", "阅读路径"), ("主视觉位置", "主视觉位置"),
        ("信息组织", "信息组织方式"), ("图文关系", "图文关系"),
        ("强调方法", "强调方式"), ("信息量", "信息量"),
        ("留白程度", "留白程度"), ("适用条件", "推荐使用条件"),
        ("局限", "主要问题/局限/不适用场景"),
    ]
    bullets = "".join(f"- {label}：{fields[key]}\n" for label, key in selections if fields.get(key) not in (None, ""))
    return (f"# {row['id']} · {row['name']}\n\n"
            f"![{row['name']} 原图](<{image_link}>)\n\n"
            f"- 原图：{image.name}\n"
            f"- 版式类型：{fields.get('一级版式类型', '未记录')} / {fields.get('二级版式特征', '未记录')}\n"
            f"{bullets}\n"
            "以上是既有抽象版式表的简明转写，便于按结构检索，不表示本次重新完成逐图视觉复核。"
            "本卡只提供信息层级与图文关系的参考；原图中的日期、机构、文字和联系方式不得沿用。"
            f"需要追溯原表时查看[完整记录](../../../catalog/layout/{row['id']}.md)。\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify generated cards and indexes without writing")
    args = parser.parse_args()
    style = style_rows()
    abstract = abstract_rows()
    for row in style:
        write_or_check(ROOT / row["card"], style_card(row), args.check)
    for row in abstract:
        path = ABSTRACT_CASES / f"{Path(row['image']).stem}.md"
        write_or_check(path, abstract_card(row), args.check)
    style_index = json.dumps(style, ensure_ascii=False, indent=2) + "\n"
    abstract_index = json.dumps([
        {"id": row["id"], "name": row["name"], "kind": "abstract", "image": row["image"],
         "card": f"references/databases/layout/abstract-cases/{Path(row['image']).stem}.md",
         "fields": row.get("fields", {})}
        for row in abstract
    ], ensure_ascii=False, indent=2) + "\n"
    write_or_check(CATALOG / "style-raw-index.json", style_index, args.check)
    write_or_check(CATALOG / "layout-abstract-index.json", abstract_index, args.check)
    print(json.dumps({"status": "pass", "mode": "check" if args.check else "write",
                      "style_cards": len(style), "abstract_cards": len(abstract)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
