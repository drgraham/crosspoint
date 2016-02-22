all: script icon desktop

script:
	mkdir -p $(HOME)/.local/bin
	cp crosspoint.py $(HOME)/.local/bin/crosspoint

icon:
	mkdir -p $(HOME)/.local/share/icons
	wget -nc -P /tmp http://crosspoint.tv/images/main/crosspoint-logo.svg
	convert +antialias -background none -density 105.5 -crop 256x256+430+0 /tmp/crosspoint-logo.svg $(HOME)/.local/share/icons/crosspoint.png

desktop:
	mkdir -p $(HOME)/.local/share/applications
	cp crosspoint.desktop $(HOME)/.local/share/applications/
	printf "Exec=$(HOME)/.local/bin/crosspoint" >> $(HOME)/.local/share/applications/crosspoint.desktop
	printf "Icon=$(HOME)/.local/share/icons/crosspoint.png" >> $(HOME)/.local/share/applications/crosspoint.desktop
	xdg-desktop-menu forceupdate
