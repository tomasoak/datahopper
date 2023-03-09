import io

import pandas as pd


def stream_object(
    key,
    bucket=BUCKET,
    version_id=None,
    client=S3_CLIENT,
    track=True,
    decode=True,
    encoding="utf8",
    decoding_errors="strict",
    **kwargs,
):
    """
    Returns a stream containing the body of an S3 object. This function is a context
    manager to ensure that the HTTP stream gets closed:

        with stream_object("my-object", "my_bucket") as file:
            print("The contents are", file.read())

    Args:
        decode: if true then the stream will contain text; otherwise it will contain
            bytes.
        decoding_errors: see the "errors" parameter of
            https://docs.python.org/3/library/io.html#io.TextIOWrapper
        track: if true then the S3 object will be added to
            `trase.tools.aws.metadata.S3_OBJECTS_ACCESSED_IN_CURRENT_SESSION`
    """

    if "VersionId" in kwargs:
        raise ValueError("Please use version_id argument")

    if version_id is not None:
        kwargs["VersionId"] = version_id

    obj = client.get_object(Bucket=bucket, Key=key, **kwargs)
    buffer: StreamingBody = obj["Body"]
    if decode:
        buffer = io.TextIOWrapper(buffer, encoding=encoding, errors=decoding_errors)

    if track:
        add_object_to_tracker(key, bucket, version_id, client)

    return closing(buffer)


def read_csv(
    key,
    bucket=BUCKET,
    version_id=None,
    client=S3_CLIENT,
    track=True,
    **kwargs,
):
    """Read an S3 object containing CSV data to a DataFrame

    Args:
        kwargs: passed through to `pd.read_csv`
    """
    with stream_object(key, bucket, version_id, client, track, decode=False) as body:
        return pd.read_csv(body, **kwargs)


def read_xlsx(
    key,
    bucket=BUCKET,
    version_id=None,
    client=S3_CLIENT,
    track=True,
    **kwargs,
):
    """Read an S3 object containing XLSX data to a DataFrame

    Args:
        kwargs: passed through to `pd.read_excel`
    """
    with stream_object(key, bucket, version_id, client, track, decode=False) as body:
        return pd.read_excel(io.BytesIO(body.read()), engine="openpyxl", **kwargs)


def get_pandas_df(
    key,
    bucket=BUCKET,
    version_id=None,
    client=S3_CLIENT,
    track=True,
    sep=";",
    encoding="utf8",
    xlsx=False,
    **kwargs,
):
    """
    Read a CSV or XLSX dataset from S3 to a Pandas DataFrame. See
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html
    """
    if xlsx:
        return read_xlsx(key, bucket, version_id, client, track, **kwargs)
    else:
        return read_csv(
            key, bucket, version_id, client, track, sep=sep, encoding=encoding, **kwargs
        )
