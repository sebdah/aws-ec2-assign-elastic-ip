""" Setup script for PyPI """
import os
from setuptools import setup
try:
    from ConfigParser import SafeConfigParser
except ImportError:
    from configparser import SafeConfigParser

settings = SafeConfigParser()
settings.read(os.path.realpath('aws_ec2_assign_elastic_ip/settings.conf'))

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='aws-ec2-assign-elastic-ip',
    version=settings.get('general', 'version'),
    license='Apache License, Version 2.0',
    description='Automatically assign Elastic IPs to AWS EC2 instances',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Sebastian Dahlgren, Skymill Solutions',
    author_email='sebastian.dahlgren@skymill.se',
    url='https://github.com/skymill/aws-ec2-assign-elastic-ip',
    keywords="aws amazon web services ec2 as elasticip eip",
    platforms=['Any'],
    packages=['aws_ec2_assign_elastic_ip'],
    scripts=['aws-ec2-assign-elastic-ip'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['boto >= 2.36.0', 'netaddr >= 0.7.12'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ]
)
