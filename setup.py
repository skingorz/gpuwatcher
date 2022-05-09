from setuptools import setup, find_packages

VERSION = '0.0.10'

setup(name='gpuwatcher',
      version=VERSION,
      description="Monitor the memory usage and notify",
      long_description='Monitor the memory usage and notify',
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords=('gpu', 'watcher','notify', 'webhook', 'feishu'),
      author='Kun song',
      author_email='songkun666@outlook.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=["psutil", "nvidia-ml-py3"],
      entry_points={
          'console_scripts': [
              'gpuwatcher = gpuwatcher.gpuwatcher:main'
          ]}
      )