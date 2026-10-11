from __future__ import annotations
import argparse,json,hashlib
from pathlib import Path

def load(path): return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    data=load(a.input)
    level=str(data.get('classification','')).upper()
    if level not in {'PUBLIC','INTERNAL','CONFIDENTIAL','RESTRICTED'}: raise SystemExit('classification required')
    if data.get('sourceKind')=='raw-trail': raise SystemExit('raw trails are not directly eligible for learning promotion')
    if level=='RESTRICTED': raise SystemExit('restricted artifacts require a separate declassification capability before learning promotion')
    policy_refs=list(data.get('policyRefs',[])); grant_refs=list(data.get('grantRefs',[])); consent=data.get('consent',{})
    if not policy_refs: raise SystemExit('policyRefs required')
    if not grant_refs: raise SystemExit('grantRefs required')
    if level in {'INTERNAL','CONFIDENTIAL'}:
        if consent.get('status')!='EXPLICIT' or consent.get('learningAllowed') is not True: raise SystemExit('explicit learning consent required')
    fields=data.get('fields')
    if not isinstance(fields,dict): raise SystemExit('fields must be an object')
    allowed=[str(x) for x in data.get('allowedLearningFields',[])]
    if not allowed: raise SystemExit('allowedLearningFields required')
    missing=[x for x in allowed if x not in fields]
    if missing: raise SystemExit('allowed learning field missing: '+','.join(missing))
    artifact={k:fields[k] for k in allowed}
    body={'schema':'pmcro.learning-artifact/v1','sourceRef':data.get('sourceRef',''),'classification':level,'purpose':data.get('purpose',''),'retentionDays':int(data.get('retentionDays',0)),'policyRefs':policy_refs,'grantRefs':grant_refs,'consentRef':consent.get('consentRef',''),'artifact':artifact,'rawTrailIncluded':False,'sanitized':True,'trainingEligible':True}
    if body['retentionDays']<=0: raise SystemExit('retentionDays must be positive')
    body['artifactDigest']=hashlib.sha256(json.dumps(body['artifact'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
    Path(a.output).write_text(json.dumps(body,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(body,indent=2))
if __name__=='__main__': main()
