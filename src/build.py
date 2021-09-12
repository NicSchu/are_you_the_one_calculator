import subprocess

import PyInstaller.__main__


def build_one_file():
    PyInstaller.__main__.run([
        'calculator.py',
        '--onefile',
        '--windowed'
    ])
    subprocess.call([r'build.bat', version, '-onefile'])


def build_normal():
    PyInstaller.__main__.run([
        'calculator.py',
        '--windowed'
    ])
    subprocess.call([r'build.bat', version, ''])


if __name__ == '__main__':
    version = 'v1.0'
    build_one_file()
    build_normal()
