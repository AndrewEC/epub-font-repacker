param(
    [ValidateSet(
        "All",
        "Audit",
        "Flake",
        "Install",
        "IntegrationTests",
        "Tests"
    )]
    [string]$ScriptAction
)

Import-Module ./PyBuildScripts

Invoke-ActivateScript

switch ($ScriptAction) {
    "All" {
        Invoke-InstallScript
        Invoke-FlakeScript
        Invoke-TestScript 90 {
            coverage run `
                --omit=./repack/tests/* `
                --source=repack.core `
                --branch `
                --module repack.tests.__run_all
        }
        Invoke-OtherScript "Integration tests" @(0) {
            python -m unittest repack.tests.integration.integration_test
        }
        Invoke-AuditScript
    }
    "Audit" { Invoke-AuditScript }
    "Flake" { Invoke-FlakeScript }
    "Install" { Invoke-InstallScript }
    "IntegrationTests" {
        Invoke-OtherScript "Integration tests" @(0) {
            python -m unittest repack.tests.integration.integration_test
        }
    }
    "Tests" {
        Invoke-TestScript 90 {
            coverage run `
                --omit=./repack/tests/* `
                --source=repack.core `
                --branch `
                --module repack.tests.__run_all
        }
    }
}
