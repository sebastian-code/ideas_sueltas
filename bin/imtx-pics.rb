#!/usr/bin/env ruby

print "Please input the prefix: "
prefix = gets.strip

sir.glob('*.jpg').sort.each_with_index do |path, i|
    i = i + 1
    if i < 10
        i = "0#{i}"
    end
    puts "Converting #{path} to #{prefix}-#{i}.jpg..."
    system("convert -quality 100 -resize 550x413 #{path} #{prefix}-#{i}.jpg")
end
