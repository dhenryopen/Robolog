library(shiny)
library(datasets)
library(jsonlite)
library(ggplot2)
library(scales)
library(RCurl)
library(ckanr)

# Motor 0 ( plus or minus, forward or backwards )
# Current 12 (up to 40A, 3.5A observed)
# number of switches will vary
# Encoder 1 distance
# Limit switch
# 3-axis gyro with accelerometer
# 256MB 
# Jade


library(ckanr)
library(jsonlite)

### Set the CKAN server URL

ckan_url <- 'http://localhost:5000/'

### Initialize the environment

ckanr_setup(url = ckan_url)

### Search for all resources with "4918" in the name

search_results <- resource_search(q = 'name:4918' , as = 'table')

### Get the 2nd resource id -- this is our "golden JSON record" for testing & demonstration

resource_url <-
    search_results$results[c('url')][1,] # resource is a .json file

### Get the extension (should be .csv or .json)

resource_ext <- tools::file_ext(resource_url)

### Retrieve the data and load it into a data frame

if (resource_ext == "json") {
    robolog <- fromJSON(resource_url)
    
} else if (resource_ext == "csv") {    # note: currently have an issue with the sample CSV file structure
    robolog <- read.csv(resource_url)
    
} 

# Concatenate date & time

t <- paste(robolog$Date,robolog$Time)

# convert to datetime and append to data frame

robolog[,'datetime'] <- as.POSIXct(strptime(t, "%m/%d/%Y %H:%M:%OS"))  
robolog[,'pct_bus_utilization'] <- as.numeric(robolog$"% Bus Utilization")
robolog[,'pct_cpu_low'] <- as.numeric(robolog$"CPU % Low")
robolog[,'pct_cpu_time_critical'] <- as.numeric(robolog$"CPU % Time Crit")
robolog[,'ram_free'] <- as.numeric(robolog$"RAM Free")
robolog[,'motor_0'] <- as.numeric(robolog$"Motor 0")
robolog[,'current_12'] <- as.numeric(robolog$"Current 12")
robolog[,'encoder_1_distance'] <- as.numeric(robolog$"Encoder 1 Distance")
robolog[,'limit_1_value'] <- robolog$"Limit 1 Value"
