""" Assign EC2 Elastic IP to the current instance """
import logging
import logging.config
import sys

if sys.platform in ['win32', 'cygwin']:
    import ntpath as ospath
else:
    import os.path as ospath

import boto.utils
from boto.ec2 import connect_to_region
from boto.utils import get_instance_metadata

from aws_ec2_assign_elastic_ip.command_line_options import ARGS as args


logging.config.fileConfig('{0}/logging.conf'.format(
    ospath.dirname(ospath.realpath(__file__))))

LOGGER = logging.getLogger('aws-ec2-assign-eip')

REGION = args.region

# Fetch instance metadata
METADATA = get_instance_metadata(timeout=1, num_retries=1)
if METADATA:
    try:
        REGION = METADATA['placement']['availability-zone'][:-1]
    except KeyError:
        pass

# Connect to AWS EC2
if args.access_key or args.secret_key:
    # Use command line credentials
    CONNECTION = connect_to_region(
        REGION,
        aws_access_key_id=args.access_key,
        aws_secret_access_key=args.secret_key)
else:
    # Use environment vars or global boto configuration or instance metadata
    CONNECTION = connect_to_region(REGION)
LOGGER.info('Connected to AWS EC2 in {0}'.format(REGION))


def main():
    """ Main function """
    # Get our instance name
    instance_id = boto.utils.get_instance_metadata()['instance-id']

    # Check if the instance already has an Elastic IP
    # If so, exit
    if _has_associated_address(instance_id):
        LOGGER.warning('{0} is already assigned an Elastic IP. Exiting.'.format(
            instance_id))
        sys.exit(0)

    # Get an unassigned Elastic IP
    address = _get_unassociated_address()

    # Exit if there were no available Elastic IPs
    if not address:
        sys.exit(1)

    # Assign the Elastic IP to our instance
    _assign_address(instance_id, address)


def _assign_address(instance_id, address):
    """ Assign an address to the given instance ID

    :type instance_id: str
    :param instance_id: Instance ID
    :type address: boto.ec2.address
    :param address: Elastic IP address
    :returns: None
    """
    LOGGER.debug('Trying to associate {0} with {1}'.format(
        instance_id, address.public_ip))

    # Check if this is an VPC or standard allocation
    try:
        if address.domain == 'standard':
            # EC2 classic association
            CONNECTION.associate_address(
                instance_id,
                public_ip=address.public_ip)
        else:
            # EC2 VPC association
            CONNECTION.associate_address(
                instance_id,
                allocation_id=address.allocation_id)
    except Exception as error:
        LOGGER.error('Failed to associate {0} with {1}. Reason: {2}'.format(
            instance_id, address.public_ip, error))
        sys.exit(1)

    LOGGER.info('Successfully associated Elastic IP {0} with {1}'.format(
        address.public_ip, instance_id))


def _get_unassociated_address():
    """ Return the first unassociated EIP we can find

    :returns: boto.ec2.address or None
    """
    eip = None
    valid_ips = _valid_ips()

    for address in CONNECTION.get_all_addresses():
        # Check if the address is associated
        if address.instance_id:
            LOGGER.debug('{0} is already associated with {1}'.format(
                address.public_ip, address.instance_id))
            continue

        # Check if the address is in the valid IP's list
        if valid_ips and address.public_ip not in valid_ips:
            LOGGER.debug(
                '{0} is unassociated, but not in the valid IPs list'.format(
                    address.public_ip, address.instance_id))
            continue

        LOGGER.debug('{0} is unassociated and OK for us to take'.format(
            address.public_ip))
        eip = address

    if not eip:
        LOGGER.error('No unassociated Elastic IP found!')

    return eip


def _has_associated_address(instance_id):
    """ Check if the instance has an Elastic IP association

    :type instance_id: str
    :param instance_id: Instances ID
    :returns: bool -- True if the instance has an Elastic IP associated
    """
    if CONNECTION.get_all_addresses(filters={'instance-id': instance_id}):
        return True
    return False


def _valid_ips():
    """ Get a list of the valid Elastic IPs to assign

    :returns: list or None
        List of IPs. If any IP is valid the function returns None
    """
    if args.valid_ips:
        ips = []

        for ip in args.valid_ips.split(','):
            ips.append(ip.strip())

        LOGGER.info('Valid IPs: {0}'.format(', '.join(ips)))
        return ips

    LOGGER.info('Valid IPs: any')
    return None
