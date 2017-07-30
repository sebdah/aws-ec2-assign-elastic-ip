aws-ec2-assign-elastic-ip
=========================

[![PyPI version](https://badge.fury.io/py/aws-ec2-assign-elastic-ip.svg)](https://badge.fury.io/py/aws-ec2-assign-elastic-ip)

Automatically assign Elastic IPs to AWS EC2 instances. This can be really nice
in auto scaling groups were you need to communicate the external IP's to third
party systems.

The script should be executed on the EC2 instance that should get assigned an
Elastic IP. This is typically done as part of the instance boot process.

`aws-ec2-assign-elastic-ip` is idempotent and will not assign an new Elastic IP
if the instance already has one.

Installation
------------

`aws-ec2-assign-elastic-ip` is easiest to install via PyPI.

    pip install aws-ec2-assign-elastic-ip

Configuration options
---------------------

The script is configured using command line options. You can provide your AWS
credentials directly on the command line, but the script also supports all [boto
credential config options](http://boto.readthedocs.org/en/latest/boto_config_tut.html#credentials)
and AWS instance profiles.

    usage: aws-ec2-assign-elastic-ip [-h] [--version] [--region REGION]
                                     [--access-key ACCESS_KEY]
                                     [--secret-key SECRET_KEY] [--dry-run]
                                     [--valid-ips VALID_IPS]

    Assign EC2 Elastic IP to the current instance

    optional arguments:
      -h, --help            show this help message and exit
      --version             Print the Automated EBS Snapshots version and exit
      --region REGION       AWS region. Default: us-east-1
      --access-key ACCESS_KEY
                            AWS access key ID
      --secret-key SECRET_KEY
                            AWS secret access key ID
      --dry-run             Turn on dry run mode. No address will be assigned,
                            we will only print which we whould take
      --valid-ips VALID_IPS
                            A comma separated list of valid Elastic IPs.
                            You can use CIDR expressions to select ranges.
                            Valid examples:
                            - 58.0.0.0/8
                            - 123.213.0.0/16,58.0.0.0/8,195.234.023.0
                            - 195.234.234.23,195.234.234.24

The `--valid-ips` option require the public IPs in a comma separated sequence.
E.g. `56.123.56.123,56.123.56.124,56.123.56.125`.

Supported platforms
-------------------

The `aws-ec2-assign-elastic-ip` should work fine on Linux, Mac OS X and
Microsoft Windows. Please submit an issue if you have any issues with any of the
platforms.

We currently support Python 2.6, 2.7 and 3.X

Required IAM permissions
------------------------

**Community contribution much appreciated on this!**

We have been using the following IAM policys to be able to list and associate
Elastic IPs. This can probably be narrowed down abit. It allows EC2 read-only
(from the IAM wizard) and `ec2:AssociateAddress` permissions:

    {
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "ec2:AssociateAddress",
            "ec2:Describe*"
          ],
          "Resource": "*"
        }
      ]
    }

License
-------

    APACHE LICENSE 2.0

    Copyright 2014 Skymill Solutions

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
