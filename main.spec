# -*- mode: python ; coding: utf-8 -*-
import sys
import os


PATH = os.path.dirname(os.path.abspath("__file__"))

block_cipher = None

assets = [
	('data/assets/fonts', 'data/assets/fonts'),

]

a = Analysis(['main.py'],
             pathex=[PATH],
             binaries=[],
             datas=assets,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['numpy', 'pandas', 'scipy'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Particle Simulator',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
