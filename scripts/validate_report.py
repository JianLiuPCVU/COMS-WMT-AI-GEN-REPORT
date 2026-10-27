#!/usr/bin/env python3
"""Static validation of portable report JSON. Not a security audit."""
import json,re,sys,shutil,subprocess,tempfile,pathlib

def validate(path):
    errors=[]; warnings=[]
    raw=pathlib.Path(path).read_text(encoding='utf-8')
    try: doc=json.loads(raw)
    except json.JSONDecodeError as e: return [f'Invalid JSON: {e}'], []
    docs=doc if isinstance(doc,list) else [doc]
    if not docs: errors.append('Empty report array')
    for index,r in enumerate(docs):
        label=f'report[{index}]'
        if not isinstance(r,dict): errors.append(f'{label} must be an object');continue
        if not isinstance(r.get('id'),str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,80}',r['id']): errors.append(f'{label}: invalid id')
        if not isinstance(r.get('name'),str) or len(r['name'])>140: errors.append(f'{label}: invalid name')
        for key in ('html','css','js'):
            if not isinstance(r.get(key),str): errors.append(f'{label}: missing string {key}')
        if len(json.dumps(r,ensure_ascii=False))>=500000: errors.append(f'{label}: exceeds extension size limit')
        js=r.get('js','')
        if isinstance(js,str):
            for pattern,reason in [(r'\bchrome\s*\.', 'Chrome APIs are not available inside report sandbox'),(r'\b(?:localStorage|sessionStorage|document\.cookie)\b','Do not use browser credential/storage surfaces'),(r'\b(?:fetch|XMLHttpRequest)\s*\(', 'Use reportAPI rather than direct HTTP'),(r'\beval\s*\(', 'Avoid eval in generated code'),(r'\bnew\s+Function\b','Avoid dynamic function generation')]:
                if re.search(pattern,js): warnings.append(f'{label}: {reason}')
            if 'reportAPI' not in js: warnings.append(f'{label}: no reportAPI usage detected (may be an offline-only report)')
            if shutil.which('node'):
                with tempfile.NamedTemporaryFile('w',suffix='.js',delete=False) as t:
                    t.write(js); temp=t.name
                result=subprocess.run(['node','--check',temp],capture_output=True,text=True)
                pathlib.Path(temp).unlink(missing_ok=True)
                if result.returncode: errors.append(f'{label}: JavaScript parse error: {result.stderr.strip()}')
        methods={'query','queryTable','queryChart','queryTotal','getDataSets','getBrands','getAlertLabels'}
        permission_map={'queryTable':'table','queryChart':'chart','queryTotal':'total','getDataSets':'datasets','getBrands':'brands','getAlertLabels':'alertLabels'}
        declared=r.get('permissions',[])
        if declared is not None and (not isinstance(declared,list) or any(x not in {'table','chart','total','datasets','brands','alertLabels'} for x in declared)):
            errors.append(f'{label}: invalid permissions')
        for method in re.findall(r'\breportAPI\s*\.\s*([A-Za-z_$][\w$]*)\s*\(',js):
            if method not in methods: errors.append(f'{label}: unsupported SDK method {method}')
            elif method in permission_map and permission_map[method] not in (declared or []): errors.append(f'{label}: missing permission {permission_map[method]}')
        if 'queryTable(' in js and re.search(r'\b(sum|total|weighted|aggregate|reduce)\b',js,re.I) and 'hasNextPage' not in js and 'queryTotal(' not in js:
            warnings.append(f'{label}: possible page-only KPI; confirm coverage and label the scope')
        # Detect technical setup forms that shift report-author work to the end user.
        ui=(r.get('html','') or '') + ' ' + js
        if re.search(r'(?:paste|enter|provide|fill in).{0,70}(?:queryTable|request JSON|query params|field mapping)',ui,re.I) or re.search(r'(?:queryTable parameters|host-approved contract|field mapping)',ui,re.I):
            warnings.append(f'{label}: user-facing technical query or field mapping configuration detected; report may not be ready to run')
        if re.search(r'<textarea',r.get('html',''),re.I) and re.search(r'(?:queryTable|JSON|parameters)',ui,re.I):
            warnings.append(f'{label}: editable technical request JSON detected; prefer fully constructed SDK calls')
        if 'queryChart(' in js and 'xAxis' not in js:
            warnings.append(f'{label}: trend should use xAxis date labels')
    return errors,warnings

if __name__=='__main__':
    if len(sys.argv)!=2: print('Usage: python3 validate_report.py REPORT.json');sys.exit(2)
    errors,warnings=validate(sys.argv[1])
    for w in warnings: print('WARNING:',w)
    for e in errors: print('ERROR:',e)
    if errors: sys.exit(1)
    print('PASS: report package shape and available static checks')
