"""Read portable community poster indexes. Runtime uses only Python's stdlib."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def records(library):
    filename = {'layout': 'layout-index.json', 'layout-abstract': 'layout-abstract-index.json',
                'style-raw': 'style-raw-index.json'}.get(library, f'{library}-cases.json')
    path = ROOT / 'references' / 'catalog' / filename
    return json.loads(path.read_text(encoding='utf-8'))


def search(library=None, query='', kind=None, family=None, case_id=None, limit=8, filters=None):
    found = []
    for lib in ([library] if library else ['layout-abstract', 'style-raw']):
        for row in records(lib):
            if case_id and row['id'].casefold() != case_id.casefold():
                continue
            if kind and row.get('kind') != kind:
                continue
            if family and row.get('family') != family:
                continue
            if filters and any(k not in row.get('fields', {}) or str(row['fields'][k]) != str(v) for k, v in filters.items()):
                continue
            body = (row.get('name', '') + json.dumps(row.get('fields', {}), ensure_ascii=False)
                    + row.get('rule', '') + row.get('screening_note', '')
                    + row.get('family_name', '') + row.get('visual_note', '')).casefold()
            tokens = [t for t in re.split(r'\s+', query.casefold()) if t]
            score = (sum(t in body for t in tokens), sum(body.count(t) for t in tokens))
            if tokens and not score[0]:
                continue
            found.append((score, lib, row))
    found.sort(key=lambda x: (-x[0][0], -x[0][1], x[2]['id']))
    if case_id:
        return [json.loads((ROOT / r['record']).read_text(encoding='utf-8')) if lib == 'layout' else r for _, lib, r in found]
    results = []
    useful = ['所属大主题类别', '传播目标', '信息类型', '目标受众', '信息量', '信息分区/组数量',
              '阅读路径', '信息组织方式', '图文关系', '强调方式', '留白程度', '信息密度',
              '一级版式类型', '二级版式特征',
              '适用信息类型/场景', '推荐使用条件', '可转化为Skill的规则', '主要问题/局限/不适用场景']
    for _, lib, row in found[:limit]:
        brief = {k: row[k] for k in ['id', 'name', 'kind', 'family', 'family_name', 'source', 'image', 'card', 'record', 'field_count', 'rule', 'review_status', 'rights_status', 'status', 'visual_note', 'screening_note', 'detailed_card', 'width', 'height'] if k in row}
        brief['library'] = lib
        brief['fields'] = {k: row.get('fields', {})[k] for k in useful if k in row.get('fields', {})}
        brief['detail'] = f'Read {row["card"]} for the reference card' if 'card' in row else f'Use --id {row["id"]} for details'
        results.append(brief)
    return results


def verify_layout(root=None):
    """Check portable paths, source/image hashes and index/record agreement."""
    root = Path(root or ROOT).resolve()
    issues = []
    def local(value):
        if not isinstance(value, str) or not value or Path(value).is_absolute():
            raise ValueError('missing or absolute resource path')
        path = (root / value).resolve()
        if not path.is_relative_to(root):
            raise ValueError('resource path escapes skill root')
        if not path.is_file():
            raise ValueError(f'missing resource: {value}')
        return path
    try:
        rows = json.loads((root / 'references/catalog/layout-index.json').read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        return {'status': 'fail', 'cases': 0, 'issues': [str(exc)]}
    ids = [r.get('id') for r in rows]
    if len(ids) != len(set(ids)):
        issues.append('duplicate case IDs')
    hashes = {}
    for row in rows:
        try:
            paths = {k: local(row.get(k)) for k in ['source', 'image', 'card', 'record']}
            rec = json.loads(paths['record'].read_text(encoding='utf-8'))
            for k in ['id', 'name', 'kind', 'source', 'sheet', 'row', 'image', 'card', 'record', 'field_count', 'image_sha256', 'source_sha256']:
                if rec.get(k) != row.get(k):
                    raise ValueError(f'index/record mismatch: {k}')
            if len(rec['fields']) != row['field_count'] or rec['fields'].get('案例ID') != row['id']:
                raise ValueError('field count or ID mismatch')
            if any(rec['fields'].get(k) != v for k, v in row['fields'].items()):
                raise ValueError('search field value mismatch')
            for k in ['source', 'image']:
                path = paths[k]
                if path not in hashes:
                    hashes[path] = hashlib.sha256(path.read_bytes()).hexdigest()
                if hashes[path] != row.get(k + '_sha256'):
                    raise ValueError(f'{k} hash mismatch')
        except (OSError, ValueError, KeyError, TypeError) as exc:
            issues.append(f'{row.get("id", "unknown")}: {exc}')
    return {'status': 'fail' if issues else 'pass', 'cases': len(rows), 'issues': issues,
            'scope': 'resource integrity only; no visual or semantic reanalysis'}


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--library', choices=['theme', 'layout', 'style', 'layout-abstract', 'style-raw'])
    p.add_argument('--query', default='')
    p.add_argument('--kind', choices=['abstract', 'concrete'])
    p.add_argument('--family')
    p.add_argument('--id')
    p.add_argument('--theme', choices=[f'T{x:02}' for x in range(1, 7)], help='List real references in a theme folder; not semantic image search')
    p.add_argument('--limit', type=int, default=5)
    p.add_argument('--field', action='append', default=[], metavar='NAME=VALUE', help='Exact match against indexed field; repeat for AND conditions')
    p.add_argument('--verify', action='store_true', help='Verify layout records, cards, images and source hashes')
    a = p.parse_args()
    if a.limit < 1:
        p.error('--limit must be positive')
    filters = {}
    for item in a.field:
        if '=' not in item or not item.split('=', 1)[0]:
            p.error('--field requires NAME=VALUE')
        key, value = item.split('=', 1)
        if key in filters:
            p.error('Repeat a field name only once')
        filters[key] = value
    if a.verify:
        if a.library not in (None, 'layout') or a.theme:
            p.error('--verify checks the layout library')
        result = verify_layout()
    elif a.theme:
        groups = json.loads((ROOT / 'references/catalog/theme-groups.json').read_text(encoding='utf-8'))
        result = [{**g, 'images': g['images'][:a.limit]} for g in groups if g['id'] == a.theme]
    else:
        result = search(a.library, a.query, a.kind, a.family, a.id, a.limit, filters)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if a.id and not result:
        raise SystemExit(1)
    if a.verify and result['status'] != 'pass':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
