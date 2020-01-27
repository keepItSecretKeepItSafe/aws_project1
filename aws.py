import click
import botocore
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
def cli():
	"""Custom AWS CLI library"""

@cli.group('instances')
def instances():
	"""Commands for instances"""

@cli.group('volumes')
def volumes():
	"""Commands for volumes"""

@cli.group('snapshots')
def snapshots():
	"""Commands for snapshots"""

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
		try:
			i.stop()
		except botocore.exceptions.Clienterror as e:
			print("Could not stop {0}".format(i.id) + str(e))
			continue
	return


@instances.command('start')
@click.option("--project", default=None, help="Only instances for project")
def start_instances(project):
	"Start EC2 instances"
	instances = filter_instances(project)
	for i in instances:
		print("Starting {0}...".format(i.id))
		try:
			i.start()
		except botocore.exceptions.Clienterror as e:
			print("Could not start {0}".format(i.id) + str(e))
			continue
	return

@instances.command('snapshot', help="Create snapshots of all volumes")
@click.option('--project', default=None, help="Only volumes for project (tag Project:<name>)")
def create_snapshots(project):
	"Create snapshots for EC2 instances"
	instances = filter_instances(project)
	for i in instances:
		print("Stopping {0}...".format(i.id))
		i.stop()
		i.wait_until_stopped()
		for v in i.volumes.all():
			print("Creating snapshot of {0}".format(v.id))
			v.create_snapshot(Description="Created from CLI")
		print("Starting {0}...".format(i.id))
		i.start()
		i.wait_until_running()
	print("Job completed")
	return

@volumes.command('list')
@click.option('--project', default=None, help="Only volumes for project (tag Project:<name>)")
def list_volumes(project):
	"List EC2 volumes"
	instances = filter_instances(project)
	for i in instances:
		for v in i.volumes.all():
			print(', '.join((
				"\n" +
				"Vid: " + v.id + "\n" +
				"Iid: " + i.id + "\n" +
				"size: " + str(v.size) + "GiB",
				"\n")))
	return

@snapshots.command('list')
@click.option('--project', default=None, help="Only snapshots for prohect (tag Project:<name>)")
@click.option('--all', 'list_all', default=False, is_flat=True, help="list all snapshots for each volume on record")
def list_snapshots(project, list_all):
	"List EC2 snapshots"
	instances = filter_instances(project)
	for i in instances:
		for v in i.volumes.all():
			for s in v.snapshots.all():
				print(', '.join((
					"\n" +
					"Sid: " + s.id + "\n" +
					"Vid: " + v.id + "\n" +
					"Iid: " + i.id + "\n" +
					"state: " + s.state + "\n" +
					"created: " + s.start_time.strftime("%c"),
					"\n")))
				if s.state == "completed" and not list_all: break
	return

if __name__ == '__main__':
	cli()
