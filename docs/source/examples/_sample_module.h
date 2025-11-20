/**
 * @file _sample_module.h
 * @brief Sample C++ module for demonstrating Breathe/Doxygen documentation
 *
 * This header provides a simple database connection class to demonstrate
 * how Breathe integrates Doxygen documentation into Sphinx.
 */

#ifndef SAMPLE_MODULE_H
#define SAMPLE_MODULE_H

#include <string>

/**
 * @brief Manages database connections
 *
 * This class provides methods for connecting to, querying, and disconnecting
 * from a database.
 */
class DatabaseConnection {
public:
    /**
     * @brief Construct a new Database Connection object
     *
     * @param host The database host address
     * @param port The database port number (default: 9042)
     * @param username Optional username for authentication
     */
    DatabaseConnection(const std::string& host, int port = 9042, 
                      const std::string& username = "");

    /**
     * @brief Establish a connection to the database
     *
     * @return true if connection was successful
     * @return false if connection failed
     * @throws ConnectionError if connection fails after retries
     */
    bool connect();

    /**
     * @brief Execute a query on the database
     *
     * @param query The SQL query string to execute
     * @return Query results as a string
     * @throws RuntimeError if not connected to database
     */
    std::string execute(const std::string& query);

    /**
     * @brief Close the database connection
     */
    void disconnect();

private:
    std::string host_;      ///< Database host address
    int port_;              ///< Database port number
    std::string username_;  ///< Optional username
    bool connected_;        ///< Connection status
};

/**
 * @brief Format a SQL query string
 *
 * @param query The SQL query template
 * @param indent Number of spaces for indentation (default: 4)
 * @return Formatted SQL query string
 */
std::string format_query(const std::string& query, int indent = 4);

/**
 * @brief Validate database connection parameters
 *
 * @param host The database host
 * @param port The database port
 * @return true if parameters are valid
 * @return false otherwise
 */
bool validate_connection_params(const std::string& host, int port);

#endif // SAMPLE_MODULE_H

