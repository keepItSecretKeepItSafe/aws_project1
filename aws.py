import click
import boto3

session = boto3.Session(profile_name='drake')
ec2 = session.resource('ec2')

@click.command()
def list_instance():
	for i in ec2.instances.all():
		print(', '.join((
			i.id,
			i.instance_type,
			i.state['Name'],
			i.public_dns_name)))
	return

if __name__ == '__main__':
	list_instance()

