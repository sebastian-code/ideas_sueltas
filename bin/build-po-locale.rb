#!/usr/bin/env ruby

Dir.glob("*.po").each do |file|
    system("mv #{file} #{file.split('-')[-1]}")
end
