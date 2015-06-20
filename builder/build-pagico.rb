#!/usr/bin/env ruby

require 'optparse'
require 'fileutils'

if ARGV.length < 6
    p 'Please Enter -m mode -v version -r revision'
    exit(1)
end

OptionParser.new do |o|
  $arch = `uname -i`.strip
  o.on('-m MODE') { |mode| $mode = mode }
  o.on('-v VERSION') { |version| $version = version }
  o.on('-r REVISION') { |revision| $revision = revision }
  o.on('-h') { puts o; exit }
  o.parse!
end

source_path = File.expand_path("~/Downloads/Pagico_#{$mode}_r#{$revision}.zip")
if (File.exist?(source_path))
    puts "The file is ready"
else
    puts "#{source_path} can not found"
    exit
end

source_root = File.expand_path("~/Sources")
project_root = File.expand_path("~/Sources/pagico")
de_path = File.expand_path("~/Sources/pagico/CodeX")
httpd_path = File.expand_path("~/Sources/pagico/httpd")


if File.exist? (de_path)
    FileUtils::rm_rf(de_path)
    puts "The file is already there, delete it at first"
end

if !File.exist? (File.expand_path("~/Sources/pagico/debian/#{$arch}"))
    puts "Error, no such '#{$arch}' arch"
    exit
end

system("cd #{project_root} && cp -r debian/#{$arch}/PHP #{httpd_path}")
system("cd #{project_root} && cp -r debian/#{$arch}/ioncube_loader_lin_5.3.so #{httpd_path}")
system("cd #{project_root} && cp -r debian/#{$arch}/abyssws #{httpd_path}")

system("unzip #{source_path} -d #{project_root}")

system("cd #{project_root} && git checkout debian/changelog")
system("cd #{project_root} && dch -v #{$version}-1~r#{$revision} 'New Upstream Version'")

system("cd #{project_root} && debuild")
name = `cd #{source_root} && ls pagico_*~r#{$revision}*.deb`.strip
new_name = "#{name.split('.deb')[0]}_#{$mode}.deb"
puts("cd #{source_root} && mv #{name} ~/Desktop/#{new_name}")
system("cd #{source_root} && mv #{name} ~/Desktop/#{new_name}")
