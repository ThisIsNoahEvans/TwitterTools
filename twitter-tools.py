import tweepy

# Auth
auth = tweepy.OAuthHandler("CONSUMER", "CONSUMER")
auth.set_access_token("ACCESS", "ACCESS")
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

def menu():
    # Menu
    print('Welcome to Twitter Tools!\nPlease choose a tool to begin:\n----------------------\n1. Verified Followers\n2. Remove Followers\n3. Transfer Followers\n4. Tweet\n----------------------')
    choice = input('')
    # Choices
    if choice == '1':
        print('Verified Followers')
        verifiedFollowers()

def verifiedFollowers():
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
        # Comment out the whole 'else' block if you don't want every follower to be printed
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
            print(colour.purple, 'A pie chart with your followers data has been saved to your home folder. See the GitHub repository\'s README for more.', colour.end)


def percent(verifiedFollowers,totalFollowers):
    percent = (verifiedFollowers / totalFollowers)
    percent = percent * 100
    return percent