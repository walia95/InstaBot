import requests
import urllib
import csv
import datetime
from tagdataplot import plotter, category_plotter, user_category_plotter

# my key
APP_ACCESS_TOKEN = "4014843938.9c149eb.91bc0f0e338141778eca564866074b2f"
BASE_URL = "https://api.instagram.com/v1/"
MENU_LIST = ["Fetch personal information.","Fetch info of a user.", "Fetch your most recent post",
             "Fetch most recent posts of a user", "Fetch most recent posts liked by you", "Like most recent post of a user",
             "Fetch list of comments on a user's recent post", "Post comment on a user's post" ,
             "Fetch comments on your latest post ", "Fetch user posts in creative styles", "Fetch number of posts on a hashtag",
             "Fetch categorised hashtag trends with advance data analytics services",
             "Fetch desired data pattern from haszhtag analysis",
             "Quit"]




# method to download files
def download_method(r):
    if r['meta']['code'] == 200:
        if len(r['data']):
            for i in range(0, len(r['data'])):

                if r['data'][i]['type'] == "image":
                    url = r['data'][i]['images']['low_resolution']['url']
                    # checking whether the image is a gif by tearing up the url to get extension of file
                    if url[-3:] == "gif":
                        name = r['data'][i]['id'] + '.gif'
                    else:
                        name = r['data'][i]['id'] + '.png'

                elif r['data'][i]['type'] == "video":
                    name = r['data'][i]['id'] + '.mp4'
                    url = r['data'][i]['videos']['low_resolution']['url']

                print 'ID: '+ name
                print 'Media Details: ' + url
                try:
                    urllib.urlretrieve(url, 'media/' + name)
                except:
                    print "Download error!"
                print '\n'
        else:
            print '\n No data or media found!'
    else:
        print "Response couldn't be fetched!"




# method to access self info
def fetch_self_info():
    req_url = BASE_URL+'users/self/?access_token=%s' % APP_ACCESS_TOKEN
    try:
        r = requests.get(req_url).json()
        if r['meta']['code'] == 200:
            if len(r['data']):
                print 'Username: %s' % (r['data']['username'])
                print 'No. of followers: %s' % (r['data']['counts']['followed_by'])
                print 'No. of people you are following: %s' % (r['data']['counts']['follows'])
                print 'No. of posts: %s' % (r['data']['counts']['media'])
            else:
                print 'There is no data for this user!'
    except:
        print "Url request exception occurred!"




# method to fetch username from the api
def fetch_uid(username):
    uid = None
    req_url = BASE_URL + 'users/search?q=%s&access_token=%s' % (username,APP_ACCESS_TOKEN)
    try:
        user_info=requests.get(req_url).json()
        if user_info['meta']['code'] == 200:
            if len(user_info['data']):
                return user_info['data'][0]['id']
        else:
            print "Status code not 200!"
    except:
        print "Url request exception occurred!"
    return uid




# method to fetch user details using the uid
def fetch_other_user(uid):
    # print uid for easiness's sake
    print uid
    if uid is None:
        print 'Username could not be fetched! \n\n'
    else:
        req_url=BASE_URL+'users/%s?access_token=%s' % (uid, APP_ACCESS_TOKEN)
        try:
            r=requests.get(req_url).json()
            if r['meta']['code'] == 200:
                if len(r['data']):
                    print 'Username: %s' % (r['data']['username'])
                    print 'No. of followers: %s' % (r['data']['counts']['followed_by'])
                    print 'No. of people he/she is following: %s' % (r['data']['counts']['follows'])
                    print 'No. of posts: %s' % (r['data']['counts']['media'])
                else:
                    print 'There is no data for this user!'
            else:
                print 'Status code other than 200 received!'
        except:
            print "exception occurred!"




# method to fetch self posts
def fetch_self_posts(num_posts):
    req_url = BASE_URL+"users/self/media/recent/?access_token=%s&count=%s" % (APP_ACCESS_TOKEN, str(num_posts))
    try:
        r = requests.get(req_url).json()

    except:
        print "Request couldn't be made"
        return
    download_method(r)




# method to fetch others posts
def fetch_other_posts(user_name, num_posts):
    uid = fetch_uid(user_name)
    if uid is not None:
        req_url = BASE_URL + "users/%s/media/recent/?access_token=%s&count=%s" % (uid, APP_ACCESS_TOKEN, str(num_posts))

        try:
            user_media = requests.get(req_url).json()
        except:
            print "Request couldn't be made"
            return
        download_method(user_media)
    else:
        print "User doesn't exist!"




# method to fetch most recent post liked by self
def fetch_most_recent_liked_self(num_posts):
    req_url = BASE_URL + "users/self/media/liked?access_token=%s&count=%s" % (APP_ACCESS_TOKEN, str(num_posts))

    try:
        r = requests.get(req_url).json()
    except:
        print "Request couldn't be made"
        return
    download_method(r)




# method to fetch self most recent post id
def fetch_self_most_recent_media_id():
    req_url = BASE_URL + "users/self/media/recent/?access_token=%s&count=3" % (APP_ACCESS_TOKEN)

    try:
        user_media = requests.get(req_url).json()
    except:
        print "Request couldn't be made"
        return

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print "Failed to fetch post!"
    else:
         print "Failed to fetch post!"
    return None




# method to fetch media id for recent post of user
def fetch_most_recent_media_id(uid):
    req_url = BASE_URL + "users/%s/media/recent/?access_token=%s&count=3" % (uid, APP_ACCESS_TOKEN)

    try:
        user_media = requests.get(req_url).json()
    except:
        print "Request couldn't be made"
        return

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print "Failed to fetch post!"
    else:
         print "Failed to fetch post!"
    return None




# method to like the most recent post of a user
def like_user_post(user_name):
    uid=fetch_uid(user_name)
    if uid is None:
        print "User doesn't exist!"
        return
    else:
        media_id=fetch_most_recent_media_id(uid)

        if media_id is not None:
            req_url=BASE_URL + "media/%s/likes" % str(media_id)
            token_payload = {"access_token": APP_ACCESS_TOKEN}

            try:
                r=requests.post(req_url, token_payload).json()
            except:
                print "Request couldn't be made"
                return

            if r['meta']['code'] != 200:
                print "Failed to like the post! 11"
            else:
                print "Keep liking more!"
        else:
            print "Failed to like the post!22"
    return




# method to fetch comments on the latest post of a user by username
def fetch_user_recent_post_comments(user_name):
    uid = fetch_uid(user_name)
    if uid is not None:
        media_id = fetch_most_recent_media_id(uid)
        if media_id is not None:
            req_url = BASE_URL + "media/%s/comments?access_token=%s" % (str(media_id), APP_ACCESS_TOKEN)
            try:
                r = requests.get(req_url).json()
            except:
                print "Request couldn't be made"
                return

            if r['meta']['code'] == 200:
                if len(r['data']):
                    print "The comments are :- \n"
                    for i in range(0,len(r['data'])):
                        print r['data'][i]['from']['full_name'] + ": " + r['data'][i]['text']
                else:
                    print "No comments yet! Be the first one to comment!"
            else:
                print "Data inaccessible!"
        else:
            print "Posts not found!"
    else:
        print "User doesn't exist!"




# method to fetch comments on the latest post of a user by username
def fetch_self_recent_post_comments():
        media_id = fetch_self_most_recent_media_id()
        if media_id is not None:
            req_url = BASE_URL + "media/%s/comments?access_token=ACCESS-TOKEN%s" % (str(media_id), APP_ACCESS_TOKEN)
            try:
                r = requests.get(req_url).json()
            except:
                print "Request couldn't be made"
                return

            if r['meta']['code'] == 200:
                if len(r['data']):
                    print "The comments are :- \n"
                    for i in range(0, len(r['data'])):
                        print r['data'][i]['text']
                else:
                    print "No comments yet! Be the first one to comment!"
            else:
                print "Data inaccessible!"
        else:
            print "Posts not found!"




# method to add to comment in the most recent user post
def post_comment_most_recent(user_name):
    uid = fetch_uid(user_name)

    if uid is not None:
        media_id = fetch_most_recent_media_id(uid)

        if media_id is not None:
            req_url = BASE_URL + "media/%s/comments" % media_id
            print "Please not that the comment should not exceed 300 characters, should not be in ALL capitals, " \
                  "should not contain more than 4 hashtags and one URL link."
            comment_msg = raw_input("Your comment: ")
            comment_payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_msg}
            try:
                r = requests.post(req_url,comment_payload).json()
            except:
                print "Request couldn't be made"
                return

            if r['meta']['code'] == 200:
                print "Comment posted successfully!"
            else:
                print "Failed to post comment. Try again!"

        else:
            print "Posts not found!"
    else:
        print "User doesn't exist!"




#  method to collect tag data from images and plot
def tag_collect(tag_name):
    req_url=BASE_URL+'tags/%s?access_token=%s'% (tag_name,APP_ACCESS_TOKEN)
    try:
        r = requests.get(req_url).json()
    except:
        print "Request couldn't be made"
        return

    if r['meta']['code'] == 200:
        if len(r['data']):
            print 'Number of images with the tag %s: %d ' % (tag_name, r['data']['media_count'])
            f = open("collection.csv",'ab')
            writer = csv.writer(f)
            writer.writerow([tag_name, r['data']['media_count']])
            f.close()
    plotter()




# method to collect data on various topics n plot trend
def trend_collect():
    politics_count = 0
    sports_count = 0
    entertainment_count = 0


    error_flag = False
    trends = {"politics": ["india", "america", "trump", "obama", "modi", "namo", "brexit"],

              "sports": ["football", "tennis", "cricket", "badminton", "realmadrid", "olympics"],

              "entertainment": ["hollywood", "bollywood", "films", "music", "theatre", "dance", "comedy"]
              }
    try:
        for category in trends:

                for i in range(0, len(trends[category])):
                    req_url = BASE_URL + 'tags/search?q=%s&access_token=%s' % (trends[category][i], APP_ACCESS_TOKEN)
                    r = requests.get(req_url).json()
                    if r['meta']['code'] == 200:
                        if len(r['data']):
                            for j in range(0, len(r['data'])):
                                if category == "politics":
                                    politics_count += r['data'][j]['media_count']

                                elif category == "sports":
                                    sports_count += r['data'][j]['media_count']

                                elif category == "entertainment":
                                    entertainment_count += r['data'][j]['media_count']
    except:
        print "Failed to fetch and analyse data"
        error_flag = True

    if error_flag is False:
        f = open("category_trend.csv", 'wb')
        writer = csv.writer(f)
        writer.writerow(['politics', politics_count])
        writer.writerow(['sports', sports_count])
        writer.writerow(['entertainment', entertainment_count])
        writer.writerow(["timestamp", datetime.datetime.now()])
        f.close()

        category_plotter()


# method to plot various stats by taking user input
def user_def_trends():
    trend_list = []
    val_list = []
    ans = True
    while ans is True:

        trend_list.append(raw_input("Enter tag to plot data for: "))
        if raw_input("Do you want to add more tags (y/n) ?")[0].upper() == 'Y':
            ans = True
        else:
            ans = False
    f = open("custom_category_trend.csv", 'wb')
    writer = csv.writer(f)
    try:
        for i in range(0, len(trend_list)):
            req_url = BASE_URL + 'tags/search?q=%s&access_token=%s' % (trend_list[i], APP_ACCESS_TOKEN)
            try:
                r = requests.get(req_url).json()
            except:
                print "couldn't make the request"
                return
            if r['meta']['code'] == 200:
                if len(r['data']):
                    count = 0
                    for j in range(0, len(r['data'])):
                        count += r['data'][j]['media_count']
                    writer.writerow([trend_list[i], count])

        writer.writerow(["timestamp", datetime.datetime.now()])
    except:
        print "Failed to fetch and analyse data"

    f.close()
    user_category_plotter()


# method to choose with atleast this much likes
def atleast_n_likes(r, n):

    for i in range(0, len(r['data'])):
        if r['data'][i]['likes'] < n:
            r['data'].pop(i)
    download_method(r)
    return r


# method to choose with minimum likes
def minimum_likes(r):
    t = None
    n = r['data'][0]['likes']
    for i in range(1, len(r['data'])):
        if r['data'][i]['likes'] < n:
            n = r['data'][i]['likes']
            t = r['data'][i]
    if t is not None:
        if t['type'] == "image":
            url = t['images']['low_resolution']['url']
            # checking whether the image is a gif by tearing up the url to get extension of file
            if url[-3:] == "gif":
                name = t['id'] + '.gif'
            else:
                name = t['id'] + '.png'

        elif t['type'] == "video":
            name = t['id'] + '.mp4'
            url = t['videos']['low_resolution']['url']

        print 'ID: ' + name
        print 'Media Details: ' + url
        try:
            urllib.urlretrieve(url, 'media/' + name)
        except:
            print "Download error!"


# method to choose with max likes
def max_likes(r):

    t = None
    n = r['data'][0]['likes']
    for i in range(1, len(r['data'])):
        if r['data'][i]['likes'] >= n:
            n = r['data'][i]['likes']
            t = r['data'][i]

    if t is None:
        t = r['data'][0]

    if t['type'] == "image":
        url = t['images']['low_resolution']['url']
        # checking whether the image is a gif by tearing up the url to get extension of file
        if url[-3:] == "gif":
            name = t['id'] + '.gif'
        else:
            name = t['id'] + '.png'

    elif t['type'] == "video":
        name = t['id'] + '.mp4'
        url = t['videos']['low_resolution']['url']

    print 'ID: ' + name
    print 'Media Details: ' + url
    try:
        urllib.urlretrieve(url, 'media/' + name)
    except:
        print "Download error!"



# method to choose with desired type
def my_type(r, type_name):

    for i in range(0, len(r['data'])):
        if r['data'][i]['type'] == type_name:
            t = r['data'][i]
            if t is not None:
                if t['type'] == "image":
                    url = t['images']['low_resolution']['url']
                    # checking whether the image is a gif by tearing up the url to get extension of file
                    if url[-3:] == "gif":
                        name = t['id'] + '.gif'
                    else:
                        name = t['id'] + '.png'

                elif t['type'] == "video":
                    name = t['id'] + '.mp4'
                    url = t['videos']['low_resolution']['url']

                print 'ID: ' + name
                print 'Media Details: ' + url
                try:
                    urllib.urlretrieve(url, 'media/' + name)
                except:
                    print "Download error!"


# method to choose with desired filter
def my_filter(r, type_name):

    for i in range(0, len(r['data'])):
        if r['data'][i]['filter'] == type_name:
            t = r['data'][i]
            if t is not None:
                if t['type'] == "image":
                    url = t['images']['low_resolution']['url']
                    # checking whether the image is a gif by tearing up the url to get extension of file
                    if url[-3:] == "gif":
                        name = t['id'] + '.gif'
                    else:
                        name = t['id'] + '.png'

                elif t['type'] == "video":
                    name = t['id'] + '.mp4'
                    url = t['videos']['low_resolution']['url']

                print 'ID: ' + name
                print 'Media Details: ' + url
                try:
                    urllib.urlretrieve(url, 'media/' + name)
                except:
                    print "Download error!"


# method to choose the post from recent media of the user creatively
def choose_creative(user_name,num_posts):
    # specific fetch menu list

    MENU_LIST_CREATIVE=["Search media with atleast a specific number of likes ", "Search media with minimum likes",
                        "Get media with maximum likes", "Search media with specific type(Video/Images)",
                        "Search by specific filter", "Quit"]

    uid = fetch_uid(user_name)
    if uid is not None:
        req_url = BASE_URL + "users/%s/media/recent/?access_token=%s&count=%s" % (uid, APP_ACCESS_TOKEN, str(num_posts))

        try:
            user_media = requests.get(req_url).json()
        except:
            print "Failed to fetch your services"
            return
        while True:
            print "Please select choice of media filter :- \n"

            for i in range(0,len(MENU_LIST_CREATIVE)):
                print '%d. %s' % (i+1, MENU_LIST_CREATIVE[i])

            try:
                menu_choice = int(raw_input())
            except:
                print 'Something\'s wrong with your choice! \n Try again! '

            if menu_choice == 1:
                try:
                    n = int(raw_input("Enter the minimum number of likes to look for "))
                    atleast_n_likes(user_media, n)
                except:
                    print "Wrong input choice! Try again"

            elif menu_choice == 2:
                minimum_likes(user_media)

            elif menu_choice == 3:
                max_likes(user_media)

            elif menu_choice == 4:
                type_name = raw_input("Enter the type that you would like to fetch(video/image) ")
                my_type(user_media, type_name)

            elif menu_choice == 5:
                type_name = raw_input("Enter the filter name that you would like to fetch ")
                my_filter(user_media, type_name)
            else:
                return
    else:
        print "User doesn't exist!"


# method to show menu and take input
def show_menu():

    print "Welcome to InstaBot! \n What are you upto today? Let's pick from the menu"

    while True:

        for i in range(0,len(MENU_LIST)):
            print '%d. %s' % (i+1, MENU_LIST[i])

        try:
            menu_choice = int(raw_input())
        except:
            print 'Something went wrong with your answer! \n Try again! '
        if menu_choice == 1:
            fetch_self_info()

        elif menu_choice == 2:
            u_name = raw_input("Enter the username to fetch details ")
            fetch_other_user(fetch_uid(u_name))

        elif menu_choice == 3:
            num_of_posts = raw_input("Enter the number of posts that you would like to fetch ")
            fetch_self_posts(num_of_posts)

        elif menu_choice == 4:
            user_name = raw_input("Enter the name of user that you would like to fetch ")
            num_of_posts = raw_input("Enter the number of posts that you would like to fetch ")
            fetch_other_posts(user_name, num_of_posts)

        elif menu_choice == 5:
            num_of_posts = raw_input("Enter the number of posts that you would like to fetch ")
            fetch_most_recent_liked_self(num_of_posts)

        elif menu_choice == 6:
            user_name = raw_input("Enter the name of user ")
            like_user_post(user_name)

        elif menu_choice == 7:
            user_name = raw_input("Enter the name of user ")
            fetch_user_recent_post_comments(user_name)

        elif menu_choice == 8:
            user_name = raw_input("Enter the name of user ")
            post_comment_most_recent(user_name)

        elif menu_choice == 9:
            fetch_self_recent_post_comments()

        elif menu_choice == 10:
            user_name = raw_input("Enter the name of user that you would like to fetch ")
            num_of_posts = raw_input("Enter the number of posts that you would like to search from ")
            choose_creative(user_name,num_of_posts)

        elif menu_choice == 11:
            tag_name = raw_input("Enter a tag to search ")
            tag_collect(tag_name)

        elif menu_choice == 12:
            trend_collect()

        elif menu_choice == 13:
            user_def_trends()

        else:
            print 'Quitting...'
            exit(0)
        print '\n\n'


show_menu()
