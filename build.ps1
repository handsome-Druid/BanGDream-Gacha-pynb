conda env create -f environment.yml
conda activate gacha-env
pyuic5 .\gacha_gui.ui -x -o .\Ui_gacha_gui.py
pyrcc5 .\res.qrc -o .\res_rc.py
pyinstaller --clean .\release.spec