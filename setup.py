from setuptools import setup, find_packages
from codecs import open

setup(name='ravepaypysdk',
      version='1.0.1',
      description='A Python library to consume the RavePay API',
      long_description=open('README.rst', 'r').read(),
      url='https://github.com/johnchuks/ravepay-python-sdk',
      author='Johnbosco Ohia',
      author_email='johnboscoohia@gmail.com',
      license='MIT',
      keywords='ravepay python library',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6'
          
      ],
      packages=find_packages(exclude=['contrib', 'tests']),
      install_requires=[
          'requests', 'pycrypto'
      ],
      test_suite='nose.collector',
      test_requires=['nose'],
      extras_require={
          'test': ['coverage']
      },
      zip_safe=False)
