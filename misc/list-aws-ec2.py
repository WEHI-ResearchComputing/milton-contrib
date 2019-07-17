"""

A sample script to list EC2 instances on an AWS region using MFA.

Your python environment needs boto3 and prettytable.

create ~/.aws/config that looks like
[default]
region_name=ap-southeast-2
output=json

create ~/.aws/credentials that looks
[default]
aws_access_key_id = <your id>
aws_secret_access_key = <your secret>

Other than the token, the default will work against an WEHI provisioned account.

python3 list-aws-ec2.py --token <token>
"""


import boto3
import os
from argparse import ArgumentParser
import sys
from prettytable import PrettyTable

def build_parser():
  parser = ArgumentParser()
  parser.add_argument('--token',
                      help='MFA token (required)',
                      default=None,
                      dest='token',
                      type=int,
                      required=False)
  parser.add_argument('--account',
                      dest='account',
                      help='AWS account number. Default: 581002922631',
                      default='581002922631',
                      required=False)
  parser.add_argument('--profile',
                      dest='profile',
                      default='default',
                      help='the entry in ~/.aws/credentials that has the relevant AWS keys. Default is default',
                      required=False)
  parser.add_argument('--user',
                      dest='user',
                      default=os.environ['USER'],
                      help='The user name. Default: ' + os.environ['USER'],
                      required=False)
  return parser

options = build_parser().parse_args(args=sys.argv[1:])

mfa = str(options.token)
device_id = 'arn:aws:iam::{account}:mfa/{user}'.format(user=options.user, account=options.account)

sts_client = boto3.client('sts')

credentials = sts_client.get_session_token(
  DurationSeconds=3600,
  SerialNumber=device_id,
  TokenCode=mfa
)

session = boto3.session.Session(
    aws_access_key_id=credentials['Credentials']['AccessKeyId'],
    aws_secret_access_key=credentials['Credentials']['SecretAccessKey'],
    aws_session_token=credentials['Credentials']['SessionToken']
)

ec2 = session.resource('ec2')
instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

out = PrettyTable(['ID', 'Name', 'Type', 'External IP'])
out.padding_width = 1

for instance in instances:
  ip = instance.network_interfaces_attribute[0]['PrivateIpAddresses'][0]['Association']['PublicDnsName']
  out.add_row((instance.instance_id, instance.key_name, instance.instance_type, ip))

print(out)
