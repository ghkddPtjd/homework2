import unittest

from src.base62 import decode, encode


class Base62Tests(unittest.TestCase):
    def test_encode_uses_the_expected_digit_order(self):
        cases = {
            0: "0",
            9: "9",
            10: "a",
            35: "z",
            36: "A",
            61: "Z",
            62: "10",
            3843: "ZZ",
            3844: "100",
        }

        for value, expected in cases.items():
            with self.subTest(value=value):
                self.assertEqual(encode(value), expected)

    def test_decode_uses_the_expected_digit_order(self):
        cases = {
            "0": 0,
            "9": 9,
            "a": 10,
            "z": 35,
            "A": 36,
            "Z": 61,
            "10": 62,
            "ZZ": 3843,
            "100": 3844,
        }

        for value, expected in cases.items():
            with self.subTest(value=value):
                self.assertEqual(decode(value), expected)

    def test_round_trips_large_integers(self):
        for value in (0, 1, 62, 2**64, 10**100):
            with self.subTest(value=value):
                self.assertEqual(decode(encode(value)), value)

    def test_decode_accepts_leading_zeroes(self):
        self.assertEqual(decode("000a"), 10)

    def test_encode_rejects_non_integer_values(self):
        for value in (1.5, "12", True):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    encode(value)

    def test_encode_rejects_negative_values(self):
        with self.assertRaises(ValueError):
            encode(-1)

    def test_decode_rejects_empty_or_invalid_strings(self):
        for value in ("", "a-b", "é"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    decode(value)

    def test_decode_rejects_non_string_values(self):
        with self.assertRaises(TypeError):
            decode(62)


if __name__ == "__main__":
    unittest.main()
