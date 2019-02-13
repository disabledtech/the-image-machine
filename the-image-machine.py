import praw
import os
import re
import requests
import time
import argparse
import prawcore


def main():

    # Get command line arguments
    args = argument_parser()

    subreddit = args.subreddit  # Which subreddit to download from.
    wait_time = args.wait  # How long to wait between searches (in seconds)
    limit = args.limit  # Limit how many new posts to process.
    repeat = args.repeat  # Continuously grab images, waiting *wait_time* between loops.
    nsfw = args.nsfw  # Include NSFW results. Default False.
    sort = args.sort  # Method of sorting when getting subreddit posts.

    # See Authentication class for info if you want to modify these values.
    auth_file = Authentication(client_id='zlGNo2QoKclQlQ',
                               useragent='script by /u/AntiHydrogen v0.1')

    reddit = login(auth_file)  # Log into reddit.

    # Make sure the user has input a real subreddit.
    while not valid_subreddit(reddit, subreddit):
        print("ERROR! I can't find the subreddit '{}'.\n".format(subreddit))
        print("Check for typos or if you are sure it exists it may be private.\n"
              "This script can only access public subreddits. See the Authentication\n"
              "class for possible fixes. You can message me on Reddit (/u/AntiHydrogen)\n"
              "or Github (disabledtech) if you need help.\n".format(subreddit))

        subreddit = input("Enter subreddit name: ")

    print("Getting a maximum of {} images from reddit.com/r/{}. Sorting by: {}".format(limit, subreddit, sort))
    print("Saving images to *script-directory*/subreddit-images/{}\n".format(subreddit))

    while True:

        grab_image_links(reddit=reddit,
                         subreddit_name=subreddit,
                         limit=limit,
                         nsfw=nsfw,
                         mode=sort)
        if repeat:

            print('Waiting for {} seconds.\n'.format(wait_time))
            time.sleep(wait_time)

        else:

            print('Images grabbed. Exiting.')
            break


class Authentication(object):
    """ A class which holds the details needed to start a PRAW reddit object.
        My implementation works with reddit in read-only mode which can grab
        images from public subreddits so we do not use a client_secret,
        username, or password. I /assume/ you could add in a username,
        password, and  client_secret to use private subreddits accessible to
        your account, however, this is untested and may not work (insert
        ominous music here).

        See 'https://www.reddit.com/prefs/apps/' to create your own app if you
        want to use a personal client_id/secret.

    Attributes:
        client_id       Reddit application client-id
        client_secret   Reddit application client_secret. We do not use a
                        secret in this script because we need read-only access
        useragent       A useragent to identify ourselves to Reddit.
        username        Reddit username
        password        Reddit password

    """
    def __init__(self, client_id, useragent):
        self.client_id = client_id
        self.client_secret = None
        self.useragent = useragent
        self.username = None
        self.password = None


class Image(object):
    """ A class which represents all the attributes of a reddit image post
        that we need to download images.

    Attributes:
        title       The title of the post
        url         The URL of the image
        subreddit   The subreddit where the image is from
        extension   The file extension. (ex. '.jpg')
        name        The name of the file. Random characters, usually, but
                    useful to make sure we're not downloading duplicates.
        nsfw        Is the post marked NSFW on Reddit. True or False.
        save_name   The name this image will be saved as if we call .save()

    """

    def __init__(self, title, url, subreddit, file_extension, file_name, nsfw):
        self.title = title
        self.url = url
        self.subreddit = subreddit
        self.extension = file_extension
        self.name = file_name
        self.nsfw = nsfw
        self.save_name = self.get_save_name()

    def get_save_name(self):
        """ Returns a name to save the file as. """

        # Characters which are not alphanumeric that we still want to keep.
        keep_these_char = (' ', '.', '_')

        save_name = "".join(c for c in self.title if c.isalnum() or c in
                            keep_these_char).rstrip() \
                    + " - {}{}".format(self.name, self.extension)

        # Attempt to protect ourselves from an absurdly long title.
        if len(save_name) > 130:
            # Cut the file name down to the first and last 60 char.
            save_name = save_name[:60] + '...' + save_name[-60:]

        return save_name

    def exists(self):
        """ Check if file exists in the subreddit directory by checking the end
        of the file names against the file name in the URL."""

        if os.path.exists(os.path.join('subreddit-images', self.subreddit)):

            for file in os.listdir(os.path.join('subreddit-images', self.subreddit)):
                if file.endswith(self.name + self.extension):

                    return True  # Found

            return False  # No match found

        else:

            # If there's no subreddit directory the file cannot exist.
            return False

    def save(self):
        """ Save this image to a directory named after the subreddit
        it was found in. The directory will be created if it does not exist."""

        try:

            os.makedirs(os.path.join('subreddit-images', self.subreddit))

        except FileExistsError:

            pass

        print("Downloading: {}".format(self.save_name))

        res = requests.get(self.url, headers={'User-agent': 'script by /u/AntiHydrogen 0.1'})
        res.raise_for_status()

        image_file = open(os.path.join('subreddit-images', self.subreddit, os.path.basename(self.save_name)), 'wb')

        for chunk in res.iter_content(100000):
            image_file.write(chunk)

        image_file.close()


def valid_subreddit(reddit, subreddit_name):
    exists = True
    try:
        reddit.subreddits.search_by_name(subreddit_name, exact=True)
    except prawcore.exceptions.NotFound:
        exists = False

    return exists


def grab_image_links(reddit, subreddit_name, limit, nsfw, mode):
    """ Checks for new images and downloads them to a folder named after the subreddit """

    subreddit = set_search_mode(reddit, subreddit_name, mode, limit)  # Choose a subreddit.

    valid_image_regex = re.compile(r"(http.+?)(\w+)(\.\w+)+(?!.*(\w+)(\.jpg|\.png)+)")

    for post in subreddit:

        # Used to check if the URL matches one for an image, get the extension, and file name.
        our_image_regex = valid_image_regex.search(post.url)

        # Init an image object with all the attr. our downloader will need.
        download_this_image = Image(title=post.title,
                                    url=post.url,
                                    subreddit=subreddit_name,
                                    file_name=our_image_regex.group(2),
                                    file_extension=our_image_regex.group(3),
                                    nsfw=post.over_18)
        
        # Check that the URL a valid image and then check that it does not exist already.
        if (not nsfw and not download_this_image.nsfw) or nsfw:
            if is_image(download_this_image.url) and not download_this_image.exists():
                download_this_image.save()


def is_image(url):
    """ Check URLs against as regex which determines if it is a valid
    image URL. Valid URLs are from the domain 'i.redd.it' or 'i.imgur.com' and
    end in .jpg or .png.

    TODO Change from regex to something less overkill? Leaving asserts in for now just in case...
    """

    valid_image = re.compile(r'''(https?://(?:i\.redd\.it|i\.imgur\.com).*\.(?:png|jpg))''')

    assert valid_image.search('https://i.imgur.com/QpOvnoL.jpg') is not None, \
        'Error. i.imgur.com links ARE NOT validating in is_image()'

    assert valid_image.search('https://i.redd.it/luce08zttse21.jpg') is not None, \
        'Error. i.redd.it links ARE NOT validating in is_image()'

    assert valid_image.search('https://www.youtube.com/watch?v=dQw4w9WgXcQ') is None, \
        'Error. Non-image links ARE validating in is_image()'

    return valid_image.search(url) is not None  # True if the search is not empty.


def login(auth_file):
    """ Reads our auth_file and returns an instance of a PRAW Reddit object. """

    reddit = praw.Reddit(client_id=auth_file.client_id,
                         client_secret=auth_file.client_secret,
                         user_agent=auth_file.useragent)

    return reddit


def set_search_mode(reddit, subreddit_name, mode, limit):

    subreddit_dictionary = {
        "hot": reddit.subreddit(subreddit_name).hot(limit=limit),
        "new": reddit.subreddit(subreddit_name).new(limit=limit),
        "rising": reddit.subreddit(subreddit_name).rising(limit=limit),
        "top-all": reddit.subreddit(subreddit_name).top('all', limit=limit),
        "top-year": reddit.subreddit(subreddit_name).top('year', limit=limit),
        "top-month": reddit.subreddit(subreddit_name).top('month', limit=limit),
        "top-week": reddit.subreddit(subreddit_name).top('week', limit=limit),
        "top-day": reddit.subreddit(subreddit_name).top('day', limit=limit),
        "top-hour": reddit.subreddit(subreddit_name).top('hour', limit=limit)
    }

    return subreddit_dictionary[mode]


def argument_parser():
    """ Adds a few command line arguments to improve usability. """

    parser = argparse.ArgumentParser(description="Downloads images from 'hot' section of the specified subreddit")
    # Valid choices for sort method.

    sort_choices = ['hot',
                    'rising',
                    'new',
                    'top-all',
                    'top-year',
                    'top-month',
                    'top_week',
                    'top-day',
                    'top-hour']

    # Choose subreddit, non optional
    parser.add_argument('subreddit',
                        help='The subreddit you want to download images from.',
                        type=str.lower)

    # Sort method
    parser.add_argument("sort",
                        help='The sort method you want to use when getting posts from a subreddit. Default: hot',
                        choices=sort_choices,
                        type=str,
                        default='hot')

    # Limit how many images to download.
    parser.add_argument('-limit',
                        help='The max. number of posts you want to check for images. Default: 50',
                        type=int,
                        default=50)

    # Whether or not to loop. Default False.
    parser.add_argument('-repeat',
                        help='Use this flag to continue downloading new images until you close the script.',
                        action='store_true')

    # Time between loops.
    parser.add_argument('-wait',
                        help='If repeat flag is on this is how long the script waits (in seconds)'
                             'before repeating. Default: 60',
                        default=60,
                        type=int)

    # Include NSFW results.
    parser.add_argument('-nsfw',
                        help='Use this flag to include NSFW results. Without this flag all posts marked'
                             'NSFW are NOT downloaded.',
                        action='store_true')

    return parser.parse_args()


if __name__ == "__main__":
    exit(main())
