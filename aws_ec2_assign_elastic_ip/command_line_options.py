""" Command line parser """
import argparse
import sys
from ConfigParser import SafeConfigParser

if sys.platform in ['win32', 'cygwin']:
    import ntpath as ospath
else:
    import os.path as ospath

SETTINGS = SafeConfigParser()
SETTINGS.read('{0}/settings.conf'.format(
    ospath.dirname(ospath.realpath(__file__))))

PARSER = argparse.ArgumentParser(
    description='Assign EC2 Elastic IP to the current instance')
PARSER.add_argument(
    '--version',
    action='count',
    help='Print the Automated EBS Snapshots version and exit')
PARSER.add_argument(
    '--region',
    default='us-east-1',
    help='AWS region. Default: us-east-1')
PARSER.add_argument(
    '--access-key',
    help='AWS access key ID')
PARSER.add_argument(
    '--secret-key',
    help='AWS secret access key ID')
PARSER.add_argument(
    '--valid-ips',
    help=(
        'A comma separated list of valid Elastic IPs. You can use CIDR '
        'expressions to select ranges. Valid examples:'
        '58.0.0.0/8'
        '123.213.0.0/16,58.0.0.0/8,195.234.023.0'
        '195.234.234.23,195.234.234.24'))
ARGS = PARSER.parse_args()

if ARGS.version:
    print('AWS EC2 Assign Elastic IP: {0}'.format(
        SETTINGS.get('general', 'version')))
    sys.exit(0)
