import tweepy

# Colour for print statements
class colour:
    purple = '\033[95m'
    blue = '\033[94m'
    green = '\033[92m'
    red = '\033[91m'
    end = '\033[0m'

# Auth
auth = tweepy.OAuthHandler("CONSUMER", "CONSUMER")
# The acces keys should belong to the account you wish to carry out the tools with (an exception for Transfer Followers, run it for more infos)
auth.set_access_token("ACCESS", "ACCESS")
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

# Menu to choose tool
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
    # User entered something other than 1...5
    else:
        print('Oops, you didn\'t select a valid choice.')
        menu()

# Verified Followerss 
def verifiedFollowers():
    # Get user's home directory
    from os import environ
    homedir = environ.get("HOME")
    # On Windows, it is HOMEPATH
    if homedir == None:
        homedir = environ.get("HOMEPATH")
    assert type(homedir) == str

    # IDs of followers
    ids = []
    # Count of verified followers
    count = int(0)
    # Count of all followers
    personNo = int(1)

    username = input('Enter your username: ')
    print('Finding followers of @' + username + '...')
    # Add the IDs of every one of the user's followers to 'ids'
    for page in tweepy.Cursor(api.followers_ids, screen_name=username).pages():
       ids.extend(page)

    # Open the text file
    textFile = open(f'{homedir}/verified-followers.txt', 'a')
    print('Checking for verification...', colour.end)
    # For each follower (person) in 'ids'
    for follower in ids:
        # Get the follower's data
        followerData = api.get_user(follower)
        # Get their screen name
        followerUsername = followerData.screen_name
        # A bool dictating if the follower is verified or not
        followerVerified = followerData.verified
        
        # If the follower is verified
        if followerVerified == True:
            count = count + 1
            print(colour.green, f'Your follower @{followerUsername} is verified! (#{personNo})', colour.end)
            # Add the user to the text file
            textFile.write(followerUsername + '\n')
        # If the follower is not verified
        else:
            print(colour.red, f'Your follower @{followerUsername} is not verified. (#{personNo})', colour.end)
    
        personNo = personNo + 1

    # Close the text file
    textFile.close()
    # If the user has 0 verified followers
    if count == 0:
        # Get the user data of the person using this tool
        userData = api.get_user(username)
        followers = userData.followers_count
        followers = int(followers)
        print(colour.purple, 'You have', followers, 'followers.')
        print('Of those, you have no verified followers.', colour.end)
    # If the user has 1 verified follower
    if count == 1:
        # Open the text file
        with open (f'{homedir}/verified-followers.txt') as textFileRead:
            # Get each line of the text file (should only be one for one verified follower)
            lines = textFileRead.readlines()
            follower = str(lines)
            # Remove the line break
            follower = follower.replace('\n', '')
        # Close the file
        textFileRead.close()
        # Get the user data of the person using this tool
        userData = api.get_user(username)
        followers = userData.followers_count
        followers = int(followers)
        print(colour.purple, 'You have', followers, 'followers.')
        print('Of those, you have 1 verified follower. Their username is @' + follower + '.')

    # If the user has more than one verified follower
    if count > 1:
        # Get the user data of the person using this tool
        userData = api.get_user(username)
        followers = userData.followers_count
        followers = int(followers)
        print(colour.purple, 'You have', followers, 'followers.')
        print('Of those, you have', count, 'verified followers.')
        print('You can view a list of all of your verified followers in the text file.')
        # Get the percentage of verified followers to total followers
        percentFollowers = percent(count, followers)
        percentFollowers = int(percentFollowers)
        print(percentFollowers, 'percent of your followers are verified, approximately.', colour.end, colour.blue)
        pieQ = input('Do you want a pie chart created? This will be saved to to your user / home folder. (y/n)')
        print(colour.end)
        # If user wants a pie chart
        if 'y' in pieQ:
            import pygal
            # Round the percentage of followers who are verified
            verifiedPie = round(percentFollowers)
            # Work out the percent of followers who are not verified - total followers minus the verified followers
            notVerified = followers - count
            # Get the percentage of the not verified followers
            notVerifiedPie = percent(notVerified, followers)
            # Define the piechart
            piechart = pygal.Pie()
            piechart.add('Verified', verifiedPie)
            piechart.add('Not Verified', notVerifiedPie)
            # Render the pie chart
            piechart.render()
            # Save the pie chart
            piechart.render_to_png(f'{homedir}/verified-followers.png')
            print(colour.purple, 'A pie chart with your followers data has been saved to your home folder.', colour.end)



# Remove Followers
def removeFollowers():
    ids = []

    username = input('Enter your username: ')

    print('Starting to remove followers of', username, '- you\'ll see their Twitter user ID printed out when they have been blocked and unblocked.')
    # Get followers of user
    for page in tweepy.Cursor(api.followers_ids, screen_name=username).pages():
        ids.extend(page)

    # For each user in list of followers
    for user in ids:
        try:
            # Block the user
            api.create_block(user)
            print('Blocked', user)
        except:
            print('There was an error blocking the user with ID', user)
            continue

        try:
            # Unblock the user
            api.destroy_block(user)
            print('Unblocked', user)
        except:
            print('There was an error unblocking the user with ID', user)
        
    print('Your followers should have been removed!')

# Transfer Following
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

# Tweet:
def tweet():
    tweet = input("Enter a Tweet: ")
    # Post Tweet
    api.update_status(tweet)
    print('Tweeted:', tweet)

def tweetWithImage():
    tweet = input("Enter a Tweet: ")

    # Initalise Tkinter
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    print('Please select an image from the dialog.')
    # Select file
    image = filedialog.askopenfilename(filetypes=[('PNG images', '.png'), ('JPEG images', '.jpg'), ('GIF images', '.gif')])

    # Uplod the image to Twitter
    media = api.media_upload(image)
    # Post the Tweet
    api.update_status(status=tweet, media_ids=[media.media_id])
    print('Tweeted:', tweet)

# Percent function for Verified Followers
def percent(verifiedFollowers,totalFollowers):
    percent = (verifiedFollowers / totalFollowers)
    percent = percent * 100
    return percent

# Run the menu when program launched
menu()
