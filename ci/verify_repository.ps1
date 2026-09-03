param([string]$Check = "all")
$ErrorActionPreference = "Stop"
python "$PSScriptRoot/verify_repository.py" $Check
