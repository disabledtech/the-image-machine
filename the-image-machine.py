import praw
import os
import re
import requests
import time
import argparse


def main():

    """TODO VALIDATE SUBREDDIT."""

    args = argument_parser()

    subreddit = args.subreddit  # Which subreddit to download from.
    sleep_time = args.s  # How long to wait between searches (in seconds)
    limit = args.l  # Limit how many new posts to get. Set to None to grab as many as possible.
    loop = args.r  # Continuously grab images, waiting *sleep_time* between loops.

    # See Authentication class for info if you want to modify these values.
    auth_file = Authentication(client_id='zlGNo2QoKclQlQ',
                               useragent='script by /u/AntiHydrogen v0.1')

    while True:

        if loop:

            grab_image_links(subreddit_name=subreddit,
                             auth_file=auth_file,
                             limit=limit)

            print('Sleeping for {} seconds.\n'.format(sleep_time))
            time.sleep(sleep_time)

        else:

            print('Images grabbed. Exiting.')
            break


class Authentication(object):
    """ A class which holds the details needed to start a PRAW reddit object. My implementation works
        with reddit in read-only mode which can grab images from public subreddits so we do not use a
        client_secret, username, or password. I /assume/ you could add in a username, password, and
        client_secret to use private subreddits accessible to your account, however, this is untested
        and may not work (insert ominous music here).

        The necessary details can be found on your 'https://www.reddit.com/prefs/apps/' if you want to
        use your own client_id/secret.

    Attributes:
        client_id       Reddit application client-id
        client_secret   Reddit application client_secret. We do not use a secret in this script because
                        we only need read-only access to public subreddits so we init to None.
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
        save_name   The name this image will be saved as if we call .save()

    """

    def __init__(self, title, url, subreddit, file_extension, file_name):
        self.title = title
        self.url = url
        self.subreddit = subreddit
        self.extension = file_extension
        self.name = file_name
        self.save_name = self.get_save_name()

    def get_save_name(self):
        """ Returns a name to save the file as. """

        # Characters which are not alphanumeric that we still want to keep.
        keep_these_char = (' ', '.', '_')

        save_name = "".join(c for c in self.title if c.isalnum() or c in keep_these_char).rstrip() \
                    + " - {}{}".format(self.name, self.extension)

        # Attempt to protect ourselves from an absurdly long title.
        if len(save_name) > 130:
            # Cut the file name down to the first and last 60 char.
            save_name = save_name[:60] + '...' + save_name[-60:]

        return save_name

    def exists(self):
        """ Check if file exists in the subreddit directory by checking the end of the file names against the
        file name in the URL. Returns True if it exists."""

        if os.path.exists(self.subreddit):
            for file in os.listdir(self.subreddit):
                if file.endswith(self.name + self.extension):
                    return True  # Found
            return False  # No match found
        else:
            return False  # If there's no subreddit directory the file cannot exist.

    def save(self):

        print("Downloading: {}".format(self.save_name))

        res = requests.get(self.url, headers={'User-agent': 'script by /u/AntiHydrogen 0.1'})
        res.raise_for_status()

        image_file = open(os.path.join(self.subreddit, os.path.basename(self.save_name)), 'wb')

        for chunk in res.iter_content(100000):
            image_file.write(chunk)

        image_file.close()


def grab_image_links(subreddit_name, auth_file, limit):
    """ Checks for new images and downloads them to a folder named after the subreddit
        TODO COUNT TIL WE HAVE LIMIT """

    reddit = login(auth_file)  # Log into reddit.
    subreddit = reddit.subreddit(subreddit_name)  # Choose a subreddit.

    try:

        os.mkdir(subreddit_name)

    except FileExistsError:

        pass

    valid_image_regex = re.compile(r"(http.+?)(\w+)(\.\w+)+(?!.*(\w+)(\.jpg|\.png)+)")


    for post in subreddit.hot(limit=limit):

        # Used to check if the URL matches one for an image, get the extension, and file name.
        our_image_regex = valid_image_regex.search(post.url)

        # Init an image object with all the attr. our downloader will need.
        download_this_image = Image(title=post.title,
                                    url=post.url,
                                    subreddit=subreddit_name,
                                    file_name=our_image_regex.group(2),
                                    file_extension=our_image_regex.group(3))
        
        # Check that the URL a valid image and then check that it does not exist already.
        if is_image(download_this_image.url) and not download_this_image.exists():
            download_this_image.save()


def is_image(url):
    """ Check URLs against as regex which determines if it is a valid
    image URL. Valid URLs are from the domain 'i.redd.it' or 'i.imgur.com' and
    end in .jpg or .png."""

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


def argument_parser():
    """ Adds a few command line arguments to improve usability. """
    parser = argparse.ArgumentParser(description="Downloads images from 'hot' section of the specified subreddit")

    # Choose subreddit, non optional
    parser.add_argument('subreddit',
                        help='The subreddit you want to download images from.',
                        type=str,
                        default='aww')  # Default unneeded because this is non-optional?

    # Limit how many images to download.
    parser.add_argument('-l', '-limit',
                        help='The number of images you want to grab. Default: 100',
                        type=int,
                        default=100)

    # Whether or not to loop.
    parser.add_argument('-r', '-repeat',
                        help='Repeat downloading new images until you close the script.',
                        action='store_true')

    # Time between loops.
    parser.add_argument('-s', '-sleep',
                        help='If repeat is True this is how long the script waits (in seconds) '
                             'before repeating. Default: 60',
                        default=60,
                        type=int)

    return parser.parse_args()


if __name__ == "__main__":
    exit(main())
