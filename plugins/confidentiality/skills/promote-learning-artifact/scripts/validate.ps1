param()
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
foreach($p in @('SKILL.md','agents','scripts','references','assets','tests')){if(-not(Test-Path -LiteralPath (Join-Path $root $p))){throw "missing $p"}}
if(-not(Test-Path -LiteralPath (Join-Path $root 'assets\policy.json') -PathType Leaf)){throw 'missing assets/policy.json'}
'PASS'
return
