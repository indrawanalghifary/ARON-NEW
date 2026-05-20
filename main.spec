# -*- mode: python ; coding: utf-8 -*-
import sys

# Atur icon berdasarkan sistem operasi
if sys.platform == 'darwin':
    app_icon = None         # Tidak menggunakan icon untuk Mac
else:
    app_icon = 'arron.ico'  # Menggunakan icon .ico untuk Windows / Linux

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=app_icon, # Menggunakan variabel icon yang sudah disesuaikan
)

# Konfigurasi khusus untuk membungkus aplikasi menjadi format .app di Mac
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='main.app',
        icon=None, # Set None karena tidak ada file .icns
        bundle_identifier='com.yourdomain.main',
        info_plist={
            'NSPrincipalClass': 'NSApplication',
            'NSAppleScriptEnabled': False,
        }
    )
    
