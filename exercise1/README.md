# Exercise 1 - Downloading Files with Python.
*by Beatriz Albiac*

## Things to be implemented:
1. Create the directory ‘downloads’ if it doesn't exist. Download the files one by one. Split out the filename from the url, so the file keeps its original filename.
  
   There's an url that has a typo and doesn't get downloaded: *https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip*<br>
   I took the decision to ignore it, as it can be determined that it should be 2020 or 2022, but the "Q1" is pretty clear. So deciding on either of those options would either make it so a csv is duplicated, or break the continuity of que quarters.<br>
   The optimal way would be to change it to "2020_Q2" but that'd be me making things up.
  
4. Each file is a zip, extract the csv from the zip and delete the zip file.
5.  Look at the data you downloaded:

    a) What kind of data is?
    
    ajkdsklljasdkj
    
    b) Can you think of analyses that can be made with this?
    
    asldkñalsd
    
    c) Is the data normalized or denormalized?
    
    asldklñsa
    
    d) It’s needed any processing before we use it?
    
    aslñdñasl
    
    e) Are there null values? In which fields? Measure how many and guess a reason
    
    sklajfklds

6. Get the mean trip time for each quarter. Track how it evolves over time. For this,
create a new file that reads the downloads directory and computes the mean. This
file can be called ‘processor.py’, and the output should be another folder called
‘processed’
7. Propose and develop any extra analysis you consider. You can use any visualization
tool from python, or any external free tool like Google Data Studio. Focus on the
columns of the file.
8. EXTRA: download the files asynchronously **NOT IMPLEMENTED**
9. Think of the need of delivery the data. How you will do it?

   fdfgdshfdgfdh
