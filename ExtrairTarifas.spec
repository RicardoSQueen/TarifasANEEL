# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['ExtrairTarifas.py'],
             pathex=['C:\\Users\\rsq5\\Energisa\\Comercial - General\\Tarifas'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
a.datas += [('energisa-comercializadora.png','C:\\Users\\rsq5\\Energisa\\Comercial - General\\Tarifas\\energisa-comercializadora.png','DATA'),('icone.png','C:\\Users\\rsq5\\Energisa\\Comercial - General\\Tarifas\\icone.png','DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='ExtrairTarifas',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
