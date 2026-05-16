# Smoke test: hit the streamable-http MCP server and verify the 7 BIST tools are registered.
# Mirrors scripts/smoke_http.ps1 — same handshake, different expected-tools set.

$ErrorActionPreference = "Stop"
$endpoint = "http://127.0.0.1:8000/mcp"

# Step 1: initialize an MCP session
$initBody = @{
    jsonrpc = "2.0"
    id      = 1
    method  = "initialize"
    params  = @{
        protocolVersion = "2024-11-05"
        capabilities    = @{}
        clientInfo      = @{ name = "smoke-bist"; version = "0.1" }
    }
} | ConvertTo-Json -Depth 10 -Compress

$headers = @{
    "Content-Type" = "application/json"
    "Accept"       = "application/json, text/event-stream"
}

$response = Invoke-WebRequest -Uri $endpoint -Method Post -Body $initBody -Headers $headers
$sessionId = $response.Headers["Mcp-Session-Id"] | Select-Object -First 1
if (-not $sessionId) { Write-Error "no session id returned"; exit 1 }
Write-Output "session: $sessionId"

# Step 2: send initialized notification
$initializedBody = @{ jsonrpc = "2.0"; method = "notifications/initialized" } | ConvertTo-Json -Compress
$headersWithSession = $headers + @{ "Mcp-Session-Id" = $sessionId }
Invoke-WebRequest -Uri $endpoint -Method Post -Body $initializedBody -Headers $headersWithSession | Out-Null

# Step 3: list tools
$listBody = @{ jsonrpc = "2.0"; id = 2; method = "tools/list" } | ConvertTo-Json -Compress
$resp = Invoke-WebRequest -Uri $endpoint -Method Post -Body $listBody -Headers $headersWithSession
$body = $resp.Content

# Strip SSE wrapper if present
if ($body -match "^data: (.+)$") {
    $body = $Matches[1]
}
$dataLines = $body -split "`n" | Where-Object { $_ -match "^data: " } | ForEach-Object { $_ -replace "^data: ", "" }
if ($dataLines) { $body = $dataLines[-1] }

$parsed = $body | ConvertFrom-Json
$tools = $parsed.result.tools | ForEach-Object { $_.name } | Sort-Object

Write-Output ""
Write-Output "=== Registered tools ($($tools.Count)) ==="
$tools | ForEach-Object { Write-Output "  $_" }

$expectedBist = @(
    "bist_market_overview",
    "bist_sector_scan",
    "bist_sector_scanner",
    "bist_index_analysis",
    "bist_stock_screener",
    "bist_trade_plan",
    "bist_fibonacci_retracement"
)
$missing = $expectedBist | Where-Object { $_ -notin $tools }
Write-Output ""
if ($missing) {
    Write-Output "FAIL: missing BIST tools: $($missing -join ', ')"
    exit 1
} else {
    Write-Output "PASS: all 7 BIST tools registered"
}
