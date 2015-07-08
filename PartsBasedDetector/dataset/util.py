def download(url, path):
    from urllib import request
    response = request.urlopen(url)
    content = response.read()
    open(path, 'wb').write(content)


def untar(data_filepath, directory_extract_to):
    import tarfile
    tar = tarfile.open(data_filepath, 'r')
    tar.extractall(path=directory_extract_to)
    tar.close()


def unzip(data_filepath, directory_extract_to):
    from zipfile import ZipFile
    zip_ = ZipFile(data_filepath, 'r')
    zip_.extractall(path=directory_extract_to)
    zip_.close()
