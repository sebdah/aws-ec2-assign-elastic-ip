""" Command line parser """
import argparse
import os.path
import sys
from ConfigParser import SafeConfigParser

SETTINGS = SafeConfigParser()
SETTINGS.read('{}/settings.conf'.format(
    os.path.dirname(os.path.realpath(__file__))))

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
    '--aws-access-key',
    help='AWS access key ID')
PARSER.add_argument(
    '--aws-secret-key',
    help='AWS secret access key ID')
PARSER.add_argument(
    '--valid-ips',
    help=(
        'A comma separated list of valid Elastic IPs. Default is to try '
        'all IPs. Example: 56.123.56.123,56.123.56.124,56.123.56.125'))
ARGS = PARSER.parse_args()

if ARGS.version:
    print('AWS EC2 Assign Elastic IP: {}'.format(
        SETTINGS.get('general', 'version')))
    sys.exit(0)
