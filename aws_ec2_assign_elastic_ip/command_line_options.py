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
        'A comma separated list of valid Elastic IPs. Default is to try '
        'all IPs. Example: 56.123.56.123,56.123.56.124,56.123.56.125'))
PARSER.add_argument(
    '--cidr',
    help=(
        'a CIDR expression instead of a list of ip addresses. Example: '
        '54.0.0.0/8'))
ARGS = PARSER.parse_args()

if ARGS.version:
    print('AWS EC2 Assign Elastic IP: {0}'.format(
        SETTINGS.get('general', 'version')))
    sys.exit(0)
