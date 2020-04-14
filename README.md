
# Museum project
This project is requested for *Advanced Topics in Computer Science course* in **Roma Tre University**.
This web app enables to see how people moved inside a museum during their visit.

## Prerequisites
- [Vagrant](https://www.vagrantup.com/downloads.html) (stable version for this project is **2.2.4**)
- [Oracle VirtualBox](https://www.virtualbox.org/wiki/Downloads) (stable version for this project is **6.0.8**)

## What to do after git clone
1. Open a terminal in the repository main folder.
2. Move inside **environment** directory.
3. `vagrant up`.
4. Wait for Virtual Machine to configure (this may take a few minutes).
5. If everything is ok, you can see a message that says *museum node configuration complete* when process terminates.

### How to run the server?
1. `vagrant ssh`.
2. `sh django_museum/start-museum-app.sh`.

If everything is ok, now you whould see Django server logs in follow mode.

### I started the server, how can i interact with it?
Open your browser, and type localhost:8080

## And if i want to do anything else?
This project runs Vagrant to build and provision a VirtualBox virtual machine.
The automated process installs and configures following features in the firtual machine:
- You can interact with virtual machine using `vagrant ssh`.
- You can shut down virtual machine by typing `vagrant halt` .
- You can remove this virtual machine by typing `vagrant destroy` .
- You can check your virtual machine status by typing `vagrant status` .
- Any other action can be checked typing `vagrant help`  or, to have a more detailed explaination, browsing [vagrant documentation](https://www.vagrantup.com/docs/).

## Technological details
This project automatically install some software inside the virtual machine. This software is required for project execution, and is listed as follow:
- Python 3.6.9
- Django framework 3.0.5
- MySQL