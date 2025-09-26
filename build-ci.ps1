# CI 构建脚本 - 适用于 GitHub Actions 自动化构建
# 基于原始 build.ps1，但移除交互和环境检测部分

param(
    [string]$CondaEnv = "gacha-env"
)

Write-Host "🚀 开始自动化构建流程..." -ForegroundColor Cyan

# 设置错误处理
$ErrorActionPreference = "Stop"

try {
    # 1. 激活 Conda 环境（在 CI 中已经激活）
    Write-Host "📦 当前环境信息:" -ForegroundColor Yellow
    conda info --envs
    python --version
    pip list | Select-String -Pattern "(pyqt5|pyinstaller|numba|numpy)"

    # 2. 生成 UI 文件
    Write-Host "🎨 生成界面文件..." -ForegroundColor Yellow
    if (Test-Path ".\gacha_gui.ui") {
        pyuic5 .\gacha_gui.ui -x -o .\Ui_gacha_gui.py
        Write-Host "✓ UI 文件已生成: Ui_gacha_gui.py" -ForegroundColor Green
    } else {
        Write-Warning "⚠ 未找到 gacha_gui.ui 文件"
    }

    # 3. 生成资源文件
    Write-Host "📁 生成资源文件..." -ForegroundColor Yellow
    if (Test-Path ".\res.qrc") {
        pyrcc5 .\res.qrc -o .\res_rc.py
        Write-Host "✓ 资源文件已生成: res_rc.py" -ForegroundColor Green
    } else {
        Write-Warning "⚠ 未找到 res.qrc 文件"
    }

    # 4. 清理旧的构建文件
    Write-Host "🧹 清理旧构建文件..." -ForegroundColor Yellow
    @("build", "dist", "__pycache__") | ForEach-Object {
        if (Test-Path $_) {
            Remove-Item $_ -Recurse -Force
            Write-Host "✓ 已清理: $_" -ForegroundColor Green
        }
    }

    # 5. 使用 PyInstaller 打包
    Write-Host "📦 开始 PyInstaller 打包..." -ForegroundColor Yellow
    if (Test-Path ".\release.spec") {
        pyinstaller --clean --noconfirm .\release.spec
        Write-Host "✓ PyInstaller 打包完成" -ForegroundColor Green
    } else {
        throw "未找到 release.spec 文件"
    }

    # 6. 验证构建结果
    Write-Host "🔍 验证构建结果..." -ForegroundColor Yellow
    $exePath = ".\dist\release.exe"
    if (Test-Path $exePath) {
        $fileInfo = Get-Item $exePath
        $sizeInMB = [math]::Round($fileInfo.Length / 1MB, 2)
        Write-Host "✓ 可执行文件构建成功!" -ForegroundColor Green
        Write-Host "  📍 位置: $exePath" -ForegroundColor Cyan
        Write-Host "  📊 大小: $sizeInMB MB" -ForegroundColor Cyan
        Write-Host "  🕐 修改时间: $($fileInfo.LastWriteTime)" -ForegroundColor Cyan
    } else {
        throw "构建失败: 未找到可执行文件 $exePath"
    }

    # 7. 列出构建产物
    Write-Host "📋 构建产物清单:" -ForegroundColor Yellow
    if (Test-Path ".\dist\") {
        Get-ChildItem ".\dist\" -Recurse | Where-Object { -not $_.PSIsContainer } | ForEach-Object {
            $relativePath = $_.FullName.Substring((Get-Location).Path.Length + 1)
            $sizeInKB = [math]::Round($_.Length / 1KB, 1)
            Write-Host "  📄 $relativePath ($sizeInKB KB)" -ForegroundColor White
        }
    }

    Write-Host ""
    Write-Host "🎉 构建流程完成!" -ForegroundColor Green
    Write-Host "✨ 可执行文件已准备就绪，位于: .\dist\release.exe" -ForegroundColor Cyan

} catch {
    Write-Host ""
    Write-Host "❌ 构建过程中出现错误:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "📋 错误排查建议:" -ForegroundColor Yellow
    Write-Host "1. 检查所有依赖是否正确安装 (pyqt5, pyinstaller, numba, numpy)" -ForegroundColor White
    Write-Host "2. 确认 .ui 和 .qrc 文件存在且格式正确" -ForegroundColor White
    Write-Host "3. 查看详细错误日志以获取更多信息" -ForegroundColor White
    Write-Host "4. 尝试手动运行各个步骤以定位问题" -ForegroundColor White
    exit 1
}