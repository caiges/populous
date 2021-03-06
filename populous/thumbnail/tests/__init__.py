# For these tests to run successfully, two conditions must be met:
# 1. MEDIA_URL and MEDIA_ROOT must be set in settings
# 2. The user running the tests must have read/write access to MEDIA_ROOT

# Unit tests:
from populous.thumbnail.tests.classes import ThumbnailTest, DjangoThumbnailTest
from populous.thumbnail.tests.templatetags import ThumbnailTagTest
from populous.thumbnail.tests.fields import FieldTest

# Doc tests:
from populous.thumbnail.tests.utils import utils_tests
from populous.thumbnail.tests.templatetags import filesize_tests
__test__ = {
    'utils_tests': utils_tests,
    'filesize_tests': filesize_tests,
}