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
                        "description": "the first name of a user must be determined"
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
        yield DAO(collection_name="fabricatedFileName")

        # clean up the file after all tests have run
        os.remove(fabricatedFileName)

        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client.edutask
        collection = db["fabricatedFileName"]
        collection.drop()

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

    def test_create_valid2(self, sut):
        """ test create valid input to db, only required properties """
        data = {
            "firstName": "John",
            "lastName": "Doe",
        }
        content = sut.create(data)
        assert content['firstName'] == data['firstName']

    def test_create_notUnique_in_task(self, sut):
        """ test create with not uniqueItems in task """
        data = {
            "firstName": "John",
            "lastName": "Doe",
            "task": [
                "test",
                "test"
            ]
        }

        with pytest.raises(pymongo.errors.WriteError):
            sut.create(data)

    def test_create_notUnique_document(self, sut):
        """ test create with not uniqueItems document"""
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

    def test_create_wrong_bson_type_only_req(self, sut):
        """ test create with wrong bson type, only required properties """
        data = {
            "firstName": 1,
            "lastName": "Doe",
        }
        with pytest.raises(pymongo.errors.WriteError):
            sut.create(data)

    def test_create_wrong_bson_type_all_properties(self, sut):
        """ test create with wrong bson type, all properties """
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

    def test_create_wrong_bson_type_all_properties(self, sut):
        """ test create with wrong bson type, all properties, not unique """
        data = {
            "firstName": 1,
            "lastName": "Doe",
            "task": [
                "test",
                "test"
            ]
        }
        with pytest.raises(pymongo.errors.WriteError):
            sut.create(data)

    def test_create_missing_property_only_req(self, sut):
        """ test create with missing required property, without task """
        data = {
            "firstName": "John",
        }

        with pytest.raises(pymongo.errors.WriteError):
            sut.create(data)

    def test_create_missing_property_all_properties(self, sut):
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

    def test_create_missing_property_all_properties_not_unique(self, sut):
        """ test create with missing required property, not unique """
        data = {
            "firstName": "John",
            "task": [
                "test",
                "test"
            ]
        }

        with pytest.raises(pymongo.errors.WriteError):
            sut.create(data)

    def test_create_wrong_bson_type_and_missing_property_only_req(self, sut):
        """ test create with wrong bson type """
        data = {
            "firstName": 1,
        }
        with pytest.raises(pymongo.errors.WriteError):
            sut.create(data)

    def test_create_wrong_bson_type_and_missing_property(self, sut):
        """ test create with wrong bson type and missing property """
        data = {
            "firstName": 1,
            "task": [
                "test",
                "test2"
            ]
        }
        with pytest.raises(pymongo.errors.WriteError):
            sut.create(data)

    def test_create_wrong_bson_type_and_missing_property_not_unique(self, sut):
        """ test create with wrong bson type, missing property and not unique """
        data = {
            "firstName": 1,
            "task": [
                "test",
                "test"
            ]
        }
        with pytest.raises(pymongo.errors.WriteError):
            sut.create(data)

    # def test_create_raise_exception(self, sut):
    #     """ test create raise exception """
    #     data = {
    #         "firstName": "Jane",
    #         "lastName": "Doe",
    #         "task": [
    #             "test",
    #             "test1"
    #         ]
    #     }
    #
    #     sut.find.side_effect = Exception
    #
    #     with pytest.raises(Exception):
    #         sut.create(data)
