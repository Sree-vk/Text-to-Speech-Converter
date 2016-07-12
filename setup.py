try :

	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'description': 'Text to Speech converter',
    	'author': 'Sree_Vk',
    	'url': 'URL to get it at.',
	'download_url': 'Where to download it.',
    	'author_email': 'vksreelakshmi@yahoo.co.in',
    	'version': '0.1',
    	'install_requires': ['nose'],
    	'packages': [],
    	'scripts': [],
    	'name': 'tts-converter'
}

setup(**config)
