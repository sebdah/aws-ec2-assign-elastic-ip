""" Assign EC2 Elastic IP to the current instance """
import logging
import logging.config
import sys

if sys.platform in ['win32', 'cygwin']:
    import ntpath as ospath
else:
    import os.path as ospath

from netaddr import IPNetwork, AddrFormatError, AddrConversionError
from boto3 import resource, client
from ec2_metadata import ec2_metadata

from aws_ec2_assign_elastic_ip.command_line_options import ARGS as args


logging.config.fileConfig('{0}/logging.conf'.format(
    ospath.dirname(ospath.realpath(__file__))))

logger = logging.getLogger('aws-ec2-assign-eip')

region = args.region

if not region:
    region = ec2_metadata.region

# Connect to AWS EC2
if args.access_key or args.secret_key:
    # Use command line credentials
    ec2_resource = resource('ec2',
        region_name=region,
        aws_access_key_id=args.access_key,
        aws_secret_access_key=args.secret_key)
    ec2_client = client('ec2',
        region_name=region,
        aws_access_key_id=args.access_key,
        aws_secret_access_key=args.secret_key)
else:
    # Use environment vars or global boto configuration or instance metadata
    ec2_resource = resource('ec2', region_name=region)
    ec2_client = client('ec2', region_name=region)

logger.info('Connected to AWS EC2 in {0}'.format(region))


def main():
    """ Main function """
    # Get our instance name
    instance_id = ec2_metadata.instance_id

    # Check if the instance already has an Elastic IP
    # If so, exit
    if _has_associated_address(instance_id):
        logger.warning(
            '{0} is already assigned an Elastic IP. Exiting.'.format(
            instance_id))
        sys.exit(0)

    # Get an unassigned Elastic IP
    address = _get_unassociated_address()

    # Exit if there were no available Elastic IPs
    if not address:
        sys.exit(1)

    # Assign the Elastic IP to our instance
    if args.dry_run:
        logger.info('Would assign IP {0}'.format(address.public_ip))
    else:
        _assign_address(instance_id, address)


def _assign_address(instance_id, address):
    """ Assign an address to the given instance ID

    :type instance_id: str
    :param instance_id: Instance ID
    :type address: EC2.VpcAddress or EC2.ClassicAddress
    :param address: Elastic IP address
    :returns: None
    """
    logger.debug('Trying to associate {0} with {1}'.format(
        instance_id, address.public_ip))

    # Check if this is an VPC or standard allocation
    try:
        if address.domain == 'standard':
            # EC2 classic association
            address.associate(
                InstanceId=instance_id,
                AllowReassociation=False)
        else:
            # EC2 VPC association
            address.associate(
                AllocationId=address.allocation_id,
                InstanceId=instance_id,
                AllowReassociation=False)
    except Exception as error:
        logger.error('Failed to associate {0} with {1}. Reason: {2}'.format(
            instance_id, address.public_ip, error))
        sys.exit(1)

    logger.info('Successfully associated Elastic IP {0} with {1}'.format(
        address.public_ip, instance_id))


def _get_unassociated_address():
    """ Return the first unassociated EIP we can find

    :returns: EC2.VpcAddress or EC2.ClassicAddress or None
    """
    eip = None

    for address in ec2_client.describe_addresses().get('Addresses', []):
        # Check if the address is associated
        if address.get('InstanceId'):
            logger.debug('{0} is already associated with {1}'.format(
                address.get('PublicIp', ''), address.get('InstanceId', '')))
            continue

        # Check if the address is attached to an ENI
        if address.get('NetworkInterfaceId'):
            logger.debug('{0} is already attached to {1}'.format(
                address.get('PublicIp', ''),
                address.get('NetworkInterfaceId', '')))
            continue

        # Check if the address is in the valid IP's list
        if _is_valid(address.get('PublicIp')):
            logger.debug('{0} is unassociated and OK for us to take'.format(
                address.get('PublicIp', '')))

            if (address.get('Domain') == 'vpc'):
                eip = ec2_resource.VpcAddress(address.get('AllocationId'))
            else:
                eip = ec2_resource.ClassicAddress(address.get('AllocationId'))

            break

        else:
            logger.debug(
                '{0} is unassociated, but not in the valid IPs list'.format(
                    address.get('PublicIp', '')))

    if not eip:
        logger.error('No unassociated Elastic IP found!')

    return eip


def _has_associated_address(instance_id):
    """ Check if the instance has an Elastic IP association

    :type instance_id: str
    :param instance_id: Instances ID
    :returns: bool -- True if the instance has an Elastic IP associated
    """
    if ec2_client.describe_addresses(
        Filters=[{'Name':'instance-id', 'Values':[instance_id]}]).get('Addresses'):

        return True
    return False

def _is_ip_in_range(address, ips):
    """ Check if the IP is in a given range.

    :type address: str
    :param address: IP address to check
    :type ips: str
    :param ips: IP range
    :returns: bool -- True if association is OK
    """
    if not ips:
        return True

    for conf_ip in ips.split(','):
        try:
            for ip in IPNetwork(conf_ip):
                if str(ip) == str(address):
                    return True

        except AddrFormatError as err:
            logger.error('Invalid valid IP configured: {0}'.format(err))
            pass

        except AddrConversionError as err:
            logger.error('Invalid valid IP configured: {0}'.format(err))
            pass

    return False


def _is_valid(address):
    """ Check if the configuration allows us to assign this address

    :type address: str
    :param address: IP address to check
    :returns: bool -- True if association is OK
    """
    if _is_ip_in_range(address, args.valid_ips):
        if args.invalid_ips and _is_ip_in_range(address, args.invalid_ips):
            return False
        else:
            return True

    return False
