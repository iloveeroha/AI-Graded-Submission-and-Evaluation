param(
    [Parameter(Mandatory = $true)]
    [ValidateRange(1, 2147483647)]
    [int]$DealerId
)

$ErrorActionPreference = "Stop"
$url = "http://127.0.0.1:8000/djangoapp/get_dealer_reviews/$DealerId"
$outputPath = Join-Path $PSScriptRoot "getdealerreviews"
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
    throw "The dealer reviews request failed; see $outputPath."
}
if ($output -notmatch "HTTP_STATUS:200") {
    throw "The dealer reviews endpoint returned a non-success status; see $outputPath."
}
