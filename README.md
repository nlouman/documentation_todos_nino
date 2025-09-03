# Documentation & ToDo's Nino
This folder contains a lot of info regarding projects and ToDo's that were ongoing by the time I had to leave. It is for sure not complete, but I hope it gives a good overview and starting point on the next steps. The main repos you will presumably work with are 
- [OR-X Middleware](https://github.com/BAL-ORX/orx_middleware)
- [Isaac ROS Common](https://github.com/BAL-ORX/isaac_ros_common)
- [Atracsys Driver](https://github.com/BAL-ROCS/atracsys_ros)
- [Rocsync](https://github.com/jaromeyer/RocSync)
- [GoPro Driver](https://github.com/nlouman/ros2_gopro_driver)

Ask Fréd for access rights.

I have sorted my points into broad categories below.
There are three things that I would say are on the top of the list:
1. Developing a Docker for the GoPro camera. Robin and Lilian need this by end of October.
2. Improving usability of the pipeline. There are so many small things to here that it's difficult to define a concrete goal. Going through my points [here](orx_interface/TODOS.md) might provide a good start.
- The two points above are very good starting points to get familiar with the codebase.
3. Finish timesyncing. Refer to [here](ptp_timesyncing/ptp_vision.md) to see what's left to do.

## Datahub Usability

### Ease of Use
Even though the whole pipeline is there, it is still has lots of issues that prevent people from using it. A researcher should be able to autonomously use everything without our help, and some features such as deploying an experiment at the OR-X should ideally also be doable by a non-programmer. This requires three things:
- **Very good Documentation:** The documentation for sure is lacking right now. The plan is to create a Wiki on Teams that is easy to follow and links to the different repos, guides and so on which provide more in-depth info if needed. I.e. make two levels, a basic one for people who want to use the existing pipeline, and one more in depth for people who want to change/add some features or need to debug.
- **Intuitive usage:** We already have a GUI and a number of scripts that are supposed to be very easy to run. However, in practice you run into all kinds of issues, and there are a lot of bugs in this, and debugging is a nightmare. So both for the developer's as well as the end user's sake, we need to make the pipeline easier to use, fix bugs, add improved debugging, etc.
- **Plug-and-Go:** In the ideal scenario, you simply plug in your datahubs in the OR, plug in your cameras to the datahubs, configure and then start your recording. Or if you want to be independent of the OR-X, you also need to be able to use a laptop to centrally steer everything. Our approach needs to become more flexible than it is right now.

This point touches upon a lot of things as it spans across the whole pipeline. Refer to these documents for a start; [(1)](orx_interface/TODOS.md), [(2)](datahubs_and_dockers/datahubs.md), [(3)](ptp_timesyncing/overview.md).

### Device Support
In order to get people to use our framework, it needs to support the devices they use - and the support should extend to options that might need to be set. One example; the OR lighting is very strong, so you will likely need to be able to reduce the exposure of the camera. If you cannot do that via a config, people will not use that camera with our framework. And if a camera is not supported, they will of course also not use it. Therefore, we are working on extending our pipeline to support the cameras that the researchers are using in their projects.

Some of the comments in [here](datahubs_and_dockers/dockers.md) are about this.

### Reliability
Mainly Vincent, my predecessor, was working on this. We want reliable image streams at high framerates and resolutions. There are two sub-issues here:
- **Data throughput:** We want to be able to use multiple devices at once on a datahub. Throughput very quickly becomes an issue, resulting in lost frames and errors. That's why Vincent was working on compressing the data before sending it. Some more work on this needs to be done, see 
- **Reliable transmission:** This is a very related issue. Some cameras have framedrops and so on, even when there isn't an issue with throughput.

For both you can see the relevant points in [here](datahubs_and_dockers/dockers.md).

## Timesyncing
- When recording time-sensitive data like video streams on multiple different devices, we need to know exactly when each image was acquired, especially if we're talking about high-framerate acquisitions that need to capture movement. This becomes even more critical when trying to coordinate multiple robots together, for example. The problem is the lack of a unified reference time: All the datahubs need to be synced very closely to each other and/or to a master clock, and (in case of a custom ROS driver implementation) the ROS timestamp that we give to each frame needs to match the actual time the image was recorded at as closely as possible. This problem and a possible solution are discussed in [here](ptp_timesyncing/overview.md).
- Another point I need to mention here is the RocSync, a tool developed by a Zivi together with Lilian Calvet in order to synchronize videos together. In case the synchronization as outlined in the document linked to above works well, it eliminates the need for this tool - however, there remain many situations where you will still need to use it. We have noticed a potential issue with it, see [here](rocsync/1_checking_rocsync_clock.md). We also want to check the accuracy of this tool, which could be done via the approach outlined [here](rocsync/2_checking_rocsync_syncing.md).