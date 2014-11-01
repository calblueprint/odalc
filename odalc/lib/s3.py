from storages.backends.s3boto import S3BotoStorage

StaticFilesS3BotoStorage = lambda: S3BotoStorage(location='static')
UploadsS3BotoStorage = lambda: S3BotoStorage(location='uploads')
