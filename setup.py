from distutils.core import setup

with open('README') as file:
    long_description = file.read()

setup(
    name='pgpsubmit',
    version='0.3',
    description='WSGI PGP public key submission system',
    author='Fraser Tweedale',
    author_email='frase@frase.id.au',
    url='https://gitorious.org/pgpsubmit',
    packages=['pgpsubmitlib'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Communications :: Email',
        'Topic :: Security :: Cryptography',
    ],
    long_description=long_description,
)
