#!/usr/bin/python

s = """
 	#982632	Window module fails to load on Xubuntu, Lubuntu	   	High	Ding Zhou 	Fix Committed
 	#988564	ubuntu-tweak 0.7.0 (oneiric/unity-2d) crashes in Unity settings	   	High	Ding Zhou 	Fix Committed
 	#990270	Ubuntu Tweak crash after install in Ubuntu 12.04 system76 laptop	   	High	Ding Zhou 	Fix Committed
 	#992581	nautilus script-worker fails on 12.04	   	High	Ding Zhou 	Fix Committed
 	#994376	Add composite, workspace and dash color options to Unity 2D	   	High	Ding Zhou 	Fix Committed
 	#995333	QuickLists should support locale	   	High	Ding Zhou 	Fix Committed
 	#995748	Natural Scrolling takes no effect in some places	   	High	Ding Zhou 	Fix Committed
 	#987573	Old kernel janitor in infinite loop	   	Medium	Ding Zhou 	Fix Committed
 	#988554	ubuntu tweak login settings crashes	   	Medium	Ding Zhou 	Fix Committed
 	#988659	If gedit is not installed, Ubuntu Tweak will crash	 	Medium	Ding Zhou 	Fix Committed
 	#993334	Update Dialog API in Source Center	 	Medium	Ding Zhou 	Fix Committed
 	#994980	The search icon is missing in Ubuntu 12.04 default theme	   	Medium	Ding Zhou 	Fix Committed
 	#995135	Quicklists editor crashed when no desktop file	   	Medium	Ding Zhou 	Fix Committed
 	#996324	Add Ubuntu Overlay Scrollbars tweak	   	Low	Ding Zhou 	Fix Committed
 	#997513	Add Settings for "Show Desktop Icon in launcher"
    """

l = []
for line in s.split("\n"):
    if line.strip():
        new_line = line.split("\t")[:3]
        new_line[0] = "    - LP:"
        l.append(" ".join(new_line))

print "\n".join(l)
