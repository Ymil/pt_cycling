# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['server\\main.py'],
             pathex=['c:\\program files\\python38\\lib','c:\\program files\\python38\\lib\site-packages','..\\..\\display7\\Lib\\site-packages\\', 'C:\\Users\\escritorio\\workspace\\pt_cycling\\client'],
             binaries=[],
             datas=[('gui', 'gui'), ('server', 'server'),('server/user_config.json', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
