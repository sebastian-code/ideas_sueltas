#!/usr/bin/env ruby

require 'optparse'
require 'fileutils'

debuild_root = File.expand_path('~/Sources/apt/fcitx/fcitx-4.2.4')
source_root = File.expand_path('~/Sources/fcitx')
debuild_parent = File.dirname(debuild_root)

system("mv #{debuild_root}/debian #{debuild_parent}")
system("cp -r #{source_root}/* #{debuild_root}")
system("mv #{debuild_parent}/debian #{debuild_root}")
system("cd #{debuild_root} && debuild")
