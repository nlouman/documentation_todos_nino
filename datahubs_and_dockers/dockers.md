# Docker Updates and Additions
This file contains things concerning the rebuilding of dockers, adding new ones, etc.
Highest priority is first. Priority is also roughly categorized as [HIGH], [MEDIUM], [LOW].

## [HIGH] GoPro Docker 
For the collaboration between Lilian Calvet and Robin Bruneau, we need a docker for the GoPro camera. This project has been started in this repo ```https://github.com/nlouman/ros2_gopro_driver```, but is still very incomplete. By the end of October, a basic docker that can stream images needs to work.
## [MEDIUM][from Vincent] New ZED SDK 
Test [new zed sdk](https://www.stereolabs.com/en-ch/developers/release).
- Can depth and rgb image be generated reliably at 30 Hz with 1080P? 
- There's already a docker with the new sdk which runs on the jetson (see deploy_zed_sdk_50.sh).
- Try running the zed camera on the datahub (don’t forget sudo jetson_clocks + use NEURAL_LIGHT depth mode) and to watch the frame rate (ros2 topic hz) from the workstation or dgx. Compare with the older sdk performance. You can also check the CPU and GPU usage with the jetson power gui.
## [MEDIUM][from Vincent] ROS2 QoS
Test ROS2 quality of service “reliable” setting.
- Add QoS setting to the config of device dockers and rosbag recording node.
- Check with validation workflow if the frame rate drops disappear in “reliable” mode.
## [MEDIUM][from Vincent] HDMI throttling
- Add throttling and resizing to HDMI input node. (Gianluca will look into this)  
- The frame resolution and rate are defined by the sender. Sometimes, we don’t need full resolution or frame rate though.  
- Throttling needs to be done on GPU before compression because you can’t downsample H264 image streams without losing important information.  
- Note (Nino): There is almost no documentation on the HDMI docker and, more importantly, on the compression (encoder/decoder) dockers Vincent was working on. Add some if you work on this.
## [MEDIUM][from Vincent] Compression
- Change image compression to lossless h264 or h265 compression   
- We currently use lossy compression which does not allow for complete reconstruction. However, lossy H264 leads to a higher compression ratio. 
## [MEDIUM] Update Sprytrack Docker
The Sprytrack docker should be updated and extended. See the Sprytrack branch of the atracsys github repo. Currently, it does not publish any markers, only RGB images. 
- For this, take inspiration from the fusionTrack driver. 
- Also, performance as well as usability should be improved. For the fusionTrack it is already completely optimized. Check if the Sprytrack also supports some timesyncing protocol like the fusionTrack does.
## [LOW] Port Dockers to Azure 
Port dockers to Azure container. We would like to store dockers on location at Balgrist directly instead of via the docker hub. This requires us to easily access the DGX - and be able to pull dockers from the DGX on-location at the OR-X. Together with Fréd, there have been some talks with Nicholas Büngert on this topic and he will (probably) eventually get back to us about this. Nothing we can do on our side for now.