Feature: User Login
  As a registered user
  I want to securely log into my account
  So that I can access my personalized dashboard

  Background:
    Given the user is on the login page
    And a registered account exists with email "jane.doe@example.com" and password "Str0ngP@ss!"

  # ---------------------------------------------------------------------
  Scenario: Valid login with correct credentials
    Given the user enters email "jane.doe@example.com"
    And the user enters password "Str0ngP@ss!"
    When the user clicks the "Log In" button
    Then the user should be redirected to the "/dashboard" page
    And a valid session token should be set in the browser
    And the page should display the welcome message "Welcome back, Jane"

  # ---------------------------------------------------------------------
  Scenario: Invalid login with incorrect password
    Given the user enters email "jane.doe@example.com"
    And the user enters password "WrongPassword123"
    When the user clicks the "Log In" button
    Then the user should remain on the login page
    And an error message "Invalid email or password" should be displayed
    And no session token should be set in the browser

  # ---------------------------------------------------------------------
  Scenario: Forgot password flow sends a reset link
    Given the user clicks the "Forgot Password?" link
    And the user is on the "Forgot Password" page
    When the user enters email "jane.doe@example.com"
    And the user clicks the "Send Reset Link" button
    Then a confirmation message "If an account exists, a reset link has been sent" should be displayed
    And a password reset email should be sent to "jane.doe@example.com"
    And the reset link should expire after 30 minutes

  # ---------------------------------------------------------------------
  Scenario: Session expires after period of inactivity
    Given the user has successfully logged in with email "jane.doe@example.com"
    And the user is on the "/dashboard" page
    When the user remains inactive for 31 minutes
    And the user attempts to navigate to "/account/settings"
    Then the user should be redirected to the login page
    And a message "Your session has expired. Please log in again." should be displayed
    And the expired session token should no longer grant access to protected routes

  # ---------------------------------------------------------------------
  Scenario: Account lockout after repeated failed login attempts
    Given the user enters email "jane.doe@example.com"
    When the user submits an incorrect password 5 times in a row
    Then the account "jane.doe@example.com" should be locked
    And an error message "Account locked due to multiple failed attempts. Try again in 15 minutes." should be displayed
    And a 6th login attempt with the correct password "Str0ngP@ss!" should still be rejected
    And a lockout notification email should be sent to "jane.doe@example.com"