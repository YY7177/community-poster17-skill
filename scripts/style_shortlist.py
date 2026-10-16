"""Shortlist image-linked style cases and flag recently shown references."""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'references/catalog/style-raw-index.json'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def recently_shown(outputs, count=6):
    if not outputs or not outputs.exists():
        return set(), set()
    task_files = []
    for task_dir in outputs.iterdir():
        if not task_dir.is_dir():
            continue
        files = [task_dir / name for name in ('run-record.json', 'directions.json')]
        files = [path for path in files if path.is_file()]
        if files:
            task_files.append((max(path.stat().st_mtime for path in files), files))
    recent = [path for _, files in sorted(task_files, reverse=True)[:count] for path in files]
    hashes = set()
    ids = set()
    for directions in recent:
        try:
            data = json.loads(directions.read_text(encoding='utf-8-sig'))
            for card in data.get('cards', []):
                for ref in card.get('style_references', []):
                    path = directions.parent / ref
                    if path.is_file():
                        hashes.add(digest(path))
            for card in data.get('style_candidates', []):
                if isinstance(card, dict):
                    case_id = card.get('case_id') or card.get('id')
                    if case_id:
                        ids.add(case_id)
        except (OSError, ValueError):
            continue
    return hashes, ids


def shortlist(task_id, outputs, per_family):
    used_hashes, used_ids = recently_shown(outputs)
    candidates = []
    duplicate_hashes = set()
    for row in json.loads(INDEX.read_text(encoding='utf-8-sig')):
        path = ROOT / row['image']
        if not path.is_file() or '重复文件' in row['status']:
            continue
        sha = digest(path)
        if sha in duplicate_hashes:
            continue
        duplicate_hashes.add(sha)
        candidates.append(dict(id=row['id'], family=row['family'], family_name=row['family_name'],
                               original_family=row['original_family'], name=row['name'],
                               visual_note=row['visual_note'], path=str(path), case_path=str(ROOT / row['card']),
                               detailed_case_path=(str(ROOT / row['detailed_card']) if row['detailed_card'] else None),
                               reviewed_original='原图已查看' in row['status'],
                               recently_shown=sha in used_hashes or row['id'] in used_ids,
                               screening_note=row['screening_note']))
    results = []
    for family in sorted({item['family'] for item in candidates}):
        family_items = [item for item in candidates if item['family'] == family]
        family_items.sort(key=lambda item: (item['recently_shown'],
                          hashlib.sha256(f'{task_id}:{item["id"]}'.encode()).hexdigest()))
        results.extend(family_items[:per_family])
    return dict(total_raw=len(candidates), recent_references=len(used_hashes) + len(used_ids),
                instruction='Read the linked Markdown cases to narrow candidates; inspect the actual images selected for the three user-facing directions.',
                candidates=results)


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--task-id', required=True)
    parser.add_argument('--outputs', type=Path)
    parser.add_argument('--per-family', type=int, default=3)
    args = parser.parse_args()
    if args.per_family < 1:
        parser.error('--per-family must be positive')
    print(json.dumps(shortlist(args.task_id, args.outputs, args.per_family), ensure_ascii=False, indent=2))
