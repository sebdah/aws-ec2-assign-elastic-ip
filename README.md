aws-ec2-assign-elastic-ip
=========================

Automatically assign Elastic IPs to AWS EC2 instances. This can be really nice in auto scaling groups were you need to communicate the external IP's to third party systems.

The script should be executed on the EC2 instance that should get assigned an Elastic IP. This is typically done as part of the instance boot process.

Installation
------------

`aws-ec2-assign-elastic-ip` is easiest to install via PyPI.

    pip install aws-ec2-assign-elastic-ip

Configuration options
---------------------

The script is configured using command line options. You can provide your AWS credentials directly on the command line, but the script also supports all [boto credential config options](http://boto.readthedocs.org/en/latest/boto_config_tut.html#credentials).

    usage: aws-ec2-assign-elastic-ip [-h] [--version] [--region REGION]
                                     [--access-key ACCESS_KEY]
                                     [--secret-key SECRET_KEY]
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
      --valid-ips VALID_IPS
                            A comma separated list of valid Elastic IPs. Default
                            is to try all IPs. Example:
                            56.123.56.123,56.123.56.124,56.123.56.125

The `--valid-ips` option require the public IPs in a comma separated sequence. E.g. `56.123.56.123,56.123.56.124,56.123.56.125`.

Supported platforms
-------------------

The `aws-ec2-assign-elastic-ip` should work fine on Linux, Mac OS X and Microsoft Windows. Please submit an issue if you have any issues with any of the platforms.

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
