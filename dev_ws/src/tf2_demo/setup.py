from setuptools import find_packages, setup

package_name = 'tf2_demo'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='25255411@qq.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'static_tf_broadcaster = tf2_demo.static_tf_broadcaster:main',
            'tf_listener = tf2_demo.tf_listener:main',
            'tf_lookup_demo = tf2_demo.tf_lookup_demo:main',
            'dynamic_tf_broadcaster = tf2_demo.dynamic_tf_broadcaster:main',
            'laser_to_odom = tf2_demo.laser_to_odom:main',
        ],
    },
)
