#!/bin/bash

DJANGO_VERSION=3.0.5

function djangoPrerequisitesInstallation {
	echo "=============================================================================="
	echo "INSTALLING PIP" 
	echo "=============================================================================="
	export DEBIAN_FRONTEND=noninteractive # to avoid provisioning break
	apt install -y python3-pip
}

function djangoInstall {
	echo "=============================================================================="
	echo "INSTALLING DJANGO" 
	echo "=============================================================================="
	pip3 install Django==$DJANGO_VERSION
}

djangoPrerequisitesInstallation
djangoInstall