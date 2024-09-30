from setuptools import setup, find_packages

setup(
    name='log_analyzer',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'openai',
        'python-dotenv',
        'APScheduler'
    ],
    entry_points={
        'console_scripts': [
            'log-analyzer = main:start_scheduler',
        ],
    }
)
