Python Email Crawler
====================

This python script search/google certain keywords, crawls the webpages from the results, and return all emails found.

Requirements
------------

- sqlalchemy
- urllib2

If you don't have, simply `sudo pip install sqlalchemy`. 


Usage
-------

Start the search with a keyword. We use "iphone developers" as an example.

	python email_crawler.py "iphone developers"

The search and crawling process will take quite a while, as it retrieve up to 500 search results (from Google), and crawl up to 2 level deep. It should crawl around 10,000 webpages :)

After the process finished, run this command to get the list of emails

	python email_crawler.py --emails

The emails will be saved in ./data/emails.csv