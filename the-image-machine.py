import praw
import logging
import configparser
import os
import re
import requests
import time

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')


def main():

    subreddit = 'memes'  # Which subreddit to download from.
    sleep_time = 30  # How long to wait between searches.
    auth_file = 'reddit-auth.ini'  # Bot auth info
    limit = 20  # Limit how many new posts to get.

    loop = True

    while True:
        if loop:
            grab_image_links(subreddit_name=subreddit,
                             auth_file=auth_file,
                             limit=limit)
            print('Images grabbed. Sleeping for {} seconds.'.format(sleep_time))
            time.sleep(sleep_time)
        else:
            print('Images grabbed. Exiting.')
            break


def grab_image_links(subreddit_name, auth_file, limit):
    """ Checks for new images and downloads them to a folder named after the subreddit """

    image_subdir = 'subreddit-images'  # Where we will store our subreddit folders

    reddit = login(auth_file)  # Log into reddit.
    subreddit = reddit.subreddit(subreddit_name)  # Choose a subreddit.

    try:

        # Try to make a subdir under image_subdir named after the subreddit
        os.makedirs(os.path.join(image_subdir, subreddit_name))

    except FileExistsError:
        # Already exists
        pass

    image_regex = re.compile(r"(http.+?)(\w+)(\.\w+)+(?!.*(\w+)(\.jpg|\.png)+)")

    for item in subreddit.new(limit=limit):
        image_url = item.url

        # Used to check if the URL matches one for an image and get a file extension
        regex = image_regex.search(image_url)

        if is_image(image_url) and not check_if_exists(regex.group(2), regex.group(3), image_subdir, subreddit_name):

            # Download the image.
            logging.debug("Downloading image: %s" % image_url)
            res = requests.get(image_url, headers={'User-agent': 'script by AntiHydrogen 0.1'})
            res.raise_for_status()

            # Characters which are not alphanumeric that we still want to keep.
            keep_these_char = (' ', '.', '_')

            # Create the file name. Uses the meme post title, keeps all alphanumeric
            # characters and those specified in 'keep_these_char'. Appends the file extension.
            file_extension = regex.group(3)
            file_name = regex.group(2)

            save_name = "".join(c for c in item.title if c.isalnum() or c in keep_these_char).rstrip() \
                        + " - {}{}".format(file_name, file_extension)

            # Attempt to protect ourselves from an absurdly long title.
            if len(save_name) > 160:
                save_name = save_name[:60] + '...' + save_name[-60:]

            logging.debug('Saving as: %s' % save_name)

            image_file = open(os.path.join(image_subdir, subreddit_name, os.path.basename(save_name)), 'wb')

            for chunk in res.iter_content(100000):
                image_file.write(chunk)

            image_file.close()


def check_if_exists(file_name, file_extension, image_subdir, subreddit_name):
    """ Check if file exists in the subreddit directory by checking the end of the file names against the
    file name in the URL. Returns True if it exists."""

    file_ends_with = file_name + file_extension

    for file in os.listdir(os.path.join(image_subdir, subreddit_name)):
        if file.endswith(file_ends_with):
            return True  # Found

    return False  # No match found


def is_image(url):
    """ Check url against as regex which determines if it is a valid image URL. Returns true
    if regex search does not return None"""

    valid_image = re.compile(r'''(https?://(?:i\.redd\.it|i\.imgur\.com).*\.(?:png|jpg))''')

    assert valid_image.search('https://i.imgur.com/QpOvnoL.jpg') is not None, \
        'Error. i.imgur.com links ARE NOT validating in is_image()'

    assert valid_image.search('https://i.redd.it/luce08zttse21.jpg') is not None, \
        'Error. i.redd.it links ARE NOT validating in is_image()'

    assert valid_image.search('https://www.youtube.com/watch?v=dQw4w9WgXcQ') is None, \
        'Error. Non-image links ARE validating in is_image()'

    return valid_image.search(url) is not None


def login(auth_file):
    """ Creates and returns a praw Reddit object. """

    config = configparser.ConfigParser()

    try:

        config.read(auth_file)

    except configparser.Error:

        logging.debug("Error reading {}".format(auth_file))

    reddit = praw.Reddit(client_id=config['REDDIT-APP']['client-id'],
                         client_secret=config['REDDIT-APP']['client-secret'],
                         password=config['USER']['password'],
                         user_agent=config['REDDIT-APP']['useragent'],
                         username=config['USER']['username'])

    return reddit


if __name__ == "__main__":
    exit(main())
