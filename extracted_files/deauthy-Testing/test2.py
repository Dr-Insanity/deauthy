import requests, zipfile, io
import requests
import io
import zipfile
def download_extract_zip(url):
    """
    Download a ZIP file and extract its contents in memory
    yields (filename, file-like object) pairs
    """
    response = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
        thezip.extractall('extracted_files')

download_extract_zip("https://github.com/Dr-Insanity/deauthy/archive/refs/heads/Testing.zip")