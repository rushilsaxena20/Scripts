import paramiko
import time

# key_name = ''
# PRIVATE_KEY_FILE = f'/Users/rushilsaxena/Downloads/awskeys/{key_name}'
PRIVATE_KEY_FILE = f'/Users/rushilsaxena/Downloads/awskeys/dc5-microservice.pem'
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# pkey = paramiko.RSAKey.from_private_key_file(PRIVATE_KEY_FILE)
ips = ["10.24.123.223", "10.24.147.83", "10.24.44.24", "10.24.38.218"]
for ip in ips:
    try:
        # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
        ssh_client.connect(hostname=ip, username="ec2-user", key_filename=PRIVATE_KEY_FILE, banner_timeout=1000)

        # Execute a command(cmd) after connecting/ssh to an instance
        stdin, stdout, stderr = ssh_client.exec_command('cat /etc/os-release')
        stdin1, stdout1, stderr1 = ssh_client.exec_command('uname -r')
        stdin.close()
        stdin1.close()
        # print(stdout.read().decode())
        op = stdout.read().decode().splitlines()
        op1 = stdout1.read().decode().splitlines()
        print(op[0], op[1], end=' ')
        print(op1)

        # close the client connection once the job is done
        ssh_client.close()
    except Exception as e:
        try:
            ssh_client.connect(hostname=ip, username="ubuntu",banner_timeout=1000, key_filename=PRIVATE_KEY_FILE)

            # Execute a command(cmd) after connecting/ssh to an instance
            stdin, stdout, stderr = ssh_client.exec_command('cat /etc/os-release')
            stdin1, stdout1, stderr1 = ssh_client.exec_command('uname -r')
            stdin.close()
            stdin1.close()
            # print(stdout.read().decode())
            op = stdout.read().decode().splitlines()
            op1 = stdout1.read().decode().splitlines()
            print(op[0], op[1], end=' ')
            print(op1)

            # close the client connection once the job is done
            ssh_client.close()
        except:
            print(f'Can not connnect to {ip}')
