from setuptools import setup, find_packages

setup(
    name='indent_print',
    version='1.1.0',
    description='library can print better readable code',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='matin ahmadi',
    author_email='matinahmadi.programmer@gmail.com',
    url='https://github.com/matinprogrammer/IPrint',
    packages=find_packages(),
    install_requires=[

    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6'
)
