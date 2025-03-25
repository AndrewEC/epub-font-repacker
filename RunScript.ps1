param(
    [ValidateSet(
        "All",
        "Audit",
        "Flake",
        "Install"
    )]
    [string]$ScriptAction
)

. ./build-scripts/Activate.ps1
. ./build-scripts/Audit.ps1
. ./build-scripts/Flake.ps1
. ./build-scripts/Install.ps1

Invoke-ActivateScript

switch ($ScriptAction) {
    "All" {
        Invoke-InstallScript
        Invoke-FlakeScript
        Invoke-AuditScript
    }
    "Audit" { Invoke-AuditScript }
    "Flake" { Invoke-FlakeScript }
    "Install" { Invoke-InstallScript }
}
