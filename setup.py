from setuptools import setup
version = '0.2.1'
repo = 'ksamsok-py'

setup(
  name = 'ksamsok',
  packages = ['ksamsok'],
  install_requires=['lxml', 'requests'],
  version = version,
  description = 'API library for the cultural heritage K-Samsök(SOCH) aggregator.',
  author = 'Albin Larsson',
  author_email = 'albin.post@gmail.com',
  url = 'https://github.com/Abbe98/' + repo,
  download_url = 'https://github.com/Abbe98/' + repo + '/tarball/' + version,
  keywords = ['SOCH', 'K-Samsök', 'heritage', 'cultural', 'API'],
  classifiers = [],
)