import pytest
import os
import re

from pyincore import IncoreClient, DataService, InsecureIncoreClient


@pytest.fixture
def datasvc():
    cred = None
    try:
        with open(".incorepw", 'r') as f:
            cred = f.read().splitlines()
    except EnvironmentError:
        return None
    # client = IncoreClient("https://incore2-services.ncsa.illinois.edu", cred[0], cred[1])
    client = InsecureIncoreClient("http://incore2-services.ncsa.illinois.edu:8888", cred[0])

    return DataService(client)


def test_get_dataset_metadata(datasvc):
    id = "5a284f0ac7d30d13bc0819c4"
    metadata = datasvc.get_dataset_metadata(id)
    assert metadata['id'] == id


def test_get_dataset_fileDescriptors(datasvc):
    errors = []
    id = "5a284f0ac7d30d13bc0819c4"
    metadata = datasvc.get_dataset_metadata(id)
    fileDescriptor = datasvc.get_dataset_fileDescriptors(id)

    if 'id' not in fileDescriptor[0].keys():
        errors.append("response does not seem right!")

    # compare the id in fileDescriptors field in metadata with the
    # id returned by /file endpoint
    if metadata['fileDescriptors'][0]['id'] != fileDescriptor[0]['id']:
        errors.append("it doesn't fetch the right fileDescriptors for this id!")

    assert not errors, "errors occured:\n{}".format("\n".join(errors))


def test_get_dataset_blob(datasvc):
    errors = []
    id = "5a284f0ac7d30d13bc0819c4"
    fname = datasvc.get_dataset_blob(id,join=True)

    if type(fname) != str:
        errors.append("doesn't return the correct filename!")
    # check if file or folder exists locally, which means successfully downloaded
    if not os.path.exists(fname):
        errors.append("no file or folder has been downloaded!")

    assert not errors, "errors occured:\n{}".format("\n".join(errors))


def test_get_datasets(datasvc):
    errors = []
    datatype = "buildingInventoryVer5.v1.0"
    metadata = datasvc.get_datasets(datatype=datatype, title="Shelby")

    if 'id' not in metadata[0].keys():
        errors.append("response is not right!")
    if not re.search(r'Shelby',metadata[0]['title']):
        errors.append("title doesn't match!")
    if not re.search(datatype, metadata[0]['dataType']):
        errors.append("datatype doesn't match!")

    assert not errors, "errors occured:\n{}".format("\n".join(errors))


def test_get_files(datasvc):
    metadata = datasvc.get_files()
    assert 'id' in metadata[0]


def test_get_file_metadata(datasvc):
    metadata = datasvc.get_file_metadata("5a284f24c7d30d13bc081adb")
    assert metadata['id'] == "5a284f24c7d30d13bc081adb"


def test_get_file_blob(datasvc):
    errors = []
    id = "5a284f24c7d30d13bc081adb"
    fname = datasvc.get_file_blob(id)

    if type(fname) != str:
        errors.append("doesn't return the correct filename!")
    # check if file or folder exists locally, which means successfully downloaded
    if not os.path.exists(fname):
        errors.append("no file has been downloaded!")

    assert not errors, "errors occured:\n{}".format("\n".join(errors))


def test_get_spaces(datasvc):
    metadata = datasvc.get_spaces()

    assert 'datasetIds' in metadata[0].keys()