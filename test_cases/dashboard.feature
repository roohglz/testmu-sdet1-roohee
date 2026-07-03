Feature: Product Listing Dashboard
  As a user of the product-listing dashboard
  I want to view, sort, and interact with product data reliably
  So that I can make informed decisions based on accurate, role-appropriate information

  Background:
    Given the user is logged into the product-listing dashboard

  # ---------------------------------------------------------------------
  Scenario: Product widgets load successfully on dashboard
    Given the product catalog contains 25 active products
    When the user navigates to the "/dashboard/products" page
    Then a loading skeleton should display within 200ms of navigation
    And exactly 25 product widgets should be rendered within 3 seconds
    And each widget should display a product image, name, and price without placeholder text

  # ---------------------------------------------------------------------
  Scenario: Displayed product name and price match backend data
    Given a product exists in the catalog with:
      | field | value          |
      | id    | SKU-1042       |
      | name  | Canon EOS R50  |
      | price | 799.00         |
    When the user views the product widget for "SKU-1042" on the dashboard
    Then the widget should display the name "Canon EOS R50" exactly as stored
    And the widget should display the price as "$799.00"
    And the displayed price should match the value returned by GET "/api/products/SKU-1042"

  # ---------------------------------------------------------------------
  Scenario: Sort products by name ascending
    Given the dashboard displays products named "Zoom Lens", "Aperture Grip", "Mono Tripod"
    When the user selects "Name" from the sort dropdown
    And the user selects "Ascending" sort order
    Then the products should be listed in the order "Aperture Grip", "Mono Tripod", "Zoom Lens"

  # ---------------------------------------------------------------------
  Scenario: Sort products by name descending
    Given the dashboard displays products named "Zoom Lens", "Aperture Grip", "Mono Tripod"
    When the user selects "Name" from the sort dropdown
    And the user selects "Descending" sort order
    Then the products should be listed in the order "Zoom Lens", "Mono Tripod", "Aperture Grip"

  # ---------------------------------------------------------------------
  Scenario: Sort products by price ascending
    Given the dashboard displays products priced at "$450.00", "$120.00", "$899.00"
    When the user selects "Price" from the sort dropdown
    And the user selects "Ascending" sort order
    Then the products should be listed in the order "$120.00", "$450.00", "$899.00"

  # ---------------------------------------------------------------------
  Scenario: Sort products by price descending
    Given the dashboard displays products priced at "$450.00", "$120.00", "$899.00"
    When the user selects "Price" from the sort dropdown
    And the user selects "Descending" sort order
    Then the products should be listed in the order "$899.00", "$450.00", "$120.00"

  # ---------------------------------------------------------------------
  Scenario: Dashboard layout adapts to mobile viewport
    Given the browser viewport is resized to 375x667 (iPhone SE)
    When the user navigates to the "/dashboard/products" page
    Then the product grid should render as a single-column list
    And the sidebar navigation should collapse into a hamburger menu icon
    And no element should overflow the viewport width, requiring horizontal scroll
    And each product widget's tap target should be at least 44x44 pixels

  # ---------------------------------------------------------------------
  Scenario: Standard user has restricted visibility on product dashboard
    Given a user is logged in with role "Standard User"
    When the user navigates to the "/dashboard/products" page
    Then the "Cost Price" column should not be visible on any product widget
    And the "Edit Product" and "Delete Product" buttons should not be rendered
    And a direct request to GET "/api/products/SKU-1042/cost" should return HTTP 403

  # ---------------------------------------------------------------------
  Scenario: Admin user has full visibility on product dashboard
    Given a user is logged in with role "Admin"
    When the user navigates to the "/dashboard/products" page
    Then the "Cost Price" column should be visible on every product widget
    And the "Edit Product" and "Delete Product" buttons should be rendered on every widget
    And a direct request to GET "/api/products/SKU-1042/cost" should return HTTP 200 with the cost value