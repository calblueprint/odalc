from storages.backends.s3boto import S3BotoStorage

# Custom storage logic for Amazon S3
StaticFilesS3BotoStorage = lambda: S3BotoStorage(location='static')
UploadsS3BotoStorage = lambda: S3BotoStorage(location='uploads')
