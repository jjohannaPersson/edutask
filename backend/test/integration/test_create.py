import pytest
import json, os
import pymongo

from src.util.dao import DAO

class TestFileHandler:
    """This test demonstrates the use of yield as an alternative to return, which allows to write code *after* the statement which will be executed once all tests have run. This can be used for cleanup."""

    @pytest.fixture
    def sut(self):
        fabricatedFileName = './src/static/validators/fabricatedFileName.json'
        self.json_string = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["firstName", "lastName"],
                "properties": {
                    "firstName": {
                        "bsonType": "string",
                        "description": "the first name of a user must be determined",
                        "uniqueItems": True,
                    },
                    "lastName": {
                        "bsonType": "string",
                        "description": "the last name of a user must be determined"
                    },
                    "task": {
                        "bsonType": "array",
                        "uniqueItems": True,
                        "items": {
                            "bsonType": "string"
                        }
                    }
                }
            }
        }
        with open(fabricatedFileName, 'w') as outfile:
            json.dump(self.json_string, outfile)

        # yield instead of return the system under test
        dao = DAO(collection_name="fabricatedFileName")
        yield dao

        # clean up the file after all tests have run
        os.remove(fabricatedFileName)

        dao.drop()

    @pytest.mark.demo
    def test_create_valid(self, sut):
        """ test create valid input to db """
        data = {
            "firstName": "John",
            "lastName": "Doe",
            "task": [
                "test",
                "test2"
            ]
        }
        content = sut.create(data)
        assert content['firstName'] == data['firstName']

    def test_create_wrong_bson_type(self, sut):
        """ test create with wrong bson type """
        data = {
            "firstName": 1,
            "lastName": "Doe",
            "task": [
                "test",
                "test2"
            ]
        }
        with pytest.raises(pymongo.errors.WriteError):
            sut.create(data)

    def test_create_missing_property(self, sut):
        """ test create with missing required property """
        data = {
            "firstName": "John",
            "task": [
                "test",
                "test2"
            ]
        }

        with pytest.raises(pymongo.errors.WriteError):
            sut.create(data)

    def test_create_notUnique_document(self, sut):
        """ test create with not unique firstName """
        data = {
            "firstName": "John",
            "lastName": "Doe",
            "task": [
                "test",
                "test1"
            ]
        }
        sut.create(data)

        with pytest.raises(pymongo.errors.WriteError):
            sut.create(data)
