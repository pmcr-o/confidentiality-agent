from __future__ import annotations
import argparse,json
from pathlib import Path

def load(path): return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output');a=p.parse_args()
    data=load(a.input)
    fields=data.get('fields')
    if not isinstance(fields,dict): raise SystemExit('fields must be an object')
    allowed=[str(x) for x in data.get('allowedFields',[])]
    protected={str(x) for x in data.get('protectedFields',[])}
    if not allowed: raise SystemExit('allowedFields required')
    overlap=sorted(set(allowed)&protected)
    if overlap: raise SystemExit('protected fields cannot be disclosed: '+','.join(overlap))
    level=str(data.get('classification','')).upper()
    if level not in {'PUBLIC','INTERNAL','CONFIDENTIAL','RESTRICTED'}: raise SystemExit('classification required')
    agreements=list(data.get('agreementRefs',[])); grants=list(data.get('grantRefs',[]))
    if level in {'CONFIDENTIAL','RESTRICTED'} and not agreements: raise SystemExit('agreementRefs required for confidential/restricted disclosure')
    if not grants: raise SystemExit('grantRefs required')
    missing=[x for x in allowed if x not in fields]
    if missing: raise SystemExit('allowed field missing from source: '+','.join(missing))
    disclosed={k:fields[k] for k in allowed}
    omitted=sorted(k for k in fields if k not in disclosed)
    out={'schema':'pmcro.minimum-disclosure/v1','recipient':data.get('recipient',''),'classification':level,'agreementRefs':agreements,'grantRefs':grants,'disclosed':disclosed,'omittedFields':omitted,'minimumNecessary':True,'sourceMutation':False}
    text=json.dumps(out,indent=2)
    if a.output: Path(a.output).write_text(text+'\n',encoding='utf-8')
    print(text)
if __name__=='__main__': main()
