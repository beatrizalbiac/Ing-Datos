# Exercise 1 - Downloading Files with Python.
*by Beatriz Albiac*

## Things to be implemented:
**1. Create the directory ‘downloads’ if it doesn't exist. Download the files one by one. Split out the filename from the url, so the file keeps its original filename.**
  
   There's an url that has a typo and doesn't get downloaded: *https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip*<br>
   I took the decision to ignore it, as it can be determined that it should be 2020 or 2022, but the "Q1" is pretty clear. So deciding on either of those options would either make it so a csv is duplicated, or break the continuity of que quarters.<br>
   The optimal way would be to change it to "2020_Q2" but that'd be me making things up.
  
**2. Each file is a zip, extract the csv from the zip and delete the zip file.** <br>

**3. Look at the data you downloaded:** <br>
*These are all assumptions based on the data, I do not how the company providing the data operates, or what practices they prefer* 
  1.  What kind of data is?<br>
     They're datasets that track the trips made with bikes lent by a service. The datasets belong to those who provide this service (Divvy) so they can track their bikes, and how they're being used by either subscribers or customers.<br>
     Each trip is identified by a trip id, and each bike has its own bike id. They track the start and end points, and the time the trip takes. Interesntingly, they also track the gender and age (birthyear) of the user. <br>
     However, this seems to have been deprecated from 2020 onwards, as the general format of que csvs changes drasticly, favoring localization aspects over personal data.<br><br>
  2. Can you think of analyses that can be made with this?<br>
     There are many diferent analysis that can be made with this data, it really depends on what is important for the company analyzing the data. Some examples are:<br>
     - The mean of how much time does a trip take usually, as they're most likely charging per the duration of the trip.
     - The most popular stations, as they maybe need to create a subsidiary or just create better connections/icrease the amount of bikes available on those stations
     - The least popular stations, if they don't really get used, they could be dropped from the ones the company offers bikes to.
     - The peak hours/seasons, as they might need to up the number of bikes to meet demand
     - Demographic analysis, as they wouldn't have gender/birthyear otherwise. Maybe which is the gender that uses the bikes more, or the age range
     - The amount of subscribers vs customers that uses the service, just to take marketing decisions on wether they should push more people to subscribe or just make it fully for "casuals"<br><br>
  3. Is the data normalized or denormalized?<br>
     It's denormalized, as things such as the gender, usertype and the station names could be in external tables to avoid duplication. Also just in 2020 the longitude and latitude colums should be summarized in some way, as they should match the longitude y latitude of the start and end stations.<br><br>
  4. It's needed any processing before we use it?<br>
     Yes, the tables need to be standarized as theres some with different column names. There are some columns such as the birthyear or even the dates that need to be in the right format. It should also be considered what to do with nulls.<br><br>
  5. Are there null values? In which fields? Measure how many and guess a reason<br>
     Yes. They're mainly in the birthyear and gender columns. There are several thousand nulls per csv except on the 2020 one, where there's just one row with nulls. This is because of the demographic elements the previous datasets have. I'm guessing that the fields of gender/age were optional when signing up to use the service, resulting in that huge number of nulls.<br>
     I believe that the company realized this in between 2019 ~ 2020, as those fields were dropped in place for some more useful latitude and longitude fields.<br>
     *I took the decision to leave the nulls alone except when visualizing the data, as given the number of them I'd just have to drop the whole birthyear and gender fields. I did drop the one row in 2020 though.*

**4. Get the mean trip time for each quarter. Track how it evolves over time. For this,
create a new file that reads the downloads directory and computes the mean. This
file can be called ‘processor.py’, and the output should be another folder called
‘processed’** <br>

**5. Propose and develop any extra analysis you consider. You can use any visualization
tool from python, or any external free tool like Google Data Studio. Focus on the
columns of the file.** <br> The visualization.py file was created just for this purpose.

**6. EXTRA: download the files asynchronously** *NOT IMPLEMENTED* <br>

**7. Think of the need of delivery the data. How you will do it?**<br>
   To deliver the data, I would include the already cleaned and standardized csvs inside the processed folder, so every quarter follows the same structure and can be compared directly. I would also add a small summary file with the mean trip duration per quarter so the results can be checked quickly without having to run the whole pipeline again. I could also include the graphs pngs, but I decided against it in this case as it wasn't necessary for what I wanted to do. If this were an actual analysis, I'd save them to use it in a presentation or report about the data, it's tendencies outliers etc.
