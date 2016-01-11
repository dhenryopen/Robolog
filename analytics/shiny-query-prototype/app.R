
# Simple Shiny application to test package_search() and resource_search()

library(shiny)
library(ckanr)
library(jsonlite)

ckan_url <- 'http://frc-robolog.org:5000/'
ckanr_setup(url = ckan_url)

ui <- fluidPage(
    
     titlePanel("Robolog Data Portal"),
     hr(),
     textInput("queryString", "CKAN Query:", "format:CSV"),  # format:JSON also works
     radioButtons("scope", label = "Scope:",
                  choices = list("Dataset" = 1, "Resource" = 2),
                selected = 1),
     actionButton("execute", "Execute"),
     hr(),
     htmlOutput("query")
)

server <- function(input, output) {

    userQuery <- eventReactive(input$execute, {
        input$queryString
    })
    
    output$query <- renderUI({
        if (input$scope == 1) {
            search_results <- package_search(q = userQuery() , as = 'json')
        } else if (input$scope == 2) {
            search_results <- resource_search(q = userQuery() , as = 'json')
        }
        search_results <- prettify(search_results)
        HTML(paste('<pre>', search_results, '</pre>', sep = '<br/>'))
    })
}

shinyApp(ui, server)
