This readme is only to run the UI part of container migration of busybox application:

Steps to run:
1. Clone or copy this “container_migration” folder into local directory
2. Prerequisites: Docker.io, node and npm software packages installed
3. Open the cloned folder and enter commands in terminal as given below:
a. Npm install
b. Node app.js
4. Go to localhost:3001 where the server is running
5. Click the start button to start container and observe logs in local terminal by command:
a. Docker logs looper2
6. Click migrate button on UI to migrate the container to a different container:
7. If you observe the new logs of looper-clone, you will notice the count has started from where it was left off
a. Docker logs looper-clone
