from setuptools import find_packages, setup

package_name = 'fira_car_control'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/car_bringup.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Anton Petnitsky',
    maintainer_email='anton.petnitsky@gmail.com',
    description=(
        'Onboard autonomous control stack for the FIRA Autonomous Cars '
        'Physical Division entry built on the NITROUS RC car chassis.'
    ),
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'lane_detection_node = fira_car_control.lane_detection_node:main',
            'steering_control_node = fira_car_control.steering_control_node:main',
            'speed_control_node = fira_car_control.speed_control_node:main',
        ],
    },
)
