from setuptools import setup

setup(
    name='ghoztrecon',
    version='1.0.0',
    py_modules=['ghozt_recon'],
    install_requires=[
        'requests',
        'colorama',
        'urllib3',
    ],
    entry_points={
        'console_scripts': [
            'ghoztrecon=ghozt_recon:main',
        ],
    },
)
