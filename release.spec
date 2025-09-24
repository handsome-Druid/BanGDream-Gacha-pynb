block_cipher = None

import PyQt5  # 触发 PyQt5 hook

hidden = [
    'font_loader',
    'bangdreamgacha_numba',
    'Ui_gacha_gui',
]

excludes = [
    'setuptools', 'pkg_resources', 'distutils', 'unittest', 'test', 'pydoc', 'doctest',
    'http', 'xmlrpc', 'asyncio', 'wsgiref', 'logging.config', 'logging.handlers'
]

datas = [
    ('res', 'res'),
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='release',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=['libimalloc.dll','python3.dll','icudt.dll'],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    optimize=2,
    icon=['res/tex_tiket_star5_R.ico'],
    # 添加版本信息可以降低被安全软件误报的几率
    version='version_info.txt',
)
