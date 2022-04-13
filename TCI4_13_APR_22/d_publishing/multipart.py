# Adapted from
# https://stackoverflow.com/questions/26299889/how-to-post-multipart-list-of-json-xml-files-using-python-requests

from urllib3.filepost import encode_multipart_formdata
from urllib3.fields import RequestField


def make_multipart_req(source):
    multipart_parts = []

    for name, (filename, contents, content_type) in source.items():
        part = RequestField(name=name, data=contents, filename=filename)
        part.make_multipart(content_type=content_type)

        multipart_parts.append(part)

    payload, content_type = encode_multipart_formdata(multipart_parts)

    content_type = ''.join(('multipart/mixed',) +
                           content_type.partition(';')[1:])

    return payload, content_type
