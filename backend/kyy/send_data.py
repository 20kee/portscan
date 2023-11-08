send_msg = {
    80 : b'GET / HTTP/1.1\r\nHost: example.com\r\n\r\n',     # HTTP 
    443 : b'GET / HTTP/1.1\r\nHost: example.com\r\n\r\n',    # SSL
    21 : b'USER anonymous\r\n',                              # FTP
    25 : b'EHLO example.com\r\n',                            # SMTP
    110 : b'USER test\r\n',                                  # POP3
    143 : b'a1 LOGIN user password\r\n',                     # IMAP
    161 : b'',                                               # SNMP
    389 : b'ldapsearch -x -h example.com -s base "(objectclass=)"',  #LDAP
    1433 : b'',#SQL Server
    1521 : b'(CONNECT_DATA=(COMMAND=version))',#Oracle DB 
    123: b'',#NTP (123)
    5060: b'OPTIONS sip:nouser@example.com SIP/2.0\r\n',#SIP (5060)
    9200 : b'GET /Redis (6379)INFO\r\nMongoDB (27017){ "ismaster": 1 }',#Elasticsearch (9200)
    53: b'', #DNS (53)
    111: b'No specific message; an RPC call is needed to grab a banner.', #RPCbind (111)
    2049: b'No specific message; an NFS call is needed to grab a banner.', #NFS (2049)
    5222: b"<stream:stream to='example.com' xmlns:stream='http://etherx.jabber.org/streams' version='1.0'>",#XMPP (5222)
    6667: b'NICK guest\r\nUSER guest 0 :guest\r\n'#IRC (6667)
}

if __name__ == '__main__':
    print(send_msg[52221])