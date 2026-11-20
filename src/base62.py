_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encode(n: int) -> str:
    """Encode a non-negative integer as a base62 string."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return "0"

    digits = []
    while n:
        n, remainder = divmod(n, len(_ALPHABET))
        digits.append(_ALPHABET[remainder])
    return "".join(reversed(digits))


def decode(s: str) -> int:
    """Decode a base62 string into a non-negative integer."""
    if not isinstance(s, str):
        raise TypeError("s must be a string")
    if not s:
        raise ValueError("s must not be empty")

    value = 0
    for character in s:
        digit = _ALPHABET.find(character)
        if digit == -1:
            raise ValueError(f"invalid base62 character: {character!r}")
        value = value * len(_ALPHABET) + digit
    return value
