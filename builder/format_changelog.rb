#!/usr/bin/env ruby

text = %q{
#983939	Workspace Edge Settings stops working on reboot		Medium	Ding Zhou 	Confirmed
#992616	Take back the original window buttons arrangement		Low	Ding Zhou 	Won't Fix
#995748	Natural Scrolling takes no effect in some places		High	Ding Zhou 	Confirmed
#998184	Integration with Ubuntu's System Settings app		Medium	Ding Zhou 	Fix Committed
#998411	Invalid values for resetting fonts		High	Ding Zhou 	Fix Committed
#998594	Ubuntu Tweak reported a negative number of bytes for removing old kernels		Low	Ding Zhou 	Fix Committed
#998626	Pressed the file manager, an error message appears		Low	Ding Zhou 	Fix Committed
#998742	crash while searching for old kernels to clean		Medium	Ding Zhou 	Fix Committed
#999072	ubuntu tweack "miscellaneous" crash		Low	Ding Zhou 	Fix Committed
#1000682	Recently Used should not display the items doesn't work for current desktop		Low	Ding Zhou 	Fix Committed
#1001551	Janitor tab is empty		Medium	Ding Zhou 	Fix Committed
#1001779	Crash while trying to add a custom command in File Type Manager		High	Ding Zhou 	Fix Committed
#1002026	Click on Sessing module generates "this module encountered an error while loading"		Low	Ding Zhou 	Fix Committed
#1002594	Houve erro ao carregar o modulo.		Low	Ding Zhou 	Fix Committed
#1004172	NameError in utils.walk_directories		Medium	Ding Zhou 	Fix Committed
#1005485	Font settings are not displayed in gnome-fallback session		Low	Ding Zhou 	Fix Committed
#1007859	launching desktop icond from within ubuntu tweak		Low	Ding Zhou 	Fix Committed
}

text_list = ["<ul>"]

text.split("\n").each do |line|
    if line != ''
        puts "Start to process line: #{line}"
        new_line = "<li>#{line.split("\t")[0..3].insert(0, 'LP:').join(' ')}</li>"

        text_list.push(new_line.sub(/#\d+/) { |match|
            "<a href='https://launchpad.net/bugs/#{match[1..-1]}'>#{match}</a>"
        })
    end
end

text_list.push("</ul>")

puts text_list.join("\n")
