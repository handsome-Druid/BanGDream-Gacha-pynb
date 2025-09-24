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
    Write-Host "开始对可执行文件进行自签名..." -ForegroundColor Cyan
    .\sign_exe.ps1 -ExePath $exePath
} else {
    Write-Host "✗ 找不到可执行文件: $exePath" -ForegroundColor Red
}