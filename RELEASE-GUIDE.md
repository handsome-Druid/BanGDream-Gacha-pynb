# GitHub Actions 自动化发布指南

本项目已配置 GitHub Actions 自动化构建和发布流程，每当推送新的版本标签时会自动生成 Release。

## 🚀 触发自动发布

### 方法1: 命令行发布（推荐）

```powershell
# 1. 确保代码已提交
git add .
git commit -m "feat: 新版本功能更新"
git push

# 2. 创建并推送版本标签
git tag v1.3.4  # 替换为实际版本号
git push origin v1.3.4

# 3. 稍等几分钟，GitHub Actions 会自动构建并创建 Release
```

### 方法2: GitHub 网页操作

1. 进入仓库的 **Releases** 页面
2. 点击 **"Create a new release"**
3. 在 **"Choose a tag"** 中输入新版本号（如 `v1.3.4`）
4. 填写发布说明
5. 点击 **"Publish release"**

### 方法3: 手动触发

1. 进入 **Actions** 标签页
2. 选择 **"Build and Release"** workflow
3. 点击 **"Run workflow"** 按钮
4. 选择分支并点击运行

## 📋 自动化流程说明

当推送版本标签时，GitHub Actions 会执行以下步骤：

1. **环境准备**
   - 使用 Windows Server 最新版
   - 安装 Miniconda 和 Python 3.9
   - 根据 `environment.yml` 创建构建环境

2. **代码生成**
   - 从 `gacha_gui.ui` 生成 `Ui_gacha_gui.py`
   - 从 `res.qrc` 生成 `res_rc.py`

3. **构建打包**
   - 使用 PyInstaller 根据 `release.spec` 打包
   - 生成单文件可执行程序

4. **代码签名**
   - 创建自签名证书
   - 对可执行文件进行代码签名（减少安全警告）

5. **发布上传**
   - 自动创建 GitHub Release
   - 上传构建好的 `.exe` 文件
   - 包含版本说明和使用指南

## 🔧 版本号规范

建议使用 [语义化版本](https://semver.org/lang/zh-CN/) 格式：

- `v1.0.0` - 主版本号.次版本号.修订号
- `v1.3.4` - 功能更新示例
- `v2.0.0` - 重大更新示例

## 📁 构建产物

每次成功构建后，Release 页面会包含：

- `BanGDream-Gacha-v{版本号}.exe` - 主程序
- `README.md` - 项目说明
- `LICENSE` - 开源协议
- `版本说明.txt` - 构建信息和使用说明

## 🛠️ 自定义构建

如需修改构建流程，可以编辑以下文件：

- `.github/workflows/release.yml` - GitHub Actions 工作流配置
- `build-ci.ps1` - CI 环境构建脚本
- `release.spec` - PyInstaller 打包配置

## ⚠️ 注意事项

1. **版本标签格式**: 必须以 `v` 开头（如 `v1.3.4`）
2. **构建时间**: 完整构建需要约 3-5 分钟
3. **代码签名**: 使用自签名证书，首次运行仍可能有安全提示
4. **依赖管理**: 确保 `environment.yml` 包含所有必需依赖
5. **文件权限**: 确保 UI 和资源文件可读

## 🔍 故障排查

### 构建失败

1. 查看 **Actions** 标签页中的构建日志
2. 检查是否有语法错误或导入问题
3. 确认所有依赖在 `environment.yml` 中正确配置

### Release 创建失败

1. 检查仓库是否有创建 Release 的权限
2. 确认标签格式正确（必须以 `v` 开头）
3. 查看 workflow 权限设置

### 可执行文件问题

1. 在本地使用 `build-ci.ps1` 测试构建
2. 检查 `release.spec` 配置
3. 确认所有资源文件正确打包

## 📞 支持

如遇到问题，可以：

1. 查看 GitHub Actions 运行日志
2. 在 Issues 中报告问题
3. 参考原始 `build.ps1` 脚本进行本地调试