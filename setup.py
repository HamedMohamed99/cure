import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

includefiles = [ 'templates', 'static', 'data.db' ,'requirements.txt']

includes = [ 'jinja2' , 'jinja2.ext']

excludes = ['Tkinter']

setup(

    name='cure',

    version = '0.1',

    description = 'cure',

    options = {'build_exe': {'excludes':excludes,'include_files':includefiles, 'includes':includes}},

    executables = [Executable('app.py')]
)

