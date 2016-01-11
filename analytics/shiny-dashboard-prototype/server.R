library(shiny)
library(datasets)
library(jsonlite)
library(ggplot2)
library(scales)
library(plotly)

shinyServer(function(input, output) {
    
    output$metricPlot <- renderPlotly({
        
        # setup the plot based on the input variable
        
        if(input$variable == "pct_bus_utilization"){
        plotData <- data.frame(var1 = robolog$datetime, var2 = robolog$pct_bus_utilization, Mode = robolog$Mode)
            ylabel = "Bus Utilization (%)\n"
        } else if(input$variable == "pct_cpu_low"){
            plotData <- data.frame(var1 = robolog$datetime, var2 = robolog$pct_cpu_low, Mode = robolog$Mode)
            ylabel = "CPU Low (%)\n"      
        } else if(input$variable == "pct_cpu_time_critical"){
            plotData <- data.frame(var1 = robolog$datetime, var2 = robolog$pct_cpu_time_critical, Mode = robolog$Mode)
            ylabel = "CPU Time Critical (%)\n"
        } else {
            plotData <- data.frame(var1 = robolog$datetime, var2 = robolog$ram_free, Mode = robolog$Mode)
            ylabel = "Free RAM\n"      
        }
        
        # trim plotData by the input slider parameters
        
        num_obs <- nrow(plotData)  # should correspond to nrecords variable in ui.R
        lower_bound <- input$slider[1]
        upper_bound <- input$slider[2]
        plotData <- plotData[lower_bound:upper_bound,]
        
        # plot the data using plot_ly
        
        p <- plot_ly(plotData, 
                     x = var1, 
                     y = var2, 
                     name = ylabel)
        
        p %>% add_trace(y = fitted(loess(var2 ~ as.numeric(var1))))
    })
    
    # Render the table on the page
    
    output$tableData = renderDataTable({
        lower_bound <- input$slider[1]
        upper_bound <- input$slider[2]
        tableData <- robolog[lower_bound:upper_bound,c("datetime","pct_bus_utilization","pct_cpu_low","pct_cpu_time_critical","ram_free")]
        colnames(tableData) <- c("Date / Time","Bus Utilization (%)","CPU Low (%)", "CPU Time Critical (%)","Free Ram")
        options(digits.secs=3)
        tableData
    })
    
    # Download the table (full data set bounded by slider)
    
    output$downloadData <- downloadHandler(
        filename = function() { 
           paste('robolog', '.csv', sep='') },
        content = function(file) {
            lower_bound <- input$slider[1]
            upper_bound <- input$slider[2]
            tableData <- robolog[lower_bound:upper_bound,c("Date","Time","FMS Present","E-Stop","Team Station","Countdown","Code Start","Brownout","Mode","Code?","Contoller Type","Error Strings","Robot IP","DB Mode","Event Name","Event Type","Event Number","Event Replay","Camera IP","Disk Free","RM Block","RAM Free","CPU % ISR","CPU % Time Crit","CPU % Time Str","CPU % High","CPU % Above","CPU % Normal","CPU % Low","% Bus Utilization","Bus off Cnt","TX_FIFO Full Count","Receive Error Cnt","Transmit Error Cnt","HID Outputs","Rumble Low","Rumble High")
]
            write.csv(tableData, file, row.names = FALSE)
        }
    )
})

