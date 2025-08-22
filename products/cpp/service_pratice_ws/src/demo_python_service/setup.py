from setuptools import find_packages, setup

package_name = 'demo_python_service'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + "/resources", ['resource/test.jpg','resource/test1.jpeg']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='bayes',
    maintainer_email='bayes',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'face_detect_service_node=demo_python_service.face_detect_service:main',
            'face_detect_client_node=demo_python_service.face_detect_client:main',
        ],
    },
)
