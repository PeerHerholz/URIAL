__version__ = '0.0.1'

NAME = 'URIAL'
MAINTAINER = 'Peer Herholz'
EMAIL = 'herholz.peer@gmail.com'
VERSION = __version__
LICENSE = 'BSD'
DESCRIPTION = ('Utilities for Representational Similarity Analysis in Python')
LONG_DESCRIPTION = ('')
URL = 'http://github.com/peerherholz/{name}'.format(name=NAME)
DOWNLOAD_URL = ('https://github.com/peerherholz/{name}/archive/{ver}.tar.gz'
                .format(name=NAME, ver=__version__))

INSTALL_REQUIRES = [
    'pandas',
    'numpy',
    'seaborn',
    'nilearn',
    'matplotlib',
    'scipy',
    'scikit_learn'

]


PACKAGE_DATA = {
    'URIAL': [
        'plotting/*', 'rdm/*', 'utils/*'
    ]
}
