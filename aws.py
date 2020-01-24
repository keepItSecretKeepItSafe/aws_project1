
import boto3

if __name__ == '__main__':
	session = boto3.Session(profile_name='drake')
	ec2 = session.resource('ec2')
	print(ec2.instances.all())

