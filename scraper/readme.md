# Includes all scripts 

My main criterion while creating a joke dataset was to have jokes that have good rating. There were lot of jokes available online, that didn't make much sense in my opinion and I felt that, if you feed in garbage, you get garbage out. So, I scraped those jokes, which had more than 50% rating or which had atleast +2 score(upvotes - downvotes) in the case of reddit. Here is the list of websites from where I scraped. 

![Alt text](joke_sources.png "Joke_Sources")

For scraping from Reddit (www.reddit.com/r/jokes), I used the PRAW (The Python Reddit API Wrapper) library. In agreement, with the terms and conditions and not to stuff with too many requests to the Reddit website, I wait 2 seconds for every joke request. For all other websites shown in the image above, I used the powerful scrapy library. 

Feel free to modify the codes according to your needs and run the scripts provided.

To scrape jokes subreddit, you need to have PRAW installed and use the file scrape_reddit.py to get jokes from reddit.

To scrape from other websites mentioned above, you need to have scrapy installed, and try the following commands for scraping jokes from respective websites. You are free to change the scrap_jokes/spiders/unijokes_spider.py to scrap all the jokes or limit the jokes with high ratings or votes. 

`scrapy crawl jokes` for https://unijokes.com 

`scrapy crawl laughfactory` for www.laughfactory.com

`scrapy crawl onelinefun` for www.onelinefun.com

`scrapy crawl ajokeaday` for https://www.ajokeaday.com

`scrapy crawl kickasshumor` for www.kickasshumor.com

`scrapy crawl funny2` for http://funny2.com

`scrapy crawl jokesoftheday` for www.jokesoftheday.net

Jester Jokes, I downloaded about 150 jokes from http://goldberg.berkeley.edu/jester-data/

I would also like to thank Abhinav Moudgil (https://github.com/amoudgl/funnybot) for some of the jokes. 

If someone reading this page has some nice source of good jokes, please write to me so that I can add codes for scraping the available data.
