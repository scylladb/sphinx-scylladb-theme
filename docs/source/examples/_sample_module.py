"""
Sample module for demonstrating autodoc functionality.

This module provides a simple database connection class and utility functions
for demonstrating how API documentation is generated with sphinx.ext.autodoc.
"""


class DatabaseConnection:
    """
    Manages connections to a database.

    This class provides methods for connecting to, querying, and disconnecting
    from a database. It's designed to demonstrate autodoc's ability to generate
    documentation from Python docstrings.

    :param host: The database host address
    :type host: str
    :param port: The port number (default: 9042)
    :type port: int
    :param username: Optional username for authentication
    :type username: str or None
    """

    def __init__(self, host, port=9042, username=None):
        """Initialize a new database connection."""
        self.host = host
        self.port = port
        self.username = username
        self._connected = False

    def connect(self):
        """
        Establish a connection to the database.

        :returns: True if connection was successful
        :rtype: bool
        :raises ConnectionError: If connection fails
        """
        self._connected = True
        return True

    def execute(self, query):
        """
        Execute a query on the database.

        :param query: The query string to execute
        :type query: str
        :returns: Query results
        :rtype: list
        :raises RuntimeError: If not connected to database
        """
        if not self._connected:
            raise RuntimeError("Not connected to database")
        return []

    def disconnect(self):
        """Close the database connection."""
        self._connected = False


def format_query(query, indent=4):
    """
    Format a database query for better readability.

    This function takes a query string and formats it with proper indentation
    and line breaks for improved readability in logs or documentation.

    :param query: The query string to format
    :type query: str
    :param indent: Number of spaces for indentation (default: 4)
    :type indent: int
    :returns: The formatted query string
    :rtype: str

    Example:

    >>> format_query("SELECT * FROM users")
    'SELECT * FROM users'
    """
    return query.strip()


def validate_connection_params(host, port):
    """
    Validate database connection parameters.

    :param host: The database host address
    :type host: str
    :param port: The port number
    :type port: int
    :returns: True if parameters are valid, False otherwise
    :rtype: bool
    """
    if not host or not isinstance(host, str):
        return False
    if not isinstance(port, int) or port < 1 or port > 65535:
        return False
    return True


# Module-level constants
DEFAULT_TIMEOUT = 30
"""Default connection timeout in seconds"""

MAX_RETRIES = 3
"""Maximum number of connection retry attempts"""

