# Running2Win-to-Strava-Importer
Automatically imports desired running2win activity data, including descriptions and comments, into Strava

[![Run on Repl.it](https://repl.it/badge/github/sfergusond/Running2Win-to-Strava-Importer)](https://repl.it/github/sfergusond/Running2Win-to-Strava-Importer)

1) Click above button
```
      a. If the link doesn't work: go to www.repl.it
      b. Click "Start Coding <>" in the upper right
      c. Select "Import from Github"
      d. Copy "sfergusond/Running2Win-to-Strava-Importer" and import
```
2) Type ```pip install -r requirements.txt``` into the command line (black window with an orange ">", should show a blinking white cursor on click) and hit ENTER on your keyboard
3) Once the packages have been installed, type desired arguments into the command line. Alternatively, copy an example from below into the command line. Make sure to replace everything inside the double quotes (" ") with your information and desired start/end dates.
4) Hit ENTER on your keyboard and let the program run. It will take a while. Avoid logging into your Strava account while the program runs.
5) Strava.com may timeout before all of your activities are loaded. If so, check the date of the most recent activity that was uploaded and run the program again (from step 3) with the new start date.

Note: Currently the program can only support logging into Strava via a Google account, Facebook account, or email/password combination. It does not work with Apple logins. Make sure the login method flag is set appropriately.

# Usage

```
usage: R2Wbot.py \[-h] -ru r2w_username -rp r2w_password -a after_date -b
                 before_date -su strava_email -sp strava_password

Retrieve R2W data and upload to Strava --- PUT ALL ARGUMENTS IN DOUBLE QUOTES | ex: -ru "myr2wusername" ---

required arguments:
  -ru r2w_username      Running2Win username
  -rp r2w_password      Running2Win password
  -a after_date         Date after which to search for activities on
                        Running2Win --!! MUST BE IN FORMAT: YYYY-MM-DD !!--
  -b before_date        Date at which to stop collecting activities form
                        Running2Win --!! MUST BE IN FORMAT: YYYY-MM-DD !!--
  -su strava_email      Strava username (MUST BE A GOOGLE EMAIL ADDRESS LINKED TO YOUR STRAVA ACCOUNT)
  -sp strava_password   Strava password 

optional arguments:
  -h, --help            show this help message and exit
  -m Strava_login_method
                        Method for logging into Strava, default is Google sign-in
                        Options: "Email" login to Strava via direct email/password combination
                                 "Facebook" login to Strava using Facebook information
```

# Examples

```
python R2WBot.py -ru "runner1" -rp "password1" -a "2016-05-31" -b "2020-04-01" -su "stravarunner1" -sp "password2"
```

This will download every activity, including descriptions and comments, from Running2Win.com between May 31st, 2016 and April 1st, 2020 (both inclusive). The activities will then be uploaded automatically to Strava. 

```
python R2WBot.py -ru "runner1" -rp "password1" -a "2016-05-31" -b "2020-04-01" -su "stravarunner1" -sp "password2" -m "Email"
```

This will download every activity, including descriptions and comments, from Running2Win.com between May 31st, 2016 and April 1st, 2020 (both inclusive). Rather than attempting a Google sign-in, the bot will directly enter the given Strava usser's email and password into the fields on www.strava.com/login.

Note: this will take a long time to run, so it is best to keep your machine on until the upload is complete

# Features

Gathers all activity data from Running2Win (not including acticities marked "NO RUN - OFF", "Other", or "Cross Training/Other"), for each activitiy retrieving its activity type, title, distance, time, description, member comments, race information, and interval information.

Uploads each gathered activity from r2w onto your Strava account. 

In progress: download to CSV option (instead of uploading to Strava), matching Running2Win activity descriptions/race info/interval info/comments to existing Strava activity descriptions rather than creating new activities.
