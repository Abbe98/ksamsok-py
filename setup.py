from setuptools import setup
version = '0.8.0'
repo = 'ksamsok-py'

setup(
  name = 'ksamsok',
  packages = ['ksamsok'],
  install_requires=['lxml', 'requests'],
  python_requires='>=3.4.0',
  version = version,
  description = 'API library for the cultural heritage K-samsök(SOCH) aggregator.',
  author = 'Albin Larsson',
  author_email = 'albin.post@gmail.com',
  url = 'https://github.com/Abbe98/' + repo,
  download_url = 'https://github.com/Abbe98/' + repo + '/tarball/' + version,
  keywords = ['SOCH', 'K-samsök', 'heritage', 'cultural', 'API'],
  license='MIT',
  classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3 :: Only',
    'Intended Audience :: Developers',
    'Intended Audience :: Education'
  ]
)