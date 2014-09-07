import re
import uuid

from athumb.backends.s3boto import S3BotoStorage_AllPublic

class S3BotoStorage_ODALC(S3BotoStorage_AllPublic):
    """ Probably the worst hack of this entire project pls forgive me """
    UUID_REGEX = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

    def __init__(self, *args, **kwargs):
        super(S3BotoStorage_ODALC, self).__init__(*args, **kwargs)

    def get_available_name(self, name):
        """ Generate unique name. If get_available_name was called already,
        don't do anything
        """
        name = self._clean_name(name)
        match = re.search(S3BotoStorage_ODALC.UUID_REGEX, name)
        if not match:
            filename = name[name.rindex('/') + 1:]
            path = name[:name.rindex('/') + 1]
            name = path + str(uuid.uuid1()) + '-' + filename
        return name
