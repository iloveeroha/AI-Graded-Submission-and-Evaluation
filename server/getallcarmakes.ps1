$ErrorActionPreference = "Stop"
$url = "http://127.0.0.1:8000/djangoapp/get_cars"
$outputPath = Join-Path $PSScriptRoot "getallcarmakes"
$curlCommand = 'curl.exe -sS "' + $url + '" -w "\nHTTP_STATUS:%{http_code}\n"'
$output = (& curl.exe -sS -w "`nHTTP_STATUS:%{http_code}`n" $url 2>&1) -join "`n"
$curlExitCode = $LASTEXITCODE

@(
    "Command:"
    $curlCommand
    ""
    "Output:"
    $output
) | Set-Content -Encoding UTF8 $outputPath

Write-Output $output
if ($curlExitCode -ne 0) {
    throw "The car makes request failed; see $outputPath."
}
if ($output -notmatch "HTTP_STATUS:200") {
    throw "The car makes endpoint returned a non-success status; see $outputPath."
}
