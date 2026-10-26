# Synchronize Repository Descriptions, Topics, and Homepages on GitHub
param (
    [Parameter(Mandatory=$false)]
    [string]$Token
)

if (-not $Token) {
    $Token = Read-Host "Enter your GitHub Personal Access Token (with 'repo' scope)"
}

$headers = @{
    "Authorization" = "Bearer $Token"
    "Accept"        = "application/vnd.github.v3+json"
    "User-Agent"    = "PowerShell-Madhu36-Sync"
}

$metadata = @{
    "Adaptive-firewall-Application-using-AI" = @{
        description = "Next-generation adaptive firewall featuring real-time anomaly detection and eBPF/XDP kernel-level rule automation (LSTM-Autoencoder + PPO RL)."
        topics      = @("deep-learning", "ebpf", "firewall", "network-security", "ddos-defense", "pytorch", "cybersecurity", "python")
        homepage    = ""
    }
    "MXB" = @{
        description = "Ultra-fast, 100% local voice-controlled AI assistant and Windows executive brain powered by Llama 3.1, Whisper, and task orchestration."
        topics      = @("ai-agent", "llama-3-1", "whisper", "voice-assistant", "windows-automation", "python", "ollama")
        homepage    = ""
    }
    "DevIgnite" = @{
        description = "High-performance, cross-platform developer environment manager with a sandboxed symlink routing engine written in Rust."
        topics      = @("rust", "cli", "developer-tools", "systems-programming", "environment-manager")
        homepage    = ""
    }
    "ASTra" = @{
        description = "Security-first, repository-local action layer and AST vulnerability scanner for AI developer assistants."
        topics      = @("ast", "code-security", "static-analysis", "llm-security", "python")
        homepage    = ""
    }
    "Game-Complex" = @{
        description = "Interactive gaming storefront and 3D environment architecture featuring procedural systems and high-throughput backend services."
        topics      = @("unity", "csharp", "react", "django", "game-development", "procedural-generation")
        homepage    = ""
    }
    "Packet-way" = @{
        description = "Enterprise-grade network threat detection and deep packet inspection engine with raw socket traffic reconstruction."
        topics      = @("network-security", "packet-inspection", "threat-detection", "javascript", "nodejs", "forensics")
        homepage    = ""
    }
    "My_Portfolio" = @{
        description = "Futuristic 3D WebGL developer portfolio featuring custom cursor physics, Web Audio SFX engine, and live telemetry HUD."
        topics      = @("threejs", "react", "typescript", "webgl", "portfolio", "tailwindcss", "cyberpunk")
        homepage    = "https://madhu-36.github.io/My_Portfolio/"
    }
}

foreach ($repo in $metadata.Keys) {
    Write-Host ">>> Updating repository: $repo..." -ForegroundColor Cyan
    $item = $metadata[$repo]

    # 1. Update Description & Homepage
    $body = @{
        description = $item.description
        homepage    = $item.homepage
    } | ConvertTo-Json

    try {
        Invoke-RestMethod -Uri "https://api.github.com/repos/Madhu-36/$repo" -Method Patch -Headers $headers -Body $body -ContentType "application/json" | Out-Null
        Write-Host "  [OK] Description and Homepage updated!" -ForegroundColor Green
    } catch {
        Write-Warning "  [FAIL] Could not update description: $($_.Exception.Message)"
    }

    # 2. Update Topics
    $topicBody = @{
        names = $item.topics
    } | ConvertTo-Json

    try {
        Invoke-RestMethod -Uri "https://api.github.com/repos/Madhu-36/$repo/topics" -Method Put -Headers $headers -Body $topicBody -ContentType "application/json" | Out-Null
        Write-Host "  [OK] Topics updated: $($item.topics -join ', ')" -ForegroundColor Green
    } catch {
        Write-Warning "  [FAIL] Could not update topics: $($_.Exception.Message)"
    }
}

Write-Host "`nAll repository metadata synchronization complete!" -ForegroundColor Magenta
