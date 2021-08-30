---- INTRO

This application was developed in Python 3.6 using Django 2.2.1 and PostgreSQL 10, just create a virtualenv and run
pip install -r requirements.txt to install the libs necessary to run the project.

I added one lib in special (requests) because i personally think is easier to work and more readable.

I opted to use pure django project with some frontend libs based in jquery (classical method) because i dont know if
you guys use some lib more complete like angular and react. In my work we created a restfull backend with django
(using DRF) and for frontend angularJS (migrating very slowly to new angular), but all ours apps are already in
angular 7, everything consuming our rest backend

There is two apps (base and weather):

1) base is for everything generic that will be used in the system like management commands, template tags,
abstract models. I personally like to create the index page inside de base because the index usually is a static page
that apoint to alot of things.

2) weather correspond to our application in fact

---- OBSERVATIONS ABOUT THE REQUIREMENTS

1) The configuration for Google Geocoding API is localized in settings.py (KEY and URL).
I created a class to work with the API: onsign/utils/GoogleAPI

2) The configuration for Dark Sky API is localized in settings.py (KEY and URL).
I created a class to work with the API: onsign/utils/DarkSkyAPI

3) I didnt understand well this part. Here my thoughts:
    3.1) I assumed the temperature doesnt vary within the same lat/lng
    3.2) "with three decimal cases precision", I assumed you was speaking about the lat/lng so i rounded the lat/lng,
    maybe you was speaking about the temperature... i became confused
    3.3) "within an 1-hour window", This really killed me (lol), I saw the API return a lot of data grouped by
    hourly, daily, minutely, currently etc... I applied the currently group. I understand "1-hour window" like a extra
    time to do something like "The time to finish this is 17pm, but i give you 1 hour window" (so i can fish at 18pm),
    maybe you wanted to get the array of all temperatures based in currently time like:

        suppose now is 17pm, i need to know all temperature from 17 to 18pm
        suppose now is 17pm, i need to know all temperature from 16:30 to 17:30pm
        suppose now is 17pm, i need to know all temperature from 16:00 to 17:00pm

    I really became confused with the requirement and choose to get the currently temperature, is not hard to change
    this and is something to discuss before complete the task and deploy to the client.

4) Every request is saved in DB, even if it return a exception (to track errors and adjust)

5) The custom management command is export_data localized in base/management/commands/export_data.py
I implemented JSON and CSV, its just a parameter to choose what you prefer, default is JSON.
