from distutils.core import setup 

setup(
    name='jarvisapi',
    packages=['jarvisapi'],
    version='0.6',
    license='MIT',
    description='This is the api used for a small WIP project.',
    author='bossauh',
    author_email='philmattdev@gmail.com',
    url='https://github.com/bossauh/jarvisapi',
    download_url='https://github.com/bossauh/jarvisapi/archive/v0.6-beta.tar.gz',
    keywords=['jarvis', 'voice assistant'],
    install_requires=[
        'requests',
        'nltk',
        'colorama',
        'termcolor'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]
)
