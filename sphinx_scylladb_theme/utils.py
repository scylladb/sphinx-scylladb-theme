import requests
import json

def multiversion_regex_builder(versions):
    """Generates a regex string from a list of versions.

    Every documentation project `conf.py` file uses this function
    to define the different documentation versions supported.

    :param versions: A list of versions. Versions could be either branch names or tags.
    :type versions: list of str

    :return: The equivalent regular expression.
    :rtype: str
    """

    if len(versions) == 0:
        return "None"
    elif len(versions) == 1 and versions[0] == "*":
        return r"^.*"
    elif len(versions) == 1:
        return r"^" + versions[0] + r"$"
    else:
        versions = [f"^{version}$" for version in versions]
        return r"\b(" + "|".join(versions) + r")\b"


def fetch_multiversion_configuration(url):
    """Fetches JSON content from the specified URL and parses it into a Python object
    for defining ScyllaDB multiversion data from a remote source.

    :param url: The URL to fetch the JSON data from.
    :type url: str

    :return: A dictionary representing the JSON content.
    :rtype: dict
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching data from {url}: {e}")
        return None
