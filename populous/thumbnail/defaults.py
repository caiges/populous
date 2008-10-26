DEBUG = False
BASEDIR = ''
SUBDIR = ''
PREFIX = ''
QUALITY = 85
CONVERT = '/usr/bin/convert'
WVPS = '/usr/bin/wvPS'
PROCESSORS = (
    'populous.thumbnail.processors.colorspace',
    'populous.thumbnail.processors.autocrop',
    'populous.thumbnail.processors.scale_and_crop',
    'populous.thumbnail.processors.filters',
)
