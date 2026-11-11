import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'my_service_demo'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.py')),
        ('share/' + package_name + '/config', glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='36922732+xtrn143@users.noreply.github.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'add_two_ints_server = my_service_demo.add_two_ints_server:main',
            'add_two_ints_client = my_service_demo.add_two_ints_client:main',
            'fibonacci_action_server = my_service_demo.fibonacci_action_server:main',
            'fibonacci_action_client = my_service_demo.fibonacci_action_client:main',
            'param_demo = my_service_demo.param_demo:main',
        ],
    },
)
