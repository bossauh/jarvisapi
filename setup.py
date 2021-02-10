from distutils.core import setup 

setup(
    name='jarvisapi',
    packages=['jarvisapi'],
    version='0.1',
    license='MIT',
    description='This is the api used for a small WIP project.',
    author='bossauh',
    author_eemail='philmattdev@gmail.com',
    url='https://github.com/bossauh/jarvisapi',
    download_url='https://github.com/bossauh/jarvisapi/archive/v0.1-beta.tar.gz',
    keywords=['jarvis', 'voice assistant'],
    instal_requires=[
        'requests',
        'nltk'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]
)
