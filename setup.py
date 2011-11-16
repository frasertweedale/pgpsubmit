from distutils.core import setup

with open('README') as file:
    long_description = file.read()

setup(
    name='pgpsubmit',
    version='0.1dev',
    description='WSGI OpenPGP public key submission system',
    author='Fraser Tweedale',
    author_email='frase@frase.id.au',
    url='https://gitorious.org/pgpsubmit',
    packages=['pgpsubmitlib'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Office/Business :: Financial :: Accounting',
    ],
    long_description=long_description,
)
