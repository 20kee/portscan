import socket

url = 'ec2-13-209-65-115.ap-northeast-2.compute.amazonaws.com'
ip = socket.gethostbyname(url)
print(ip)