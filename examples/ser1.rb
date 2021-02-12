
require 'webrick'

$stdout.sync = true

class Echo < WEBrick::HTTPServlet::AbstractServlet
  def do_GET(request, response)
    puts request
    response.status = 200
    response.body = "From GET: Hello world! The time is #{Time.now}"
  end
  def do_POST(request, response)
    puts request
    response.status = 200
    response.body = "From POST: Hello world! The time is #{Time.now}"
  end
end

server = WEBrick::HTTPServer.new(:Port => 9010)
server.mount "/", Echo
trap "INT" do server.shutdown end
# puts 'started on 9010'
server.start
