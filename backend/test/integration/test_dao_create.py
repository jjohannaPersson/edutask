import pytest
import pymongo
import json
import unittest.mock as mock
from src.util.dao import DAO

@pytest.fixture
def sut():
    collection = "test"

    mockedsut = DAO(collection_name=collection)
    yield mockedsut

    mockedsut.drop()

@pytest.mark.demo
def test_create_all_required_prop(sut):
    """ test create valid input to db """
    # Act
    data = {
        "firstName": "Test",
        "lastName": "McTest",
        "email": "test@test.com"
    }
    result = sut.create(data)

    # Assert
    assert result["email"] == data["email"]

def test_create_not_all_required_props(sut):
    """ test create invalid input to db """
    # Act
    data = {
        "firstName": "Test",
        "lastName": "McTest"
    }

    # Assert
    with pytest.raises(pymongo.errors.WriteError):
        sut.create(data)
