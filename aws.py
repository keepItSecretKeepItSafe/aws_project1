import click
import boto3

session = boto3.Session(profile_name='drake')
ec2 = session.resource('ec2')

def filter_instances(project):
	instances = []
	if project:
		filters = [{'Name':'tag:Project', 'Values':["test"]}]
		instances = ec2.instances.filter(Filters=filters)
	else:
		instances = ec2.instances.all()
	return instances

@click.group()
def instances():
	"""Commands for instances"""

@instances.command('list')
@click.option('--project', default=None, help="Only instances for project (tag Project:<name>)")
def list_instance(project):
	"List EC2 instances"
	instances = filter_instances(project)
	for i in instances:
		tags = {t['Key']: t['Value'] for t in i.tags or []}
		print(', '.join((
			"\n" +
			"id: " + i.id + "\n" +
			"placement: " + i.placement['AvailabilityZone'] + "\n" +
			"public_dns_name: " + i.public_dns_name + "\n" +
			"tags: " + tags.get('Project', '<no tags>') + "\n" +
			"instance_type: " + i.instance_type,
			"\n")))
	return

@instances.command('stop')
@click.option("--project", default=None, help="Only instances for project")
def stop_instances(project):
	"Stop EC2 instances"
	instances = filter_instances(project)
	for i in instances:
		print("Stopping {0}...".format(i.id))
		i.stop()
	return


@instances.command('start')
@click.option("--project", default=None, help="Only instances for project")
def start_instances(project):
	"Start EC2 instances"
	instances = filter_instances(project)
	for i in instances:
		print("Starting {0}...".format(i.id))
		i.start()
	return

if __name__ == '__main__':
	instances()



