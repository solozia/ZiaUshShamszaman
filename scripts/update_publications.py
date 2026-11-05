#!/usr/bin/env python3
"""Synchronise publications from OpenAlex, preserving local curated metadata.
Requires OPENALEX_AUTHOR_ID. Optional OPENALEX_API_KEY, OPENALEX_EMAIL.
Standard library only. Never matches authors by name alone.
"""
import datetime as dt
import json
import os
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
AUTHOR_ID = os.getenv('OPENALEX_AUTHOR_ID', '').strip().rstrip('/').split('/')[-1]
API_KEY = os.getenv('OPENALEX_API_KEY', '').strip()
EMAIL = os.getenv('OPENALEX_EMAIL', '').strip()
AUTO_APPROVE = os.getenv('AUTO_APPROVE_NEW', 'false').lower() == 'true'


def read(name, default):
    p = DATA / name
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else default


def save(name, data):
    p = DATA / name
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def api(url):
    params = {'mailto': EMAIL} if EMAIL else {}
    if API_KEY:
        params['api_key'] = API_KEY
    url += ('&' if '?' in url else '?') + urllib.parse.urlencode(params) if params else ''
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'ResearchUniverse/3.0 (academic bibliography updater)', 'Accept': 'application/json'})
            with urllib.request.urlopen(req, timeout=35) as response:
                return json.load(response)
        except Exception as exc:
            if attempt == 3:
                raise RuntimeError(f'OpenAlex API request failed: {exc}') from exc
            time.sleep(2 ** attempt)


def doi_normalize(v):
    if not v:
        return None
    return re.sub(r'^https?://(?:dx\.)?doi\.org/', '', v.strip(), flags=re.I).lower() or None


def key_title(t):
    return re.sub(r'[^a-z0-9]', '', (t or '').lower())


def abstract(inv):
    if not inv:
        return ''
    pos = [(i, word) for word, positions in inv.items() for i in positions]
    return ' '.join(w for _, w in sorted(pos))[:10000]


def main():
    if not re.fullmatch(r'A\d+', AUTHOR_ID):
        print('OPENALEX_AUTHOR_ID not set or invalid. No data changed. Set an ID such as A1234567890 (not a name).')
        return 2
    author = api('https://api.openalex.org/authors/' + AUTHOR_ID)
    display = author.get('display_name', '')
    # Identity guard: stop if author identity is obviously not the intended scholar.
    identity = display.lower().replace('-', ' ')
    if 'zia' not in identity or ('shamszaman' not in identity and 'ush' not in identity):
        raise RuntimeError(f'Author ID points to unexpected identity: {display!r}. Refusing to overwrite files.')
    works = []
    cursor = '*'
    for page in range(50):
        q = urllib.parse.urlencode({'filter': 'author.id:' + AUTHOR_ID, 'per-page': 200, 'cursor': cursor})
        data = api('https://api.openalex.org/works?' + q)
        works.extend(data.get('results', []))
        next_cursor = data.get('meta', {}).get('next_cursor')
        if not next_cursor or not data.get('results'):
            break
        cursor = next_cursor
    else:
        raise RuntimeError('More than 50 pages of works; refusing partial sync.')
    old = read('publications.json', [])
    rejected = set(read('excluded_dois.json', []))
    by_doi = {doi_normalize(p.get('doi')): p for p in old if doi_normalize(p.get('doi'))}
    by_title = {key_title(p.get('title')): p for p in old if key_title(p.get('title'))}
    candidates = []
    updated = []
    for w in works:
        title = (w.get('title') or '').strip()
        year = w.get('publication_year')
        if not title or not isinstance(year, int):
            continue
        doi = doi_normalize(w.get('doi'))
        if doi and doi in rejected:
            continue
        authors = [a.get('author', {}).get('display_name', '') for a in w.get('authorships', [])]
        venue = ((w.get('primary_location') or {}).get('source') or {}).get('display_name') or ''
        rec = {
            'id': 'oa-' + w['id'].split('/')[-1], 'openalex_id': w['id'], 'title': title,
            'year': year, 'authors': authors, 'venue': venue, 'doi': doi,
            'url': 'https://doi.org/' + doi if doi else w.get('id', ''),
            'abstract': abstract(w.get('abstract_inverted_index')),
            'cited_by_count': w.get('cited_by_count'),
            'referenced_works': w.get('referenced_works') or [],
            'themes': [t.get('display_name') for t in (w.get('topics') or [])[:3] if t.get('display_name')],
            'source': 'OpenAlex', 'verification': 'openalex-author-id'
        }
        previous = (by_doi.get(doi) if doi else None) or by_title.get(key_title(title))
        if previous:
            # Retain the owner's thematic categorisation and any custom annotations.
            rec['id'] = previous.get('id', rec['id'])
            if previous.get('themes') and previous.get('source') != 'OpenAlex':
                rec['themes'] = previous['themes']
            for k in ('notes', 'featured', 'custom_url'):
                if k in previous:
                    rec[k] = previous[k]
            updated.append(rec)
        elif AUTO_APPROVE:
            updated.append(rec)
        else:
            candidates.append(rec)
    # Preserve curated records not found in OpenAlex (e.g. accepted manuscripts).
    used_ids = {p['id'] for p in updated}
    matched_keys = {key_title(p['title']) for p in updated}
    for p in old:
        if p.get('id') not in used_ids and key_title(p.get('title')) not in matched_keys:
            updated.append(p)
    updated.sort(key=lambda p: (-p.get('year', 0), p.get('title', '').lower()))
    save('publications.json', updated)
    save('pending_review.json', candidates)
    save('sync_status.json', {
        'last_updated_utc': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'),
        'source': 'OpenAlex + preserved curated records', 'openalex_author_id': AUTHOR_ID,
        'openalex_author_name': display, 'openalex_works_seen': len(works),
        'publication_records': len(updated), 'pending_review': len(candidates),
        'automatic_new_records': AUTO_APPROVE,
    })
    print(f'Synchronised {len(updated)} records, {len(candidates)} pending; OpenAlex returned {len(works)} works for {display}.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
