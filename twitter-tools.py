import tweepy

class colour:
    purple = '\033[95m'
    blue = '\033[94m'
    green = '\033[92m'
    red = '\033[91m'
    end = '\033[0m'

# Auth
auth = tweepy.OAuthHandler("CONSUMER", "CONSUMER")
auth.set_access_token("ACCESS", "ACCESS")
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

def menu():
    # Menu
    print('Welcome to Twitter Tools!\nPlease choose a tool to begin:\n----------------------\n1. Verified Followers\n2. Remove Followers\n3. Transfer Following\n4. Tweet\n5. Tweet with Image\n----------------------')
    choice = input('')
    # Choices
    if choice == '1':
        print('Verified Followers')
        verifiedFollowers()
    if choice == '2':
        print('Remove Followers')
        removeFollowers()
    if choice == '3':
        print('Transfer Following')
        transferFollowing()
    if choice == '4':
        print('Tweet')
        tweet()
    if choice == '5':
        print('Tweet with Image')
        tweetWithImage()
    else:
        print('Oops, you didn\'t select a valid choice.')
        menu()

def verifiedFollowers():
    from os import environ
    homedir = environ.get("HOME")
    if homedir == None: # on windows it is $HOMEPATH
        homedir = environ.get("HOMEPATH")
    assert type(homedir) == str

    ids = []
    count = int(0)
    personNo = int(1)

    username = input('Enter your username: ')
    print('Finding followers of @' + username + '...')
    for page in tweepy.Cursor(api.followers_ids, screen_name=username).pages():
       ids.extend(page)

    print('Checking for verification...', colour.end)
    for person in page:
        personData = api.get_user(person)
        personVerified = personData.verified
        if personVerified == True:
            count = count + 1
            personUsername = personData.screen_name
            print(colour.green, f'Your follower @{personUsername} is verified! (#{personNo})', colour.end)

            textFile = open(f'{homedir}/verified-followers.txt', 'a')
            textFile.write(personUsername + '\n')
        else:
            personUsername = personData.screen_name
            print(colour.red, f'Your follower @{personUsername} is not verified. (#{personNo})', colour.end)
    
        personNo = personNo + 1


    if count == 0:
        user = api.get_user(username)
        followers = user.followers_count
        followers = int(followers)
        print(colour.purple, 'You have', followers, 'followers.')
        print('Of those, you have no verified followers.', colour.end)
    if count == 1:
        with open (f'{homedir}/verified-followers.txt') as textFileRead:
            lines = textFileRead.readlines()
            follower = str(lines)
            follower = follower.replace('\n', '')
        textFileRead.close()
        user = api.get_user(username)
        followers = user.followers_count
        followers = int(followers)
        print(colour.purple, 'You have', followers, 'followers.')
        print('Of those, you have 1 verified follower. Their username is @' + follower + '.')
        print('You can view a list of all of your verified followers in the text file.', colour.end)


    if count > 1:
        user = api.get_user(username)
        followers = user.followers_count
        followers = int(followers)
        print(colour.purple, 'You have', followers, 'followers.')
        print('Of those, you have', count, 'verified followers.')
        print('You can view a list of all of your verified followers in the text file.')
        percentFollowers = percent(count, followers)
        percentFollowers = int(percentFollowers)
        print(percentFollowers, 'percent of your followers are verified, approximately.', colour.end, colour.blue)
        pieQ = input('Do you want a pie chart created? This will be saved to to your user / home folder. (y/n)')
        print(colour.end)
        if 'y' in pieQ:
            import pygal
            verifiedPie = round(percentFollowers)
            notVerified = followers - count
            notVerifiedPie = percent(notVerified, followers)
            piechart = pygal.Pie()
            piechart.add('Verified', verifiedPie)
            piechart.add('Not Verified', notVerifiedPie)
            piechart.render()
            piechart.render_to_png(f'{homedir}/verified-followers.png')
            print(colour.purple, 'A pie chart with your followers data has been saved to your home folder.', colour.end)




def removeFollowers():
    ids = []

    username = input('Enter your username: ')

    print('Starting to remove followers of', username, '- you\'ll see their Twitter user ID printed out when they have been blocked and unblocked.')
    for page in tweepy.Cursor(api.followers_ids, screen_name=username).pages():
        ids.extend(page)

    for user in ids:
        try:
            api.create_block(user)
            print('Blocked', user)
        except:
            print('There was an error blocking the user with ID', user)
            continue

        try:
            api.destroy_block(user)
            print('Unblocked', user)
        except:
            print('There was an error unblocking the user with ID', user)
        
    print('Your followers should have been removed!')


def transferFollowing():
    usernameOriginal = input('Enter the username of your original account: ')
    usernameNew = input('Enter the username of your new account: ')

    transferKeys = input('Would you like to use the access keys in this file for your new account? If so, these must match the username you entered just now - as the account of which the access keys in the file belongs to will start following everyone your old account used to follow. [Y/N]')
    transferKeys = transferKeys.capitalize
    # User's new account has access keys already in file
    if transferKeys == 'Y':
        ids = []

        # Get IDs of original account's followers
        print('Finding users... ')
        for page in tweepy.Cursor(api.friends_ids, screen_name=usernameOriginal).pages():
            ids.extend(page)
        print('Got following of', usernameOriginal)

        # For each follower in original account's followers
        for user in ids:
            try:
                # Follow the user
                api.create_friendship(user)
                print('Followed', user)
            except:
                print('There was an error following the user with ID', user)
                continue

        print('Your following should have been transferred!')

    # User's new account does not have access keys already in file: will supply new ones
    if transferKeys == 'N':
        newAccountAccess1 = input('Enter the first access key (with a hypen / dash) for your new account: ')
        newAccountAccess2 = input('Enter the second access key for your new account: ')
        # Reconnect to Twitter API with new auth keys
        auth.set_access_token(newAccountAccess1, newAccountAccess2)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

        ids = []

        # Get IDs of original account's followers
        print('Finding users... ')
        for page in tweepy.Cursor(api.friends_ids, screen_name=usernameOriginal).pages():
            ids.extend(page)
        print('Got following of', usernameOriginal)

        # For each follower in original account's followers
        for user in ids:
            try:
                # Follow the user
                api.create_friendship(user)
                print('Followed', user)
            except:
                print('There was an error following the user with ID', user)
                continue

        print('Your following should have been transferred!')

def tweet():
    tweet = input("Enter a Tweet: ")
    api.update_status(tweet)
    print('Tweeted:', tweet)

def tweetWithImage():
    tweet = input("Enter a Tweet: ")

    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    print('Please select an image from the dialog.')
    image = filedialog.askopenfilename()

    media = api.media_upload(image)
    post_result = api.update_status(status=tweet, media_ids=[media.media_id])
    print('Tweeted:', tweet)


def percent(verifiedFollowers,totalFollowers):
    percent = (verifiedFollowers / totalFollowers)
    percent = percent * 100
    return percent

menu()
