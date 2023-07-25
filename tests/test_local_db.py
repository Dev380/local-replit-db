# flake8: noqa# flake8: noqa
"""
Tests for localreplitdb
Copied from https://github.com/replit/replit-py/blob/cee2529780072fadfd5230a6b5467366376b7cec/tests/test_database.py.
"""

from localreplitdb import LocalDatabase as Database

import requests
import unittest

class TestDatabase(unittest.TestCase):
    """Tests for the sync db."""

    def setUp(self) -> None:
        """Init DB."""
        self.db = Database("/tmp/test_db_real.db")

        # nuke whatever is already here
        for k in self.db.keys():
            del self.db[k]

    def tearDown(self) -> None:
        """Nuke whatever the test added."""
        for k in self.db.keys():
            del self.db[k]

    def test_get_set_delete(self) -> None:
        """Test get, set, and delete."""
        with self.assertRaises(KeyError):
            self.db["key"]

        self.db["key"] = "value"
        val = self.db["key"]
        self.assertEqual(val, "value")

        del self.db["key"]
        with self.assertRaises(KeyError):
            val = self.db["key"]

    def test_list_keys(self) -> None:
        """Test that we can list keys."""
        key = "test-list-keys-with\nnewline"
        self.db[key] = "value"

        val = self.db[key]
        self.assertEqual(val, "value")

        keys = self.db.prefix(key)
        self.assertEqual(keys, (key,))

        keys = self.db.keys()
        self.assertTupleEqual(tuple(keys), (key,))

        # just to make sure...
        self.assertTupleEqual(tuple(self.db.keys()), self.db.prefix(""))

        del self.db[key]
        with self.assertRaises(KeyError):
            val = self.db[key]

    def test_delete_nonexistent_key(self) -> None:
        """Test that deleting a non-existent key returns 404."""
        key = "this-doesn't-exist"
        with self.assertRaises(KeyError):
            self.db[key]

    def test_get_set_fancy_object(self) -> None:
        """Test that we can get/set/delete something that's more than a string."""
        key = "big-ol-list"
        val = ["this", {"is": "a", "complex": "object"}, 1337]

        self.db[key] = val
        act = self.db[key]
        self.assertEqual(act, val)

    def test_nested_setting(self) -> None:
        """Test that nested setting of dictionaries."""
        db = self.db
        key = "big-nested-object"
        val = {"a": {"b": 1}}

        db[key] = val
        db[key]["a"]["b"] = 5
        db[key]["a"]["b"] += 2
        self.assertEqual(db[key], {"a": {"b": 7}})

    def test_nested_lists(self) -> None:
        """Test that nested setting of lists works."""
        db = self.db
        key = "nested-list"

        db[key] = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        db[key][1][1] = 99
        db[key].append(2)
        self.assertEqual(db[key], [[1, 2, 3], [4, 99, 6], [7, 8, 9], 2])

        db[key] = [[1, 2]]
        db[key] *= 2
        self.assertEqual(db[key], [[1, 2], [1, 2]])

        db[key] = [1]
        db[key] += [[2, [3, 4]]]
        db[key][1][1][1] *= 2
        self.assertEqual(db[key], [1, [2, [3, 8]]])

    def test_raw(self) -> None:
        """Test that get_raw and set_raw do not use JSON."""
        k = "raw_test"
        self.db.set(k, "asdf")
        self.assertEqual(self.db.get_raw(k), '"asdf"')

        self.db.set_raw(k, "asdf")
        self.assertEqual(self.db.get_raw(k), "asdf")

        self.db.set(k, {"key": "val"})
        self.assertEqual(self.db.get_raw(k), '{"key":"val"}')

    def test_bulk(self) -> None:
        """Test that bulk setting works."""
        self.db.set_bulk({"bulk1": "val1", "bulk2": "val2"})
        self.assertEqual(self.db["bulk1"], "val1")
        self.assertEqual(self.db["bulk2"], "val2")

    def test_bulk_raw(self) -> None:
        """Test that bulk raw setting works."""
        self.db.set_bulk_raw({"bulk1": "val1", "bulk2": "val2"})
        self.assertEqual(self.db.get_raw("bulk1"), "val1")
        self.assertEqual(self.db.get_raw("bulk2"), "val2")
