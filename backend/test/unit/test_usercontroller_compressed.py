# import pytest
# import json
# import unittest.mock as mock
# from src.controllers.usercontroller import UserController

# test_user = json.load(open("./test/unit/test_user.json"))
# test_users = json.load(open("./test/unit/test_users.json"))
# valid_email = "test@test.com"

# # tests for get_user_by_email
# @pytest.fixture
# def sut(json_data: json):
#     mocked_dao = mock.MagicMock()
#     mocked_dao.find.return_value = json_data
#     mockedsut = UserController(dao=mocked_dao)
#     return mockedsut


# @pytest.mark.demo
# @pytest.mark.parametrize('json_data, expected', [(test_user, valid_email), (test_users, valid_email)])
# def test_get_user_by_email(sut, expected):
#     result = sut.get_user_by_email(valid_email)
#     assert result["email"] == expected

# # def test_get_user_by_email_valid_email_existing_user():
# #     """ test get user by email with valid email and existing user """
# #     # Arrange
# #     mocked_dao = mock.MagicMock()
# #     test_user = json.load(open("./test/unit/test_user.json"))
# #     mocked_dao.find.return_value = test_user
# #     sut = UserController(dao=mocked_dao)

# #     # Act
# #     valid_email = "test@test.com"
# #     result = sut.get_user_by_email(valid_email)

# #     # Assert
# #     assert result["email"] == valid_email
