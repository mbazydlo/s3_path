from pytest import fixture, mark, param
from s3_path import S3Path

params_for_test_init_S3Path = [
    ('bucket', ''),
    ('bucket', 'foo'),
    ('bucket', 'foo/bar'),
]


@mark.parametrize('bucket, path', params_for_test_init_S3Path, ids=['empty key', 'foo key', 'foo/bar key'])
def test_init_S3Path_using_bucket_and_path(bucket, path):
    obj = S3Path(Bucket=bucket, Key=path)
    assert type(obj) == S3Path
    assert vars(obj) == dict(_bucket=bucket, _key=path)


params_for_test_init_S3Path = [
    ('s3://bucket', 'bucket', ''),
    ('s3://bucket/', 'bucket', ''),
    ('s3://bucket/foo', 'bucket', 'foo'),
    ('s3://bucket/foo/bar', 'bucket', 'foo/bar'),
]

@mark.parametrize('path, bucket, key', params_for_test_init_S3Path)
def test_init_S3Path_using_path(path, bucket, key):
    obj = S3Path(path)
    assert type(obj) == S3Path