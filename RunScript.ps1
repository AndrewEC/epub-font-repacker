param(
    [ValidateSet(
        "All",
        "Audit",
        "Lint",
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
        Invoke-RuffScript
        Invoke-TestScript 85 {
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
    "Lint" { Invoke-RuffScript }
    "Install" { Invoke-InstallScript }
    "IntegrationTests" {
        Invoke-OtherScript "Integration tests" @(0) {
            python -m unittest repack.tests.integration.integration_test
        }
    }
    "Tests" {
        Invoke-TestScript 85 {
            coverage run `
                --omit=./repack/tests/* `
                --source=repack.core `
                --branch `
                --module repack.tests.__run_all
        }
    }
}
