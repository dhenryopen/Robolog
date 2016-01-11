# ckanr_test.R

# Basic test of the ckanr package with Robolog

# For more information see https://cran.r-project.org/web/packages/ckanr/vignettes/ckanr_vignette.html

library(ckanr)
library(jsonlite)

### Set the CKAN server URL

ckan_url <- 'http://localhost:5000/'

### Initialize the environment

ckanr_setup(url = ckan_url)

### Search for all resources with "4918" in the name

search_results <- resource_search(q = 'name:4918' , as = 'table')
str(search_results)

### Get the resource id for the Nth resource

resource_url <-
#   search_results$results[c('url')][1,] # First resource is a .csv file
    search_results$results[c('url')][2,] # Second resource is a .json file

### Get the extension (should be .csv or .json)

resource_ext <- tools::file_ext(resource_url)

### Retrieve the data for the Nth resource and load it into a data frame

if (resource_ext == "json") {
    robolog_df <- fromJSON(resource_url)
    
} else if (resource_ext == "csv") {
    robolog_df <- read.csv(resource_url)
    
} else {
    print("File type not recognized")
}
str(robolog_df)
