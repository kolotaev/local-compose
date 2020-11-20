require 'socket'

$stdout.sync = true

server = TCPServer.new 9020
puts "started on 9020"

while session = server.accept
  request = session.gets
  puts request + "proc 2"

  session.print "HTTP/1.1 200\r\n" # 1
  session.print "Content-Type: text/html\r\n" # 2
  session.print "\r\n" # 3
  session.print "Hello world! The time is #{Time.now}" #4

  session.close
end
