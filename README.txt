ECM1400 Continuous Assessment 

IMPORTANT NOTE:

When you run the Flask section it will print the link to the logging.log file so you will have to copy and paste it into a web browser to access it. It might take a short while to load and won't load it up if you are currently viewing the logging.log file. You need to be viewing something else for it to show. Then you are able to copy and paste the link into a browser.

Github link: https://github.com/RaftRunner/Personalised-COVID-Dashboard/tree/main




Covid data updates:

Task 1 - Read data from a file:

For this task I created a function that takes the CSV file and opens it, then reads it and splits each line up then closes and returns it. Then I test it works through the test underneath the first function. It will work if it prints nothing. If the data doesn't match up then it will output an error, telling you it doesn't work properly. There are 639 lines of data so if it is all read correctly then it works. Just run to test it works.

Task 2 - Data processing:

For this task I imported the function from task 1 for the function I created in task 2, this allows the function in task 2 to access necessary data. The function in task 2 takes data from the past 7 days with all the necessary information to equal the data for the test. I take data for the last 7 days cases and for this I add up the past 7 days with values and then take the overall number. I also take the current hospital cases. And lastly, I take the total deaths by using loops, I get the program to search until it reaches the data required and then after this it stops. Then once all the data is found I return it all and am able to print and compare the data I acquired with the tests. If the data matches then it is all correct. 

Task 3 - Live data access:

For this task I first created the function with it's arguments and default values. I then accessed the current COVID-19 data by using data from the UK Covid-19 module I implemented into the program and imported it in. After the module had been installed it meant we are able to choose what data to print out. I took data from England, the date for each section of data, the area name, area code, number of new cases by specimen date, cumulative daily number of deaths, and the number of hospital cases. Then I used filters to make sure it was only the data I wanted to use and printed it out. To test this you can run the program and it will print up to the most recent data available which is the day before whatever day it is when the user is reading this. I have also created a filepath for the code to be used in the Flask section of the program.

Task 4 - Automated updates: 

For this task I first imported the time and sched modules. I then created the function with it's arguments. After this I designed the scheduled update to update the data in task 3 at whatever interval the user chooses to set it at. To test this if you go to the bottom of the program it will have "schedule_covid_updates(1,'name') where you can decided how long to set the interval at to test it. 




Covid News:

For this section of the project I first started it by creating a function with an argument and default value. This was so it would access all current Covid related news and print out the sources to the user. I made sure it was only English Covid related news by setting this in the function. To test this you can run the program and it will print all the news sources it accessed with a URL you can click to see. After this I created another function which is able to update the function at a given time interval. This can be changed to whatever the desired interval is by erasing the original time interval and replacing it with the new one. I have also created a filepath for the code to be used in the Flask section of the program.




User Interface:

For this section of the project I started it off by implementing a function that will redirect the webpage to the correct site. After this I imported the functions from the previous parts of the project by inserting them into a function which is used to show the information I have used and will display it on the website. Then I was in the process of creating a function that adds new articles to the user interface, a function that schedules the update for that, and several time conversion functions for more scheduling functions I was planning on doing. To test the website you have to run the program and then go to the logging.log file to copy and paste the link.