library(shiny)
library(plotly)

nrecords = nrow(robolog)  # upper bound for slider input control

shinyUI(pageWithSidebar(
    
    # Application title
    
    headerPanel("Robolog Metrics"),
    
    # Sidebar with controls to select the variable to plot against time
    
    sidebarPanel(
        selectInput("variable", "Metric:",
                    list("Bus Utilization (%)" = "pct_bus_utilization", 
                         "CPU Low (%)" = "pct_cpu_low", 
                         "CPU Time Critical (%)" = "pct_cpu_time_critical", 
                         "Free RAM" = "ram_free")),
        
        sliderInput("slider", label = "Record Range:", min = 1, 
                    max = nrecords, value = c(1,nrecords)),
        
        downloadButton('downloadData', 'Download')
    ),
    
    # Show the caption and plot of the requested variable against time
    
    mainPanel(
        h3(textOutput("caption")),
        plotlyOutput("metricPlot"),
        tabPanel('metricTable',
                 dataTableOutput("tableData"))
    )
))
