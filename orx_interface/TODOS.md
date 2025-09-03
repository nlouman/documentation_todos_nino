This is a collection of future plans plus currently known bugs of the OR-X Datahub data acquisition pipeline.

## Quality-of-Life improvements of the usage pipeline
When going to the OR-X and wanting to use the datahubs, there are any number of issues that might be encountered, such as topics not being detected, or being detected but not published, annoying errors when running the code etc. During my usage of the pipeline, I encountered some of them, partially listed below. Some are real errors, some would be nice-to-haves, as they would make either development or usage nicer. I sorted them by ERROR (not runnable if this is still there), NEED (i.e. in order to have a reasonably nice user experience, this needs to be there), WISH (some things that could save a lot of time down the road). The relevant folders in `orx_middleware` are ```experiment_deployment``` and ```orx_interface```. Try to run through the pipeline, and you will encounter most of these issues yourself.

### (1) The GUI
Under ```/home/${USER}/dev/orx/orx_middleware/orx_interface/device_config_gui```, there's the code plus docker build scripts for the streamlit docker. There are a number of bugs that I noticed while using it

- [NEED]: There's options that can be set that invalidate others, and/or lead to errors down the line. For example for the ZED Mini you can set the depth mode in the config, by default it is *NONE* I believe. Therefore it does not publish any depth topic. If you leave it at the default, but select to record the depth topic down the line, this will result in an error. It would be great to grey out certain options if others are set, (plus for the ZED Mini have a different depth mode be the default), so as to not run into these errors.

- [WISH]: Better tooltips actually explaining what the options you set are doing for each camera would be great.

- [NEED]: Actually integrate all the cameras we have into this pipeline and update the configs. I believe the Atracsys FusionTrack 500 one is outdated, the Kinect one is not there yet, same for the Atracsys Sprytrack and the Luxonis OAK-D Pro W (```./deploy_depthai.sh```).

- [WISH]: When you leave one tab of the streamlit app, and go back to it, all the settings are reset to default. This can be very annyoing, we need some kind of cache that keeps the set variables in memory.

- [ERROR]: When you choose to manually specify devices to add instead of using automatic device detection, you get an immediate error. 

### (2) The scripts
- [ERROR]: There's something wrong with the bag data extractor pathing.

- [NEED]: There's also still some issue with the workstation/DGX not seeing the topics of the datahubs, or seeing them but nothing being published. Check the ```cyclone_profile.xml``` for this.

- [WISH]: Improve the device detection to automatically check reachable datahubs and only continue with those / ask which datahubs should be used.

- [WISH]: Passwordless ```03_prepare_devices```.

- [NEED]: There needs to be some way to see whether the cameras were correctly started or not. Right now it could be that you do a recording, get no error, and later see that half the cameras didn't work. To verify cameras working, you can use ```rqt_image_view```, but when they are not working, in order to see any errors/traces, you need to ssh into the datahub and go into the tmux container to see what went wrong. Some way to transmit part of the console output of the tmux session to the "main" terminal would be ideal (or write them to logs somewhere). This integrates back into the config setting - as cameras/our dockers still have issues, a lot of the time they don't work, and it's very time-consuming to debug like this.

- [NOTE]: I noted down some more bugs, but I don't quite remember what they were about;
    - Bug with too many tmux sessions being started?
    - Ideally only close sessions which were previously opened to avoid errors