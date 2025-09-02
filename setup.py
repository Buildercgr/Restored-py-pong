from setuptools import setup

APP = ['py_pong.py']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['pygame'],
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
)
