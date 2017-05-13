from distutils.core import setup, Extension

setup(
    name='xdelta3',
    version='0.0.1',
    ext_modules=[
        Extension(
            '_xdelta3',
            sources=['xdelta3/_xdelta3.c'],
            include_dirs=['./xdelta/xdelta3'],
            define_macros=[
                ('SIZEOF_SIZE_T', '8'),
                ('SIZEOF_UNSIGNED_LONG_LONG', '8'),
                ('XD3_USE_LARGEFILE64', '1'),
                ('XD3_DEBUG', '1'),
                ('NDEBUG', '1'),
            ]
        )
    ]
)
