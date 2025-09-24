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