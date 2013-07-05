from distutils.core import setup

with open('README.rst') as file:
    long_description = file.read()

setup(
    name='pgpsubmit',
    version='0.3.1',
    description='WSGI PGP public key submission system',
    author='Fraser Tweedale',
    author_email='frase@frase.id.au',
    url='https://github.com/frasertweedale/pgpsubmit',
    packages=['pgpsubmitlib'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Communications :: Email',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Security :: Cryptography',
    ],
    long_description=long_description,
)
