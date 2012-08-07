.. Python Email Crawler documentation master file, created by
   sphinx-quickstart on Fri Aug  3 12:26:56 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Python Email Crawler's documentation!
================================================

This python script search certain keywords on Google, crawls the webpages from the results, and return all emails found.

For each result from Google, the crawler will crawl that page for an email. If it could not find an email, it will crawl the linked pages (up to 2nd level). 

This is useful when the result returns the hompage of a website, and the email is usually in the Contact Us page.

------------
Requirements
------------

* sqlalchemy
* urllib2


------
Usage
------
Start the search with a keyword. We use "iphone developers" as an example.

.. code-block:: bash

	$ ./email_crawler.py "iphone developers"

The search and crawling process will take quite a while, as it retrieve up to 500 search results (from Google), and crawl up to 2 level deep. It shold crawl around 10,000 webpages :)

After the process finished, run this command to get the list of emails

.. code-block:: bash

	$ ./email_crawler.py --emails

The emails will be saved in ./data/emails.csv


Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

