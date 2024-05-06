Name: Xiaokun Du
NetID: xd239

Challenges Attempted (Tier I/II/III): none
Working Endpoint: <GET /api/courses/>
Your Docker Hub Repository Link: https://hub.docker.com/repository/docker/xkund/pa5/general

Questions:
Explain the concept of containerization in your own words.

Containerization involves packaging software code, along with all its dependencies, into standardized units called containers. These containers ensure that the software runs consistently across different environments by virtualizing the operating system instead of the hardware. This makes containers lightweight and portable, allowing multiple containers to share the same OS kernel.



What is the difference between a Docker image and a Docker container?

A Docker image is a static blueprint of a software application, containing all the necessary components such as code, runtime, libraries, and environment variables to run it. A Docker container, on the other hand, is a runtime instance of an image. When you execute an image, it becomes a container. 

What is the command to list all Docker images?

docker image ls

What is the command to list all Docker containers?

docker container ls

What is a Docker tag and what is it used for?

A Docker tag is a label applied to Docker images that specify different versions or configurations of the same base image. Tags are used to easily identify and pull specific versions of images from a repository. We might tag different versions of our application to manage development, testing, and production versions separately.

What is Docker Hub and what is it used for?

Docker Hub is a cloud-based repository service where Docker users and organizations can share Docker images. It works similarly to GitHub but for Docker images. We can push our local images to Docker Hub to make them accessible to others, or pull images published by others to our local environment. 

What is Docker compose used for?

Docker Compose is a tool used to define and run multi-container Docker applications. With Compose, we can use a YAML file to configure our application’s services and with a single command, we can create and start all the services defined in our configuration. It simplifies the management of applications that consist of several interconnected containers.


What is the difference between the RUN and CMD commands?

The RUN command is used in a Dockerfile to execute commands that form the image. RUN is used for installing software, modifying settings,  performing build tasks during the image creation. CMD is used to specify a command that should be run when the container starts. If we don’t specify a CMD, Docker will use the default command from the image. If we start the container with an alternative command, it overrides the CMD specified in the Dockerfile.






