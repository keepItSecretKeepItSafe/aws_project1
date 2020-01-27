from setuptools import setup

setup(
	name="AWS CLI Library",
	version="0.1",
	author="Drake",
	author_email="drake.s.deaton",
	description="Instance analyzer & snapshot maker",
	license="GPLv3+",
	packages=["."],
	entry_points="""
		[console_scripts]
		drake=aws.aws:cli
	"""
)

