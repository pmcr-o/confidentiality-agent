from __future__ import annotations
import argparse,json
from pathlib import Path

LEVELS=['PUBLIC','INTERNAL','CONFIDENTIAL','RESTRICTED']

def load(path): return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output');a=p.parse_args()
    data=load(a.input); policy=load(Path(__file__).resolve().parents[1]/'assets/policy.json')
    labels=[str(x).strip().lower() for x in data.get('labels',[]) if str(x).strip()]
    if not data.get('artifactRef'): raise SystemExit('missing artifactRef')
    if not labels: raise SystemExit('labels are required; classifier does not infer undisclosed sensitive facts')
    mapped=[policy['labelPriority'].get(x) for x in labels if x in policy['labelPriority']]
    if not mapped: raise SystemExit('no recognized confidentiality labels')
    level=max(mapped,key=LEVELS.index)
    out={'schema':'pmcro.confidentiality-classification/v1','artifactRef':data['artifactRef'],'declaredLabels':labels,'level':level,'policyRefs':data.get('policyRefs',[]),'agreementRefs':data.get('agreementRefs',[]),'inferenceUsed':False,'learningDefault':'DENY' if level!='PUBLIC' else 'POLICY_ALLOWED'}
    text=json.dumps(out,indent=2)
    if a.output: Path(a.output).write_text(text+'\n',encoding='utf-8')
    print(text)
if __name__=='__main__': main()
