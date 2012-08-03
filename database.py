from sqlalchemy import create_engine, Table, Column, Integer, String, Boolean, MetaData, select
import urlparse

DATABASE_NAME = 'data/crawler.sqlite'
HTML_DIR = 'data/html/'

class CrawlerDb:

	def __init__(self):
		self.connected = False

	def connect(self):

		self.engine = create_engine('sqlite:///' + DATABASE_NAME)
		self.connection = self.engine.connect()
		self.connected = True if self.connection else False
		self.metadata = MetaData()

		# Define the tables
		self.website_table = Table('website', self.metadata,
			Column('id', Integer, primary_key=True),
			Column('url', String, nullable=False),
			Column('has_crawled', Boolean, default=False),
			Column('emails', String, nullable=True),
		)

		# Create the tables
		self.metadata.create_all(self.engine)
		
	def enqueue(self, url, emails = None):
		if not self.connected:
			return False

		s = select([self.website_table]).where(self.website_table.c.url == url)
		res = self.connection.execute(s)
		result = res.fetchall()
		res.close()
		# If we get a result, then this url is not unique
		if len(result) > 0:
# 			print 'Duplicated: %s' % url
			return False

		args = [{'url':unicode(url)}]
		if (emails != None):
			args = [{'url':unicode(url), 'has_crawled':True, 'emails':unicode(",".join(emails))}]
		result = self.connection.execute(self.website_table.insert(), args)
		if result:
			return True
		return False
		
		
	def dequeue(self):
		if not self.connected:
			return False
		# Get the first thing in the queue
		s = select([self.website_table]).limit(1).where(self.website_table.c.has_crawled == False)
		res = self.connection.execute(s)
		result = res.fetchall()
		res.close()
		# If we get a result
		if len(result) > 0:
			# Remove from the queue ?
			# delres = self.connection.execute(self.queue_table.delete().where(self.queue_table.c.id == result[0][0]))
			# if not delres:
			# 	return False
			# Return the row
			# print result[0].url
			return result[0]
		return False
		
		
	def crawled(self, website, new_emails=None):
		if not self.connected:
			return False
		stmt = self.website_table.update() \
			.where(self.website_table.c.id==website.id) \
			.values(has_crawled=True, emails=new_emails)
		self.connection.execute(stmt)


	def get_all_emails(self):
		if not self.connected:
			return None

		s = select([self.website_table])
		res = self.connection.execute(s)
		results = res.fetchall()
		res.close()
		email_set = set()
		for result in results:
			if (result.emails == None):
				continue
			for email in result.emails.split(','):
				email_set.add(email)

		return email_set

	def get_all_domains(self):
		if not self.connected:
			return None

		s = select([self.website_table])
		res = self.connection.execute(s)
		results = res.fetchall()
		res.close()
		domain_set = set()
		for result in results:
			if (result.url == None):
				continue
			url = urlparse.urlparse(result.url)
			hostname = url.hostname.split(".")
			# Simplistic assumeption of a domain. If 2nd last name is <4 char, then it has 3 parts eg. just2us.com.sg
			hostname = ".".join(len(hostname[-2]) < 4 and hostname[-3:] or hostname[-2:])
			domain_set.add(hostname)

		return domain_set


	def close(self):
		self.connection.close()
		

	def save_html(filename, html):
		filename = os.path.join(HTML_DIR, filename)
		file = open(filename,"w+")
		file.writelines(html)
		file.close()


	def test(self):
		c = CrawlerDb()
		c.connect()
		# c.enqueue(['a12222', '11'])
		# c.enqueue(['dddaaaaaa2', '22'])
		c.enqueue('111')
		c.enqueue('222')
		website = c.dequeue()
		c.crawled(website)
		website = c.dequeue()
		c.crawled(website, "a,b")
		print '---'
		c.dequeue()
	
	
# CrawlerDb().test()

