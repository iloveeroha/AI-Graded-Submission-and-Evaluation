$ErrorActionPreference = "Stop"
$baseUrl = "http://127.0.0.1:8000"
$cookieJar = Join-Path $PSScriptRoot "cookies.txt"
$outputPath = Join-Path $PSScriptRoot "loginuser"

$username = Read-Host "Django username"
$securePassword = Read-Host "Django password" -AsSecureString
$passwordPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword)

try {
    $password = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($passwordPointer)
    $csrfJson = & curl.exe -sS -c $cookieJar -b $cookieJar "$baseUrl/api/csrf/"
    if ($LASTEXITCODE -ne 0) {
        throw "Could not request the CSRF token. Is the Django server running?"
    }

    $csrfToken = ($csrfJson -join "`n" | ConvertFrom-Json).csrfToken
    $loginBody = @{
        userName = $username
        password = $password
    } | ConvertTo-Json -Compress
    $curlArgs = @(
        "-sS", "-w", "`nHTTP_STATUS:%{http_code}`n",
        "-c", $cookieJar, "-b", $cookieJar,
        "-X", "POST", "$baseUrl/djangoapp/login/",
        "-H", "Content-Type: application/json",
        "-H", "X-CSRFToken: $csrfToken",
        "--data-raw", $loginBody
    )
    $output = (& curl.exe @curlArgs 2>&1) -join "`n"
    $curlExitCode = $LASTEXITCODE
    $command = 'curl.exe -sS -w "\nHTTP_STATUS:%{http_code}\n" -c cookies.txt -b cookies.txt -X POST http://127.0.0.1:8000/djangoapp/login/ -H "Content-Type: application/json" -H "X-CSRFToken: <CSRF token from /api/csrf/>" --data-raw ''{"userName":"<your username>","password":"<entered securely>"}'''
    @(
        "Command (password omitted):"
        $command
        ""
        "Output:"
        $output
    ) | Set-Content -Encoding UTF8 $outputPath

    Write-Output $output
    if ($curlExitCode -ne 0) {
        throw "The login request failed; see $outputPath."
    }
    if (
        $output -notmatch "HTTP_STATUS:200" -or
        $output -notmatch '"status":"Authenticated"'
    ) {
        throw "Login was not successful. Check the username and password in $outputPath."
    }
}
finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($passwordPointer)
    Remove-Variable password -ErrorAction SilentlyContinue
}
