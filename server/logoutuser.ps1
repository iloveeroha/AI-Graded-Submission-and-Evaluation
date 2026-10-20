$ErrorActionPreference = "Stop"
$baseUrl = "http://127.0.0.1:8000"
$cookieJar = Join-Path $PSScriptRoot "cookies.txt"
$outputPath = Join-Path $PSScriptRoot "logoutuser"

if (-not (Test-Path $cookieJar)) {
    throw "Run loginuser.ps1 successfully first; its session cookie is required."
}

$curlArgs = @(
    "-sS", "-w", "`nHTTP_STATUS:%{http_code}`n",
    "-c", $cookieJar, "-b", $cookieJar,
    "-X", "GET", "$baseUrl/djangoapp/logout"
)
$output = (& curl.exe @curlArgs 2>&1) -join "`n"
$curlExitCode = $LASTEXITCODE
$command = 'curl.exe -sS -w "\nHTTP_STATUS:%{http_code}\n" -c cookies.txt -b cookies.txt -X GET http://127.0.0.1:8000/djangoapp/logout'
@(
    "Command (session cookie and CSRF token omitted):"
    $command
    ""
    "Output:"
    $output
) | Set-Content -Encoding UTF8 $outputPath

Write-Output $output
if ($curlExitCode -ne 0) {
    throw "The logout request failed; see $outputPath."
}
if (
    $output -notmatch "HTTP_STATUS:200" -or
    $output -notmatch '"userName":""'
) {
    throw "Logout was not successful. Run loginuser.ps1 first and see $outputPath."
}
