Feature: User Management REST API
  As an API consumer
  I want to authenticate and manage user resources
  So that I can build reliable integrations against the /api/login and /api/users endpoints

  Background:
    Given the API base URL is configured
    And the request "Content-Type" header is "application/json"

  # ---------------------------------------------------------------------
  # AUTHENTICATION
  # ---------------------------------------------------------------------
  Scenario: Successful login returns a valid auth token
    Given a registered user exists with email "jane.doe@example.com" and password "Str0ngP@ss!"
    When the client sends a POST request to "/api/login" with body:
      """
      {
        "email": "jane.doe@example.com",
        "password": "Str0ngP@ss!"
      }
      """
    Then the response status code should be 200
    And the response body should contain a non-empty "token" field
    And the "token" field should be a valid JWT string

  Scenario: Login request missing required field returns 400
    When the client sends a POST request to "/api/login" with body:
      """
      {
        "email": "jane.doe@example.com"
      }
      """
    Then the response status code should be 400
    And the response body should contain an "error" field
    And the error message should indicate that "password" is required

  Scenario: Malformed login request body returns 400
    When the client sends a POST request to "/api/login" with body:
      """
      { "email": "jane.doe@example.com", "password":
      """
    Then the response status code should be 400
    And the response body should contain an "error" field
    And the error message should indicate the request body is malformed or invalid JSON

  # ---------------------------------------------------------------------
  # CRUD LIFECYCLE — /api/users
  # ---------------------------------------------------------------------
  Scenario: Create a new user
    Given the client has a valid auth token
    When the client sends a POST request to "/api/users" with body:
      """
      {
        "email": "new.user@example.com",
        "first_name": "New",
        "last_name": "User"
      }
      """
    Then the response status code should be 201
    And the response body should contain a non-empty "id" field
    And the response body "email" field should equal "new.user@example.com"
    And the created user id should be stored for subsequent scenarios as "userId"

  Scenario: Retrieve an existing user
    Given the client has a valid auth token
    And a user exists with id "userId"
    When the client sends a GET request to "/api/users/{userId}"
    Then the response status code should be 200
    And the response body "id" field should equal "{userId}"
    And the response body "email" field should equal "new.user@example.com"

  Scenario: Update an existing user
    Given the client has a valid auth token
    And a user exists with id "userId"
    When the client sends a PUT request to "/api/users/{userId}" with body:
      """
      {
        "email": "new.user@example.com",
        "first_name": "Updated",
        "last_name": "User"
      }
      """
    Then the response status code should be 200
    And the response body "first_name" field should equal "Updated"

  Scenario: Delete an existing user
    Given the client has a valid auth token
    And a user exists with id "userId"
    When the client sends a DELETE request to "/api/users/{userId}"
    Then the response status code should be 200 or 204
    And a subsequent GET request to "/api/users/{userId}" should return status code 404

  # ---------------------------------------------------------------------
  # ERROR HANDLING
  # ---------------------------------------------------------------------
  Scenario: Retrieve a non-existent user returns 404
    Given the client has a valid auth token
    When the client sends a GET request to "/api/users/does-not-exist-999"
    Then the response status code should be 404
    And the response body should contain an "error" field
    And the error message should indicate the user was not found

  Scenario: Update a non-existent user returns 404
    Given the client has a valid auth token
    When the client sends a PUT request to "/api/users/does-not-exist-999" with body:
      """
      {
        "email": "ghost@example.com",
        "first_name": "Ghost",
        "last_name": "User"
      }
      """
    Then the response status code should be 404
    And the response body should contain an "error" field

  Scenario: Delete a non-existent user returns 404
    Given the client has a valid auth token
    When the client sends a DELETE request to "/api/users/does-not-exist-999"
    Then the response status code should be 404
    And the response body should contain an "error" field

  # ---------------------------------------------------------------------
  # SCHEMA VALIDATION
  # ---------------------------------------------------------------------
  Scenario: Created user object matches expected schema
    Given the client has a valid auth token
    When the client sends a POST request to "/api/users" with body:
      """
      {
        "email": "schema.check@example.com",
        "first_name": "Schema",
        "last_name": "Check"
      }
      """
    Then the response status code should be 201
    And the response body should include exactly the fields "id", "email", "first_name", "last_name"
    And the "id" field should be of type string or integer
    And the "email" field should be of type string and match a valid email format
    And the "first_name" field should be of type string
    And the "last_name" field should be of type string

  Scenario: Retrieved user object matches expected schema
    Given the client has a valid auth token
    And a user exists with id "userId"
    When the client sends a GET request to "/api/users/{userId}"
    Then the response status code should be 200
    And the response body should include exactly the fields "id", "email", "first_name", "last_name"
    And no field in the response body should be null or missing