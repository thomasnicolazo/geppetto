import paramiko
import logging
import os
import sys
import argparse
import yaml

import logger.logger_formater as formater

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#client.load_system_host_keys()
# private_key_path = '/path/to/private_key'
# private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
# ssh.connect('hostname', username='username', pkey=private_key)
client.connect('scp721', username='thomas', password='test')
stdin, stdout, stderr = client.exec_command('ls')
print(stdout.read().decode())
client.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='geppetto.py', usage='%(prog)s [options]')
    parser.add_argument( '-c', '--config-file', help='path to the config file ',default="config.yaml")
    parser.add_argument('-t', '--test', help='run test script for scripts in config file', action='store_true')
    args = parser.parse_args()
    logger = logging.getLogger(__name__)
    #logging.basicConfig(level=logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formater.CustomFormatter())
    logger.addHandler(handler)
    if not os.path.exists(args.config_file):
        raise FileNotFoundError(args.config_file)
        exit(1)
    with open(args.config_file, 'r') as conf_file:
        try:
            yaml_cfg = yaml.safe_load(conf_file)
        except yaml.YAMLError as exc:
            logger.error(exc)

    machines = yaml_cfg['machines']
