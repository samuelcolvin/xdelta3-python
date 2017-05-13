from importlib.machinery import SourceFileLoader
from pathlib import Path
from setuptools import setup, Extension

THIS_DIR = Path(__file__).resolve().parent
long_description = THIS_DIR.joinpath('README.rst').read_text()

# avoid loading the package before requirements are installed:
version = SourceFileLoader('version', 'xdelta3/version.py').load_module()

setup(
    name='xdelta3',
    version=str(version.VERSION),
    description='Fast delta encoding using xdelta3',
    long_description=long_description,
    author='Samuel Colvin',
    author_email='s@muelcolvin.com',
    url='https://github.com/samuelcolvin/xdelta3',
    license='MIT',
    packages=['xdelta3'],
    zip_safe=True,
    ext_modules=[
        Extension(
            '_xdelta3',
            sources=['xdelta3/_xdelta3.c'],
            include_dirs=['./xdelta/xdelta3'],
            define_macros=[
                ('SIZEOF_SIZE_T', '8'),
                ('SIZEOF_UNSIGNED_LONG_LONG', '8'),
                ('XD3_USE_LARGEFILE64', '1'),
            ]
        )
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX :: Linux',
    ],
)
