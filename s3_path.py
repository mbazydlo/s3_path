from __future__ import annotations

import re


class S3Path:
    S3_SUFFIX = 's3://'

    def __init__(self, full_path=None, *, bucket: str = '', key: str = ''):
        if full_path:
            self.split_path(full_path)
            return
        self.bucket = bucket
        self.key = key

    def __str__(self):
        return f'{self.S3_SUFFIX}{self.bucket}/{self.key}'

    def __repr__(self):
        return f'{self.__class__.__name__}(bucket={self.bucket!r}, key={self.key!r})'

    def __truediv__(self, other: str):
        if not isinstance(other, str):
            raise ValueError(f'Part of path that being added has to be string type, got {type(other)}: {other}')

        new_key = (self.key + '/' + other).strip('/')
        return S3Path(bucket=self.bucket, key=new_key)

    @staticmethod
    def is_s3_path(value):
        return re.search('^s3:\/\/.+\/?.?', value)

    @property
    def parent(self):
        new_key = ''
        if '/' in self.key:
            new_key = self.key.rsplit('/', 1)[0]
        return S3Path(bucket=self.bucket, key=new_key)

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value.strip('/')

    @property
    def bucket(self):
        return self._bucket

    @bucket.setter
    def bucket(self, value):
        self._bucket = value.strip('/')

    @property
    def boto3_params(self):
        return dict(Bucket=self.bucket, Key=self.key)

    def split_path(self, full_path):
        if not self.is_s3_path(full_path):
            raise ValueError(f'{full_path=} is not a correct s3 path')
        self.bucket, self.key, *_ = full_path.strip(self.S3_SUFFIX).split('/', 1) + ['']


    
    