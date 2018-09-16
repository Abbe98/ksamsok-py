from setuptools import setup
version = '2.0.0'
repo = 'ksamsok-py'

setup(
  name = 'ksamsok',
  packages = ['ksamsok'],
  install_requires=['requests'],
  setup_requires=['pytest-runner'],
  tests_require=['pytest'],
  python_requires='>=3.6.0',
  version = version,
  description = 'API library for the cultural heritage K-Samsök(SOCH) aggregator.',
  author = 'Albin Larsson',
  author_email = 'albin.post@gmail.com',
  url = 'https://github.com/Abbe98/' + repo,
  download_url = 'https://github.com/Abbe98/' + repo + '/tarball/' + version,
  keywords = ['SOCH', 'K-Samsök', 'heritage', 'cultural', 'API'],
  license='MIT',
  classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3 :: Only',
    'Intended Audience :: Developers',
    'Intended Audience :: Education'
  ]
)