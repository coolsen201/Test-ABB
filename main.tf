# main.tf
provider "azurerm" {
  features = {}
}
resource "azurerm_resource_group" "main" {
  name     = "VSDB01-resource-group"
  location = "East US"
}
resource "azurerm_postgresql_server" "VSDB01" {
  name                = "VSDB01"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku_name            = "B_Gen5_1"
  storage_profile     = "Standard_LRS"
  administrator_login          = "user1"
  administrator_login_password = "YYYYYYY"
}
resource "azurerm_app_service" "VSappweb" {
  name                = "VSappweb-web-app"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  app_service_plan_id = azurerm_app_service_plan.example.id
  site_config {
    python_version = "3.12"
  }
}
resource "azurerm_app_service_plan" "VSapp" {
  name                = "VSapp-app-service-plan"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku {
    tier = "Basic"
    size = "B1"
  }
}
output "postgres_connection_string" {
  value = azurerm_postgresql_server.VSDB01
}
