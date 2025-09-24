param(
    [Parameter(Mandatory = $true)]
    [string]$ExePath,

    [string]$CertName = "BanGDream-Gacha Developer",
    [string]$Description = "BanGDream Gacha Simulator"
)

# 兼容 PowerShell 5.1 的编码设置
if ($PSVersionTable.PSVersion.Major -lt 7) {
    try {
        if ((chcp) -notmatch '65001') { chcp 65001 > $null }
        [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
        $OutputEncoding = [System.Text.Encoding]::UTF8
    } catch {}
}

# 检查是否已存在证书
$existingCert = Get-ChildItem -Path "Cert:\CurrentUser\My" | Where-Object { $_.Subject -like "*$CertName*" }

if (-not $existingCert) {
    Write-Host "创建自签名证书..." -ForegroundColor Yellow
    
    # 创建自签名证书
    $cert = New-SelfSignedCertificate -Type CodeSigningCert -Subject "CN=$CertName" -KeySpec Signature -KeyLength 2048 -Provider "Microsoft Enhanced RSA and AES Cryptographic Provider" -CertStoreLocation "Cert:\CurrentUser\My" -KeyUsage DigitalSignature -NotAfter (Get-Date).AddYears(3)
    
    # 将证书添加到受信任的发布者（可选，仅本机生效）
    Write-Host "添加到受信任发布者存储..." -ForegroundColor Yellow
    $store = [System.Security.Cryptography.X509Certificates.X509Store]::new("TrustedPublisher", "CurrentUser")
    $store.Open("ReadWrite")
    $store.Add($cert)
    $store.Close()
    
    $certThumbprint = $cert.Thumbprint
} else {
    Write-Host "使用已存在的证书..." -ForegroundColor Green
    $certThumbprint = $existingCert.Thumbprint
}

# 签名可执行文件
if (Test-Path $ExePath) {
    Write-Host "对 $ExePath 进行签名..." -ForegroundColor Green
    
    # 获取证书并尝试签名
    try {
        $cert = Get-ChildItem -Path "Cert:\CurrentUser\My\$certThumbprint"
        Write-Host "证书信息: $($cert.Subject)" -ForegroundColor Cyan
        Write-Host "证书有效期: $($cert.NotBefore) 至 $($cert.NotAfter)" -ForegroundColor Cyan
        
        # 简化签名：直接签名，不使用时间戳服务器
        Write-Host "使用简单签名模式（跳过时间戳和证书链验证）..." -ForegroundColor Yellow
        
        try {
            # 直接签名，不验证证书链
            $result = Set-AuthenticodeSignature -FilePath $ExePath -Certificate $cert -HashAlgorithm SHA256
            
            # 对于自签名证书，接受 Valid 或 UnknownError 状态
            if ($result.Status -eq "Valid" -or $result.Status -eq "UnknownError") {
                Write-Host "✓ 签名完成!" -ForegroundColor Green
                Write-Host "发布者: $($result.SignerCertificate.Subject)" -ForegroundColor Cyan
                Write-Host "签名状态: $($result.Status)" -ForegroundColor Cyan
                
                if ($result.Status -eq "UnknownError") {
                    Write-Host "注意: 自签名证书会显示 UnknownError 状态，这是正常现象" -ForegroundColor Yellow
                }
            } else {
                Write-Host "✗ 签名失败: $($result.Status)" -ForegroundColor Red
                if ($result.StatusMessage) {
                    Write-Host "状态消息: $($result.StatusMessage)" -ForegroundColor Red
                }
            }
        }
        catch {
            Write-Host "✗ 签名过程中发生错误: $($_.Exception.Message)" -ForegroundColor Red
            Write-Host "错误类型: $($_.Exception.GetType().Name)" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "✗ 签名过程中发生错误: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "错误类型: $($_.Exception.GetType().Name)" -ForegroundColor Red
    }
} else {
    Write-Host "错误: 找不到文件 $ExePath" -ForegroundColor Red
    exit 1
}

Write-Host "`n注意: 自签名证书不能消除 SmartScreen 警告，仅用于标识发布者。" -ForegroundColor Yellow
Write-Host "要完全消除警告，需要购买商业代码签名证书。" -ForegroundColor Yellow