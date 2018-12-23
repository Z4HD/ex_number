# -*- mode: python -*-

block_cipher = None

from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal, get_deps_all, hookspath, runtime_hooks
#import kivy
from kivy.deps import sdl2, glew

a = Analysis(['randEx-GUI.py'],
             pathex=['.'],
             binaries=[],
             datas=[('ui.kv','.'),('fonts\\wqy-microhei.ttc','fonts')],
             hookspath=hookspath(),
             runtime_hooks=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             **get_deps_minimal(audio=None, camera=None, clipboard=None, image=True, spelling=None, text=True, video=True, window=True))
#excludes=[],hiddenimports=[],

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          *[Tree(p) for p in(sdl2.dep_bins + glew.dep_bins)],
          name='randEx-GUI',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True)
