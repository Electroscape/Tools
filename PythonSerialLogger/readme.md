pip3 install -r requirements.txt

// to set the sound on analogue not HDMI
sudo amixer cset numid=3 1

// feature on RPis for this repo, may need to be installed again
sudo -H pip install paramiko --ignore-installed

// disable BT to have Serial working, just why you HAVE to do this dont ask me
dtoverlay=pi3-disable-bt

// since regular serial module may be working on pc on rpis its bitching
sudo pip uninstall serial 
sudo pip3 install pyserial

