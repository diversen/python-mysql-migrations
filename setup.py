from setuptools import setup

setup(
    name='mysql_migrations',
    version='0.0.1',    
    description='Simple way to migrate MySQL',
    url='https://github.com/diversen/mysql-migration',
    author='Dennis Iversen',
    author_email='dennis.iversen@gmail.com',
    license='MIT',
    packages=['mysql_migrations'],
    install_requires=['mysql-connector-python>=8.0.31'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.10',
    ],
)
