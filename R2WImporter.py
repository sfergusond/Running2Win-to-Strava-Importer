"""
Created on Thu Apr 30 12:04:19 2020

Author: Spencer Ferguson-Dryden
https://github.com/sfergusond

TO DO: Implement description-only upload

Uses: webbot from https://github.com/nateshmbhat/webbot
"""

from webbot import Browser
import datetime
import time
from bs4 import BeautifulSoup
import r2w_parser

def main():
    args = {}
    
    print('\nStarting R2W Importer\n\nPlease fill out the following fields and hit ENTER on your keyboard after typing each entry.\nEnter options exactly as they appear.')
    
    ru = str(input('Enter your Running2Win username: '))
    args['ru'] = ru
    rp = str(input('Enter your Running2Win password: '))
    args['rp'] = rp
    a = str(input('Enter date of first activity to collect (format: YYYY-MM-DD): '))
    args['a'] = a
    b = str(input('Enter date of last activity to collect (format: YYYY-MM-DD): '))
    args['b'] = b
    c = str(input('Would you like to download to a .csv file or upload to Strava? (Options: csv | upload ): '))
    args['c'] = c
    if c != 'csv':
        m = str(input('How do you login to Strava? (Options: Google | Facebook | Email ): '))
        args['m'] = m 
        if m == 'Google':
            su = str(input('Enter Google account email: '))
            args['su'] = su
            sp = str(input('Enter Google account password: '))
            args['sp'] = sp
        elif m == 'Facebook':
            su = str(input('Enter Facebook account email: '))
            args['su'] = su
            sp = str(input('Enter Facebook account password: '))
            args['sp'] = sp
        else:
            su = str(input('Enter Strava account email: '))
            args['su'] = su
            sp = str(input('Enter Strava account password: '))
            args['sp'] = sp
            
    print('')
    # Run!
    driver(args)

def login_strava(username, password, web, method):
    web.go_to('https:///www.strava.com/login')
    if method == "Google":
        print('Logging into Strava with Google...')
        web.click('Log in using Google')
        web.type(username, into = 'Email or phone')
        web.click('Next')
        time.sleep(3)
        web.type(password, classname = 'Xb9hP')
        web.click('Next')
    elif method == 'Facebook':
        print('Logging into Strava with Facebook...')
        web.click('Log in using Facebook')
        web.type(username, id='email')
        web.type(password, id='pass')
        web.click(id='loginbutton')
    else:
        print('Logging into Strava with email/password...')
        web.type(username, id='email')
        web.type(password, id='password')
        web.click(id='login-button')
    print('Successfully logged into Strava and beginning activity upload...\n')
    time.sleep(5)

def login_r2w(username, password, web):
    web.go_to('https://www.running2win.com/')
    web.click('LOG IN')
    time.sleep(2) # Prevent username from failing to enter
    print('Logging into Running2Win...')
    web.type(str(username), into='Username')
    web.click('NEXT' , tag='span')
    web.type(str(password), into='Password')
    web.click('Login')
    print('Successfully logged into Running2Win and beginning activity download...\n')

def add_strava_entry(run, web):
    # DISTANVT
    web.type(run['distance'], id='activity_distance')
    
    # TIME
    web.type(run['time'][0], id='activity_elapsed_time_hours')
    web.type(run['time'][1], id='activity_elapsed_time_minutes')
    web.type(run['time'][2], id='activity_elapsed_time_seconds')
    
    # TYPE
    web.click(id='activity-type-dd')
    if run['type'] in r2w_parser.r2w_run_types or 'Run' in run['type']:
        web.click('Run', tag='a')
    elif run['type'] == 'Hiking':
        web.click('Hike')
    elif run['type'] == 'Cycling':
        web.click('Ride')
    elif run['type'] == 'Elliptical':
        web.click('Elliptical')
    elif run['type'] in r2w_parser.strava_activity_types:
        scroll = r2w_parser.strava_activity_types.index(run['type'])
        _type = r2w_parser.strava_activity_types[scroll]
        web.scrolly(5)
        if scroll > 9:
            web.scrolly(5*scroll)
        web.click(_type)
    else:
        #web.scrolly(5)
        #web.scrolly(100)
        web.click('Workout')
        
    # DATE
    web.type(run['date'], id='activity_start_date')
    web.click('NEXT', tag='span')
    
    # TITLE
    web.type(run['title'], id='activity_name')
    
    # RUN SUBTYPE
    if 'Long' in run['type']:
        web.click(id='workout-type-run-dd')
        web.click('Long Run')
    elif 'Race' in run['type']:
        web.click(id='workout-type-run-dd')
        web.click('Race')
    elif 'VO2 Max' in run['type'] or 'Endurance' in run['type'] or 'Steady State' in run['type'] or 'Tempo' in run['type'] or 'Hill Training' in run['type'] or 'Fartlek' in run['type'] or 'Speed Training' in run['type'] or 'Threshold' in run['type'] or 'Interval' in run['type']:
        web.click(id='workout-type-run-dd')
        web.click('Workout')
    
    # DESCRIPTION
    web.type(run['description'], id='activity_description')
    
    # DIFFICULTY
    if run['difficulty'] > 1:
        web.click(id='perceived-exertion-slider-1')
        for i in range(run['difficulty']):
            web.press(web.Key.RIGHT)
        web.click('NEXT', tag = 'span')
        
    # SUBMIT
    web.click(xpath='/html/body/div[1]/div[3]/div[1]/form/div[6]/div/input')
    
def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 2, length = 50, fill = '█', printEnd = "\r"):
    """
    Borrowed from: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    """
    
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s \n\n|%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def driver(args):
    import sys
    web = Browser(showWindow=False)
    
    print('Loading https://www.running2win.com ...')
    login_r2w(args['ru'], args['rp'], web)
    
    tmp = (args['a']).split('-')
    start = datetime.date(int(tmp[0]), int(tmp[1]), int(tmp[2]))
    tmp = (args['b']).split('-')
    end = datetime.date(int(tmp[0]),int(tmp[1]), int(tmp[2]))
    delta = datetime.timedelta(weeks=8)
    
    # helpers for progress bar
    total_days_str = str(end - start)
    if 'day' not in total_days_str: total_days = 1
    else: total_days = int(total_days_str[0:total_days_str.find(' day')])
    
    runs = [] # Master list for activities
    
    # Navigate to running log and iterate through 8 week chunks
    count = 0
    while start < end:
        count += 56
        upper = start + delta
        if upper > end:
            upper = end
            count = total_days
        web.go_to('https://www.running2win.com/community/view-member-running-log.asp?sd='+ str(start) + '&ed=' + str(upper))
        start += delta + datetime.timedelta(days=1)
        
        file = web.get_page_source() # convert to html
        f = r2w_parser.log_to_html(file) # store html as text/text file
        t = r2w_parser.get_text(f) # strip text
        gathered = r2w_parser.runs_to_dict(t, f)
        runs.extend(gathered)
        
        progress = f'\rGathered {len(runs)} activities | Most Recent: ' + gathered[0]['date']
        printProgressBar(count, total_days, prefix=progress)
        
    if args['c'] == 'csv':
        import pandas as pd
        for a in runs:
            tmp = a['time']
            if tmp[0] == 0:
                time = f'{tmp[1]}:{tmp[2]}'
            else:
                time = f'{tmp[0]}:{tmp[1]}:{tmp[2]}'
            a['time'] = time
    
        pd.DataFrame(runs).to_csv('activities.csv', index=False)
        print('\nActivities downloaded to \"activities.csv\" in the program\'s folder')
        web.driver.close()
    
    print("\nLoading https://www.strava.com ...")
    login_strava(args['su'], args['sp'], web, args['m'])
    
    count = 0
    for i in runs:
        web.go_to('https://www.strava.com/upload/manual')
        add_strava_entry(i, web)
        
        count += 1
        progress = f'\rAdded activity on ' + i['date'] + f' to Strava | Total = {count} of {len(runs)}'
        printProgressBar(count, len(runs), prefix=progress)
        
    web.driver.close()
    print(f'\nSuccessfully added {count} activities to Strava!')
    
if __name__ == '__main__':
    main()
    
    '''import argparse
    
    parser = argparse.ArgumentParser(description='Retrieve R2W data and upload to Strava -- PUT ALL ARGUMENTS IN DOUBLE QUOTES | ex: -ru \"myr2wusername\" ---')
    parser.add_argument('-ru', type = str, metavar = 'r2w_username', help = 'Running2Win username', required=True)
    parser.add_argument('-rp', type = str, metavar = 'r2w_password', help = 'Running2Win password', required=True)
    parser.add_argument('-a', type = str, metavar = 'after_date', help = 'Date of first activity to import from Running2Win\nMUST BE IN FORMAT: YYYY-MM-DD', required=True)
    parser.add_argument('-b', type = str, metavar = 'before_date', help = 'Date of last activity to import from Running2Win\nMUST BE IN FORMAT: YYYY-MM-DD', required=True)
    parser.add_argument('-su', type = str, metavar = 'strava_login_username/email', help = 'Username/email for Strava/Google/Facebook account, depending on the value of the -m flag', required=False)
    parser.add_argument('-sp', type = str, metavar = 'strava_password', help = 'Password for Strava/Google/Facebook account, depending on the value of the -m flag', required=False)
    parser.add_argument('-m', type = str, default = "Google", metavar = 'strava_login_method', help = 'Method for logging into Strava, default is Google sign-in\nDefault: \"Google\" (if you do not include this argument, it will default to Google sign-in)\nOptions: \"Email\" login to Strava via direct email/password combination\n\"Facebook\" login to Strava using Facebook\n"Google" login to Strava using Google', required = False)
    parser.add_argument('-c', type = str, default = "upload", metavar = 'upload/download_method', help = 'Default: \"upload\" (if you do not include this argument, activities will be uploaded to Strava)\nOptions: \"upload\" to upload all activity data to Strava\n\"csv\" to import data to a local csv file (no upload or Strava login)', required = False)
    args = parser.parse_args()
    
    # fix any whitespace issues
    for a in vars(args):
        arg = getattr(args, a)
        if arg == None: continue
        if arg[0] == '\'' and arg[-1] == '\'':
            arg = arg.replace('\'','')
            setattr(args, a, arg)
            
    vals = {'ru': args.ru, 'rp': args.rp, 'a': args.a, 'b': args.b, 'c': args.c, 'm': args.m, 'su': args.su, 'sp': args.sp}
            
    # Run!        
    driver(vals)'''
    