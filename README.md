
<a href="http://g.recordit.co/C4QK9yBmsq.gif"><img src="http://g.recordit.co/C4QK9yBmsq.gif"></a>

<h1 align="center">TIM  (The Image Machine)</h1>

<div align="center">
    A configurable <code>Python 3</code> script for bulk downloading images from Reddit.
</div>

<br/>

<div align="center">
  <a href="http://badges.mit-license.org">
    <img src="http://img.shields.io/:license-mit-blue.svg?style=flat-square)"
      alt="MIT Licence" />
  </a>
</div>

## Table of Contents
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Examples](#examples)
- [Support](#support)



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

### Parameters

| Parameter     | Description |
| ------------- | -------------| 
| `subreddit` | The subreddit you want to download images from. *Required.*| 
| `sort`      | Method of sorting when getting subreddit posts. *Required.*   |  
| |*Methods:* `hot` `new` `rising` `top-all` `top-year` `top-month` `top-week` `top-day` `top-hour`| 
| `-limit [#]`    | Maximum number of posts to process. Default `50` *Optional.*|
| `-repeat`   | Use this flag to continuously grab images, waiting `wait_time` between checks. *Optional.*| 
| `-wait [#]`     | The time in seconds to wait before repeating if `-repeat` is used. Default: `60` *Optional*. |
| `-nsfw`     | Use this flag to include posts marked **NSFW**. *Optional.* |

<br/>

---

## Examples

### Example: `/r/pics`
```
the-image-machine.py pics hot -repeat -wait 30
```
- Downloads a maximum of 50 (default) images from `/r/pics/` `hot posts`. 
- Does **not** include posts marked **NSFW**. 
- **Does** repeat. 
- Waits **30 seconds** between checks.

<br/>

### Example: `/r/aww`
```
the-image-machine.py aww top-month -limit 35
```
- Downloads a maximum of 35 images from `/r/aww/` `top posts for month`. 
- Does **not** include posts marked **NSFW**. 
- Does **not** repeat.

<br/>

### Example: `/r/wallpapers`
```
the-image-machine.py wallpapers new -limit 10 -repeat -wait 120 -nsfw
```
- Downloads a maximum of 10 images from `/r/wallpapers/` `new`. 
- **Does** include posts marked **NSFW**. 
- **Does** repeat.
- Waits **60 seconds** (default) between checks.

<br/>

### Example: `/r/nsfw`
```
the-image-machine.py nsfw top-all -limit 50 -nsfw
```
- Downloads a maximum of 20 images from `/r/nsfw/` `top posts for year`. 
- **Includes** posts marked **NSFW**. 
- Does **not** repeat.

<br/>

---

## Support

Reach out to me at one of the following places!

- Reddit at <a href="https://www.reddit.com/user/AntiHydrogen" target="_blank">`/u/AntiHydrogen`</a>
- Github at <a href="https://github.com/disabledtech" target="_blank">`disabledtech`</a>

<br/>

---

## License

MIT License

Copyright (c) 2019 disabledtech

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


