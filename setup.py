from setuptools import setup

setup(
    name='Terminal manager',
    version='0.1',
    py_modules=['tman'],
    install_requires=[
        'Click',
        'PyYAML'
    ],
    entry_points='''
        [console_scripts]
        tman=tman:cli
    ''',
)