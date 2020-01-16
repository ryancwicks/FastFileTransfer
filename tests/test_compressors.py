import io

import zstandard as zstd


def test_simple_compress_decompress():
    test_string = "The quick red fox jumped over the lazy brown dog.".encode(
        "utf-8")

    compressor = zstd.ZstdCompressor()
    with open("tests/img_orig.tif", 'rb') as input_stream, open("tests/compressed_img.small", 'wb') as output_stream:
        compressor.copy_stream(input_stream, output_stream)

    decompressor = zstd.ZstdDecompressor()
    with open("tests/compressed_img.small", 'rb') as input_stream, open('tests/output_img.tif', 'wb') as output_stream:
        decompressor.copy_stream(input_stream, output_stream)


def test_simple_compress_decompress():
    test_string = "The quick red fox jumped over the lazy brown dog.".encode(
        "utf-8")

    compressor = zstd.ZstdCompressor()
    with open("tests/img_orig.tif", 'rb') as input_stream, open("tests/compressed_img.small", 'wb') as output_stream:
        compressor.copy_stream(input_stream, output_stream)

    decompressor = zstd.ZstdDecompressor()
    with open("tests/compressed_img.small", 'rb') as input_stream, open('tests/output_img.tif', 'wb') as output_stream:
        decompressor.copy_stream(input_stream, output_stream)
