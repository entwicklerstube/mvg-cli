require 'rubygems'
require 'mechanize'
require 'colorize'

@station_url = ARGV[0]

class Ride
   def initialize(line, destination, minutes)
      @line=line
      @destination=destination
      @minutes=minutes
   end

   def display_info
    puts @line + ' - in ' + @minutes + ' minutes - to ' + @destination.red
  end
end

def getRides
    agent = Mechanize.new
    agent.get('http://www.mvg-live.de/ims/dfiStaticAuswahl.svc') do |page|

      form = page.forms.first
      form['haltestelle'] = @station_url
      result = form.submit

      ubahn_ary = []
      sbahn_ary = []
      bus_ary = []

      res_table = result.search('table.departureTable')

      res_table.search('tr').each do |entry|
        
        line = entry.search('.lineColumn').text
        station = entry.search('.stationColumn').text.gsub(/\r?\n?\t/, '')
        minutes = entry.search('.inMinColumn').text

        if line != '' && station != '' && minutes != ''
            if line[0] == 'U'
                single_ride = Ride.new(line, station, minutes)
                ubahn_ary.push(single_ride)
            elsif line[0] == 'S'
                single_ride = Ride.new(line, station, minutes)
                sbahn_ary.push(single_ride)
            else
                single_ride = Ride.new(line, station, minutes)
                bus_ary.push(single_ride)
            end
        end
      end

      puts 'U-Bahn'
      if(ubahn_ary.length == 0)
        puts "Keine Einträge gefunden".red
      else
        ubahn_ary.each do |entry|
            puts entry.display_info
        end
      end
      puts '----------------------------------'
      puts 'S-Bahn'
      if(ubahn_ary.length == 0)
        puts "Keine Einträge gefunden".red
      else
        sbahn_ary.each do |entry|
            puts entry.display_info
        end
      end
      puts '----------------------------------'
      puts 'Bus'
      if(ubahn_ary.length == 0)
        puts "Keine Einträge gefunden".red
      else
        bus_ary.each do |entry|
            puts entry.display_info
        end
      end
    end
end

while true do
    getRides
    sleep 10
end

