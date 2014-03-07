""" Command line parser """
import argparse

PARSER = argparse.ArgumentParser(
    description='Assign EC2 Elastic IP to the current instance')
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
    '--ips',
    help='A comma separated list of valid Elastic IPs. Default: any')
ARGS = PARSER.parse_args()
