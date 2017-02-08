import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.md')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'waitress',
    'bson',
    'pymongo',
    'mongoengine',
    'marshmallow',
    'WebTest >= 1.3.1',  # py3 compat
    'nose2',
    'cov-core'
]

setup(
    name='stackcite.api',
    version='0.0',
    description='The REST API web application for Stackcite.',
    long_description=README + '\n\n' + CHANGES,
    author='Konrad R.K. Ludwig',
    author_email='konrad.rk.ludwig@gmail.com',
    url='http://www.konradrkludwig.com/',
    packages=find_packages(),
    namespace_packages=['stackcite'],
    install_requires=requires,
    classifiers=[
    "Programming Language :: Python",
    "Framework :: Pyramid",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    keywords='web pyramid pylons',
    include_package_data=True,
    zip_safe=False,
    entry_points="""\
    [paste.app_factory]
    main = stackcite.api:main
    """,
)
