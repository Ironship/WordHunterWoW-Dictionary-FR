# Archive the finished wave and prepare the next one.
#   pwsh Tools/wave.ps1 <number of the wave just finished>
param([Parameter(Mandatory=$true)][int]$Finished, [int]$Limit = 6000)
$work = "Data/cache/audit_work"
$dest = "$work/done/wave_{0:d2}" -f $Finished
# Everything accepted is already in CuratedFR.jsonl, which is what prepare_audit
# reads to know what is done, so the batch files can be moved out of the way.
New-Item -ItemType Directory -Force $dest | Out-Null
foreach ($side in @("in", "out")) {
  if (Test-Path "$work/$side") {
    Move-Item "$work/$side" "$dest/$side" -Force
  }
}
python Tools/prepare_audit.py --limit $Limit --batch-size 150
