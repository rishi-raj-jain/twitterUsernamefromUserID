[![Pull Requests Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)](http://makeapullrequest.com)
[![first-timers-only Friendly](https://img.shields.io/badge/first--timers--only-friendly-blue.svg)](http://www.firsttimersonly.com/)
[![GitHub license](https://img.shields.io/github/license/haccer/tweep.svg)](https://github.com/haccer/tweep/blob/master/LICENSE)
[![Selenium](https://img.shields.io/badge/-selenium-green)](https://www.selenium.dev/)
[![Python](https://img.shields.io/badge/-python-yellow)](https://www.python.org/)
[![Chrome](https://img.shields.io/badge/-chrome-blue)](https://www.google.com/chrome/)

>No authentication. No API. No limits.

**twitterUsernameviaUserID** is an advanced Twitter scraping tool written in Python and Selenium that allows for scraping tweet usernames from the twitter id's, **without** using Twitter's API.

## tl;dr Benefits
Some of the benefits of using twitterUsernameviaUserID vs Twitter API:
- Can fetch __all__ tweet usernames from their id's (Twitter API limits to last 3200 Tweets only);
- Fast initial setup;
- Can be used anonymously and without Twitter sign up;
- **No rate limitations**.

## Requirements
- Python >= 3.6
- Selenium
- WebDriver Manager

## Installing

**Pip:**
```bash
- pip3 install twitterUsernameviaUserID
- Voila!
```

**Example:**
```
    from twitterUsernameviaUserID import getHandles as gH
    # A dictionary with mapped user ids to their usernames
    temp= gH.getHandles([<list of user ids (in string)>], <delay time between request>)
```
