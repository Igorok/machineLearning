# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

setup(
    name='machineLearning',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'feedparser',
        'Pillow',
        'bs4',
        
        # 'ipython',
        # 'jupyter',
        # 'pandas',
        # 'sympy',
        # 'nose'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)