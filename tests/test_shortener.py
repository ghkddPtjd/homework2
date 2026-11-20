import unittest

from src.shortener import Shortener


class ShortenerTests(unittest.TestCase):
    def setUp(self):
        self.shortener = Shortener()

    def test_shortens_and_expands_a_valid_url(self):
        url = "https://example.com/articles/42?view=full"

        code = self.shortener.shorten(url)

        self.assertEqual(self.shortener.expand(code), url)

    def test_same_url_always_returns_its_existing_code(self):
        url = "https://example.com/same"

        first_code = self.shortener.shorten(url)
        repeated_code = self.shortener.shorten(url)
        next_code = self.shortener.shorten("https://example.com/another")

        self.assertEqual(first_code, repeated_code)
        self.assertEqual(first_code, "0")
        self.assertEqual(next_code, "1")

    def test_codes_are_sequential_base62_identifiers_not_url_hashes(self):
        first = self.shortener.shorten("https://alpha.example/")
        second = self.shortener.shorten("https://beta.example/")
        third = self.shortener.shorten("https://gamma.example/")

        self.assertEqual((first, second, third), ("0", "1", "2"))

    def test_missing_code_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.shortener.expand("not-issued")

    def test_invalid_urls_raise_value_error(self):
        invalid_urls = (
            "",
            "example.com/path",
            "ftp://example.com/file",
            "http:///missing-host",
            " https://example.com/",
            "https://example.com/a b",
        )

        for url in invalid_urls:
            with self.subTest(url=url):
                with self.assertRaises(ValueError):
                    self.shortener.shorten(url)


if __name__ == "__main__":
    unittest.main()
