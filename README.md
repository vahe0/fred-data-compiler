# fred-data-compiler

This script pulls data from the Federal Reserve Economic Data website (FRED) into a CSV file programmatically. 

I created this to quickly extract data I needed for a class project, and I felt that it may also benefit some of my classmates. The FRED website from what I can tell does not have a convenient way of exporting multiple symbols, and during export, it separates different series based on their frequency which makes compiling them into a single dataset time-consuming. There is an addon offered for Excel but I was unable to get it to work on my computer.
 
This script resamples and backfills the series if the specified frequency is not available by default. Details such as start and end dates can be changed in the code but was unnecessary for my use. Any rows that have null values are dropped from the final output, so if you are not seeing a lot of values then one of the symbols may not have very much data. Code can also be added to check for which series is the culprit in that case. Not all symbols have been tested and I highly recommended to check the output to be sure it is accurate.

## Usage

Edit fred_data_compiler.py and enter your API key in the single quotes. An API key can be requested from the FRED site here: https://fred.stlouisfed.org/docs/api/api_key.html

Run the script and input the desired symbols and frequency. A symbol is a short abbreviation like a stock ticker symbol that is found in parentheses next to the title of a dataset on FRED or at the end of the URL of the page. After entering those details, you may get a warning regarding the frequency of the series -this means that the specified symbol(s) were resampled, so please be sure to check the output carefully to make sure there are no undesirable effects. 

A CSV file, "FRED Data.csv",  with all columns will be outputted in the same directory as the script. 
