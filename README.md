
<a href="http://g.recordit.co/C4QK9yBmsq.gif"><img src="http://g.recordit.co/C4QK9yBmsq.gif"></a>

<!-- (https://avatars1.githubusercontent.com/u/4284691?v=3&s=200)](http://fvcproductions.com) -->

# The Image Machine (TIM)

> A configurable Python 3 script for bulk downloading images from Reddit.
> README IS VERY W.I.P.

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

---

## Prerequisites

<br/>

<a href="https://praw.readthedocs.io/en/latest/" target="_blank">PRAW</a> is used to interact with the reddit API.
```
pip install praw
```

---
## Usage

<br/>
 
```
the-image-machine.py [subreddit] [sort_method] [-optional_parameters]
```

#### Parameters
| Parameter     | Description |
| ------------- | -------------| 
| `subreddit` | The subreddit you want to download images from. *Required.*| 
| `sort`      | Method of sorting when getting subreddit posts. *Required.*   |  
| |*Sort methods:* `hot` `new` `rising` `top-all` `top-year` `top-month` `top-week` `top-day` `top-hour`| 
| `-limit`    | Maximum number of posts to process. Default `50` *Optional.*|
| `-repeat`   | Use this flag to continuously grab images, waiting `wait_time` between checks.| 
| `-wait`     | The time in seconds to wait before repeating if `-repeat` is used. Default: `60` *Optional*. |
| `-nsfw`     | Use this flag to include posts marked **NSFW**. *Optional.* |
|

## Examples

<br/>

####Example: `/r/pics`
```
the-image-machine.py pics hot -repeat -wait 30
```
- Downloads a maximum of 50 (default) images from `/r/pics/` `hot posts`. 
- Does **not** include posts marked **NSFW**. 
- **Does** repeat. 
- Waits **30 seconds** between checks.

<br/>

####Example: `/r/aww`
```
the-image-machine.py aww top-month -limit 35
```
- Downloads a maximum of 35 images from `/r/aww/` `top posts for month`. 
- Does **not** include posts marked **NSFW**. 
- Does **not** repeat.

<br/>

####Example: `/r/wallpapers`
```
the-image-machine.py wallpapers new -limit 10 -repeat -wait 120 -nsfw
```
- Downloads a maximum of 10 images from `/r/wallpapers/` `new`. 
- **Does** include posts marked **NSFW**. 
- **Does** repeat.
- Waits **60 seconds** (default) between checks.

<br/>

####Example: `/r/nsfw`
```
the-image-machine.py nsfw top-all -limit 50 -nsfw
```
- Downloads a maximum of 20 images from `/r/nsfw/` `top posts for year`. 
- **Includes** posts marked **NSFW**. 
- Does **not** repeat.


---
## Support

Reach out to me at one of the following places!

- Reddit at <a href="https://www.reddit.com/user/AntiHydrogen" target="_blank">`/u/AntiHydrogen`</a>
- Github at <a href="https://github.com/disabledtech" target="_blank">`disabledtech`</a>

---

## License

- **[MIT license](http://opensource.org/licenses/mit-license.php)**

---