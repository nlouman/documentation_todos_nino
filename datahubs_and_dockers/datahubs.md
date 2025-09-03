# Datahub ToDo's
This file contains bugs that concern the software on the datahubs directly. Highest priority is first. Priority is also roughly categorized as [HIGH], [MEDIUM], [LOW].

## [MEDIUM] Forced Update
There is a known issue of the datahub sometimes forcing an update on shutdown, i.e. it tries to install an update on the next boot. This doesn't mix well with the custom kernel that ZHAW developed for the DH, causing an unrecoverable black screen. In cases like these, we needed to reflash the DH, erasing all data on it in the process.

- We think that the bug only happens when shutting down while connected to the internet.
- When shutting down once I noticed that there was an option that was on by default to perform an update on the next reboot on the window telling you "Shutting down in 60s". My guess is that that's exactly what was causing the issue. And hopefully there's a config/settings file somewhere allowing to turn automatic updates off completely... some research into this is needed.

## [MEDIUM] 1st of January 1970 start time
**NOTE: This might already be fixed from when I was working on the timesyncing, but remains to be tested.**

So when the datahub starts and isn't connected to the internet, its date is set to 1st of January 1970. Once chrony finds internet access or another master, this is updated. What we would like, however, is for the time to be roughly correct at startup, irrespective of any connections (ofc the connections would override that time). As there is no hardware clock present on the device itself, that becomes a bit of a challenge. I tried a bit with a package called `fake hardware clock`, but it doesn't seem to work yet. When you change anything here, please make sure it doesn't interfere with the timesyncing from chrony/PTP. This issue can get annoying since we don't really have internet access down in the OR-X, and since browsers, git, etc. won't work if your time is too far off from the actual time.

## [LOW] Browser Issues
There seems to be an issue (both with chromium, firefox) of browsers not being able to start anymore on some DH due to some permissions issues (SELinux).

## [LOW] Transferring large files
When recording ROS bags, they can get very big very fast. Therefore, if you are not using the OR-X-setup of recording everything to one device, you are going to be left with transferring your data off of the DH. Peter had issues with this, possibly related to the power the DH is able to provide to an external SSD (although he also had problems to `scp` such large files). Some checks and possible remedies for this could help save time down the line. 

## [LOW] Mouse Issues
There are issues with peripheral support.
- On the development datahubs, these issues appear only when running a camera plugged into one of the USB-A ports at the same time as trying to move a mouse with a dongle plugged into the other USB-A port. I don't think there's much that can be done about this. The keyboard works fine.
- At least on DH 2, possibly on the other encased DHs as well, we have mouse issues in general, i.e. the mouse is very difficult to move at some points. If it becomes a big problem (if it happens on all datahubs), maybe talk to Gianluca Pargätzi about this.

## [LOW] [from Vincent] Wifi    
- Find a solution to have reliable WiFi internet on datahub from OR-X.   
    - Check with Gianluca.
    - Note (Nino): The DH do not have built-in Wifi.
    - Note 2 (Nino): Wifi+Bluetooth could allow connecting to the GoPro wirelessly. The fusiontrack and sprytrack sensors in theory support this as well.