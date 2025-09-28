# BanG Dream! Gacha Simulator 构建脚本
# 适用于 PowerShell 7+ 环境

# 兼容 PowerShell 5.1 的编码设置
if ($PSVersionTable.PSVersion.Major -lt 7) {
    try {
        if ((chcp) -notmatch '65001') { chcp 65001 > $null }
        [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
        $OutputEncoding = [System.Text.Encoding]::UTF8
    } catch {}
}

# 版本自动递增函数
function Update-VersionInfo {
    param(
        [string]$VersionFilePath = ".\version_info.txt"
    )
    
    if (-Not (Test-Path $VersionFilePath)) {
        Write-Host "✗ 版本信息文件不存在: $VersionFilePath" -ForegroundColor Red
        return $false
    }
    
    try {
        # 读取版本信息文件
        $content = Get-Content $VersionFilePath -Raw -Encoding UTF8
        
        # 使用正则表达式查找版本号
        $versionPattern = 'filevers=\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)'
        $prodVersionPattern = 'prodvers=\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)'
        $fileVersionPattern = "StringStruct\('FileVersion',\s*'(\d+)\.(\d+)\.(\d+)\.(\d+)'\)"
        $productVersionPattern = "StringStruct\('ProductVersion',\s*'(\d+)\.(\d+)\.(\d+)\.(\d+)'\)"
        
        # 获取当前版本号
        if ($content -match $versionPattern) {
            $major = [int]$matches[1]
            $minor = [int]$matches[2]
            $build = [int]$matches[3]
            $revision = [int]$matches[4]
            
            # 递增构建版本号（第三位），修订版本号重置为0
            $newBuild = $build + 1
            $newRevision = 0
            $newVersionString = "$major.$minor.$newBuild.$newRevision"
            
            Write-Host "版本更新: $major.$minor.$build.$revision -> $newVersionString" -ForegroundColor Green
            
            # 更新 filevers
            $content = $content -replace $versionPattern, "filevers=($major, $minor, $newBuild, $newRevision)"
            
            # 更新 prodvers
            $content = $content -replace $prodVersionPattern, "prodvers=($major, $minor, $newBuild, $newRevision)"
            
            # 更新 FileVersion
            $content = $content -replace $fileVersionPattern, "StringStruct('FileVersion', '$newVersionString')"
            
            # 更新 ProductVersion
            $content = $content -replace $productVersionPattern, "StringStruct('ProductVersion', '$newVersionString')"
            
            # 写回文件
            $content | Set-Content $VersionFilePath -Encoding UTF8
            
            Write-Host "✓ 版本信息已更新为: $newVersionString" -ForegroundColor Green
            return $newVersionString
        } else {
            Write-Host "✗ 无法解析版本信息" -ForegroundColor Red
            return $false
        }
    } catch {
        Write-Host "✗ 更新版本信息时出错: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

Write-Host "🚀 开始构建 BanG Dream! Gacha Simulator" -ForegroundColor Cyan

# 0. 自动更新版本号
Write-Host "📝 更新版本号..." -ForegroundColor Yellow
$newVersion = Update-VersionInfo
if (-Not $newVersion) {
    Write-Host "⚠ 版本更新失败，继续构建..." -ForegroundColor Yellow
}

# 1. 创建并激活环境
if (-Not (Test-Path "C:\Users\$env:USERNAME\.conda\envs\gacha-env")) {
    conda init ; conda env create -f environment.yml -n gacha-env
}

conda activate gacha-env


# 2. 生成 UI
if (Test-Path ".\gacha_gui.ui") {
    pyuic5 .\gacha_gui.ui -x -o .\Ui_gacha_gui.py
}

# 3. 生成资源文件
if (Test-Path ".\res.qrc") {
    pyrcc5 .\res.qrc -o .\res_rc.py
}

# 4. 打包
pyinstaller --clean .\release.spec

# 5. 自动签名
$exePath = ".\dist\release.exe"
if (Test-Path $exePath) {
    Write-Host "🔐 开始对可执行文件进行自签名..." -ForegroundColor Cyan
    .\sign_exe.ps1 -ExePath $exePath
    
    # 显示文件大小信息
    $fileSize = (Get-Item $exePath).Length
    $fileSizeMB = [math]::Round($fileSize / 1MB, 2)
    Write-Host "📦 构建完成！文件大小: $fileSizeMB MB" -ForegroundColor Green
    
    if ($newVersion) {
        Write-Host "🎉 版本 $newVersion 构建成功！" -ForegroundColor Green
    }
} else {
    Write-Host "✗ 找不到可执行文件: $exePath" -ForegroundColor Red
    exit 1
}