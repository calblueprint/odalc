import base64, hmac, json, re, time, urllib, uuid
from hashlib import sha1

from django.conf import settings
from django.views.generic import View
from django.http import HttpResponse

class SignS3View(View):
    """ Logic for signing an s3 upload request for non-image files. This View
    isn't rendered - it's only used in AJAX calls. """
    def get(self, request, *args, **kwargs):
        # Load necessary information into the application:
        AWS_ACCESS_KEY = settings.AWS_ACCESS_KEY_ID.strip()
        AWS_SECRET_KEY = settings.AWS_SECRET_ACCESS_KEY.strip().encode('UTF-8')
        S3_BUCKET = settings.S3_BUCKET.strip()

        # Collect information on the file from the GET parameters of the request:
        object_name = 'materials/' + urllib.quote(request.GET.get('s3_object_name'))
        mime_type = request.GET.get('s3_object_type')

        # Set the expiry time of the signature (in seconds) and declare the permissions of the file to be uploaded
        expires = int(time.time()+10)
        amz_headers = "x-amz-acl:public-read"

        # Generate the PUT request that JavaScript will use:
        put_request = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires, amz_headers, S3_BUCKET, object_name)

        # Generate the signature with which the request can be signed:
        signature = base64.encodestring(hmac.new(AWS_SECRET_KEY, put_request, sha1).digest())
        # Remove surrounding whitespace and quote special characters:
        signature = urllib.quote(signature.strip())
        # Build the URL of the file in anticipation of its imminent upload:

        url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, object_name)
        """
        get_params = urllib.urlencode({
            'AWSAccessKeyId': AWS_ACCESS_KEY,
            'Expires': expires,
            'Signature': signature
        })

        content = json.dumps({
            'signed_request': '%s?%s' % (url, get_params),
            'url': url
        })
        """

        content = json.dumps({
            'signed_request': '%s?AWSAccessKeyId=%s&Expires=%d&Signature=%s' % (url, AWS_ACCESS_KEY, expires, signature),
            'url': url
        })

        # Return the signed request and the anticipated URL back to the browser in JSON format:
        return HttpResponse(content, content_type='text/plain; charset=x-user-defined')
