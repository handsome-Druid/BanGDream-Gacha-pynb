# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['Ui_gacha_gui.py'],
    pathex=[],
    binaries=[],
    datas=[('res', 'res')],
    hiddenimports=['font_loader', 'bangdreamgacha_numba', 'ipaddress', 'pkg_resources', 'pkg_resources._vendor.jaraco.functools', 'pkg_resources._vendor.jaraco.context', 'pkg_resources._vendor.jaraco.text'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['rthook_ipaddress.py'],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=True,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='gacha_release',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['res\\tex_tiket_star5_R.ico'],
)
