from setuptools import find_packages, setup

package_name = 'pixpubsub'

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
    maintainer_email='root@todo.todo',
    description='Depth publisher/subscriber using rclpy',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "pixhawk_worker = pixpubsub.pix_pubsub_node:main",
            "testing_node = pixpubsub.testing_node:main",
            "Depth_node = pixpubsub.pressure_sensor_subscriber:main",

        ],
    },
)
