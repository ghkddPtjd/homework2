import unittest

from src.hash_table import HashTable


def horner_bucket(key, capacity):
    value = 0
    for character in key:
        value = (value * 31 + ord(character)) % capacity
    return value


def colliding_keys(capacity, count):
    buckets = [[] for _ in range(capacity)]
    for number in range(1000):
        key = f"key-{number}"
        bucket = horner_bucket(key, capacity)
        buckets[bucket].append(key)
        if len(buckets[bucket]) == count:
            return buckets[bucket]
    raise AssertionError(f"could not find {count} colliding keys")


class HashTableTests(unittest.TestCase):
    def test_empty_table_has_initial_capacity_and_missing_keys_raise(self):
        table = HashTable()

        self.assertEqual(table.capacity, 8)
        self.assertEqual(len(table), 0)
        with self.assertRaises(KeyError):
            table.get("missing")
        with self.assertRaises(KeyError):
            table.delete("missing")

    def test_insert_get_overwrite_and_delete(self):
        table = HashTable()

        table.insert("alpha", "first")
        self.assertEqual(table.get("alpha"), "first")
        self.assertEqual(len(table), 1)

        table.insert("alpha", "updated")
        self.assertEqual(table.get("alpha"), "updated")
        self.assertEqual(len(table), 1)

        table.delete("alpha")
        self.assertEqual(len(table), 0)
        with self.assertRaises(KeyError):
            table.get("alpha")

    def test_horner_hash_and_bucket_indices(self):
        table = HashTable()

        self.assertEqual(table.bucket_index(""), 0)
        self.assertEqual(table.bucket_index("abc"), horner_bucket("abc", table.capacity))
        for key in ("", "a", "abc", "longer-key"):
            with self.subTest(key=key):
                self.assertGreaterEqual(table.bucket_index(key), 0)
                self.assertLess(table.bucket_index(key), table.capacity)

    def test_collisions_can_be_found_and_entries_deleted_from_each_chain_position(self):
        table = HashTable()
        keys = colliding_keys(table.capacity, 3)
        self.assertEqual(
            [table.bucket_index(key) for key in keys],
            [table.bucket_index(keys[0])] * 3,
        )

        for key in keys:
            table.insert(key, f"value-{key}")
        for key in keys:
            with self.subTest(key=key):
                self.assertEqual(table.get(key), f"value-{key}")

        # This order exercises both ends and the middle, independent of chain direction.
        for key in (keys[0], keys[1], keys[2]):
            table.delete(key)
            for remaining in keys:
                if remaining != key:
                    self.assertEqual(table.get(remaining), f"value-{remaining}")
            with self.assertRaises(KeyError):
                table.get(key)

        self.assertEqual(len(table), 0)

    def test_table_resizes_only_after_load_factor_exceeds_three_quarters(self):
        table = HashTable()

        for number in range(6):
            table.insert(f"key-{number}", number)
        self.assertEqual(table.capacity, 8)

        table.insert("key-6", 6)
        self.assertEqual(table.capacity, 16)
        self.assertEqual(len(table), 7)
        for number in range(7):
            self.assertEqual(table.get(f"key-{number}"), number)

    def test_collisions_survive_resize(self):
        table = HashTable()
        keys = colliding_keys(table.capacity, 3)
        for key in keys:
            table.insert(key, key.upper())

        for number in range(5):
            table.insert(f"extra-{number}", number)

        self.assertEqual(table.capacity, 16)
        for key in keys:
            self.assertEqual(table.get(key), key.upper())


if __name__ == "__main__":
    unittest.main()
