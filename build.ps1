conda env create -f environment.yml
conda activate gacha-env
pyinstaller --clean .\release.spec