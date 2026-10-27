#!/usr/bin/env python3
"""Check identity and potential regressions for a report update. Not a complete QA/security check."""
import json,re,sys
from pathlib import Path

def semver(value):
    match=re.fullmatch(r'(\d+)\.(\d+)\.(\d+)(?:[-+][\w.-]+)?',str(value))
    return tuple(map(int,match.groups())) if match else None

def main(old,new):
    a=json.loads(Path(old).read_text(encoding='utf-8')); b=json.loads(Path(new).read_text(encoding='utf-8'))
    errors=[]; warnings=[]
    if not isinstance(a,dict) or not isinstance(b,dict):
        raise ValueError('Expected one JSON object in each file')
    if a.get('id')!=b.get('id'): errors.append('Stable report id changed')
    for k in ('version','schemaVersion'):
        if k in a and a[k]!=b.get(k): errors.append(f'Compatibility field {k} changed')
    prev=semver(a.get('reportVersion','1.0.0' if isinstance(a.get('version'),int) else ''))
    now=semver(b.get('reportVersion'))
    if not now: errors.append('New reportVersion missing or not SemVer')
    elif prev and now<=prev: errors.append(f'reportVersion did not increase ({prev} -> {now})')
    if a.get('name')!=b.get('name'):warnings.append('Report name changed; check if intentional')
    oldperm=set(a.get('permissions') or []); newperm=set(b.get('permissions') or [])
    if oldperm-newperm:warnings.append('Permissions removed: '+', '.join(sorted(oldperm-newperm)))
    if newperm-oldperm:warnings.append('Permissions added: '+', '.join(sorted(newperm-oldperm)))
    for k in ('html','css','js'):
        if not isinstance(b.get(k),str) or not b[k].strip():errors.append(f'{k} missing/empty')
    old_methods = set(re.findall(r'reportAPI\.([A-Za-z]+)\(', a.get('js','')))
    new_methods = set(re.findall(r'reportAPI\.([A-Za-z]+)\(', b.get('js','')))
    for m in sorted(old_methods - new_methods):
        warnings.append(f'Previously used SDK method removed: {m}')
    for w in warnings:print('WARNING:',w)
    for e in errors:print('ERROR:',e)
    if errors:sys.exit(1)
    print('PASS: version identity checks; functional regressions still require testing')
if __name__=='__main__':
    if len(sys.argv)!=3:sys.exit('Usage: python scripts/check_report_update.py previous.json edited.json')
    main(*sys.argv[1:])
