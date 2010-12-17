#!/usr/bin/python

import urllib2
from vsmtispider import log

class Vsmti:
	def __init__(self, address):
		self.address = address
		pass
		
	def fetch_site(self):
		try:
			connection = urllib2.urlopen(self.address)
			raw_page = connection.read()
			uraw_page = unicode(raw_page, 'windows-1250')
			log.write('Size: ' + str(len(uraw_page) / 1024) + '.' + str(len(uraw_page) % 1024) + ' kB')
		except Exception, e:
			log.write(str(e))
		return uraw_page
		
	def split_sections(self):
		raw_page = self.fetch_site()
		section = raw_page.split('Obavijesti')[1]
		sections = section.split('<span class="article_seperator">')
		return sections
		
	def get_each(self):
		return self.get_stories(self.split_sections())
		
	def get_stories(self, sections):
		stories = []
		for section in sections:
			if not 'contentpaneopen' in section:
				pass
			else:
				for item in section.split('\t\t\t\t\t'):
					if not '\t' in item:
						if not '&nbsp;</span>\n' in item:
							if not '<td align="left" colspan="2">' in item:
								predmet = item.rstrip('\n').rstrip('\n')
							
					if '<td valign="top" colspan="2">' in item:
						for tem in item.split('<td valign="top" colspan="2">'):
							if '<p>' in tem:
								if '<div align="right">' in tem:
									poruka, has_link, link = self.get_message(tem, '<div align="right">')
								
								else:
									poruka, has_link, link = self.get_message(tem, '<p align="right">')

				storybuffer = [predmet, poruka, has_link, link]
				stories.append(storybuffer)
		return stories
		
	def get_message(self, tem, string):
		#'<div align="right">'
		#'<p align="right">'
		raw_poruka = tem.split(string)[0]
		poruka = self.replace_chars(raw_poruka)
		if '<a href="' in poruka:
			has_link = 1
			start = poruka.find('"')
			end = poruka[start + 1:].find('"')
			link = poruka[start + 1:start+end + 1]
			if not 'http' in link:
				link = 'http://www.vsmti.hr' + link
			for item in range(poruka.count('<a href')):
				poruka = self.clean_up_message(poruka)
		else:
			has_link = 0
			link = ''
		return poruka, has_link, link
			
	def clean_up_message(self, message):
		start = message.find('<')
		part1 = message[:start]
		end = message.find('>')
		part2 = message[end + 1:].replace('</a>', '', 1)
		return part1 + part2
		
	def replace_chars(self, message):
		toreplace = ['<p>', '</p>', '&quot;', '\t', '\r', '</table>', '</td>', '</tr>', '</div>', '<strong>', '</strong>', '<u>', '</u>', '<br />', '<p align="justify">', '<span>', '</span>', '&nbsp;']
		for item in toreplace:
			message = message.replace(item, '')		
		return message.replace('\n', ' ')