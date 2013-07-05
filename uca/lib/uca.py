#!/usr/bin/env python
# coding: utf-8

import hashlib
import urlparse
import re


class UrlValidate:
    SUCCESS = 0
    EMPTY_URL = 1
    EMPTY_PROTO = 2
    INVALID_PROTO = 3
    URL_TOO_SHORT = 4
    INVALID_URL = 5
    UNKNOWN_ERROR = -1


def get_hash_value(link):
    """
    Args:
        link: the string of http link
    Returns:
        the hash value(6 bytes) of the link
    """
    hashSlice = hashlib.md5(link).hexdigest()[0:8]
    try:
        bits = get_bit_string(hashSlice)
    except ValueError:
        raise
    charList = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
        'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
        's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
        'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
        'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    ]
    c = []
    for i in range(6):
        # Convert 5 bytes(0 or 1) in bits array to a decimal number
        # Use the decimal number as index to get the desire char from charList
        # The last 2 bytes in the bits array will be ignored
        c.append(charList[int(bits[(5 * i):(5 * (i + 1))], 2)])
    hashLink = ''
    for i in range(6):
        hashLink += (str(c[i]))
    return hashLink


def get_bit_string(hashSlice):
    """
    Args:
        hashSlice: the string contains 1~9 and 'a'~'f', the length should be 8
    Returns:
        Bit string of hashSlice, length should be 32(8 * 4)
    """
    num = 0
    ord_0 = ord('0')
    ord_9 = ord('9')
    ord_a = ord('a')
    ord_f = ord('f')
    for value in hashSlice:
        v = ord(value)
        if (v >= ord_0 and v <= ord_9) or (v >= ord_a and v <= ord_f):
            pass
        else:
            raise ValueError('Invalid string: %s' % (hashSlice))
    for i in range(len(hashSlice)):
        # ex: ab000000 -> 10 + (11 * 16) = 186
        num = num + (int(hashSlice[i], 16) << (4 * i))
    bits = bin(num)[2:]  # Get binary string and cut '0x'
    bits = '00000000000000000000000000000000'[len(bits):] + bits
    return bits


def validate_url(url):
    if url is None or url == '':
        return False, UrlValidate.EMPTY_URL
    url_result = urlparse.urlparse(url)
    if not url_result.scheme:
        return False, UrlValidate.EMPTY_PROTO
    if url_result.scheme != 'http' and url_result.scheme != 'https':
        return False, UrlValidate.INVALID_PROTO
    if len(url_result.netloc) < 5:
        return False, UrlValidate.URL_TOO_SHORT

    legal_url = '%s://%s%s' % (url_result.scheme, url_result.netloc, url_result.path)
    if url_result.query != '':
        legal_url = '%s?%s' % (legal_url, url_result.query)
    if legal_url != url:
        return False, UrlValidate.INVALID_URL
    url = legal_url

    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if regex.search(url) is None:
        return False, UrlValidate.INVALID_URL
    return True, UrlValidate.SUCCESS
