###########################################################################################
# PREREQUISITES
# * A raspberry pi with a camera
#    * I used a pi zero but other versions should work
#    * Install raspbian
#    * Enable the camera and SSH through the raspi-config menu
# * A slack account with a bot token created for our notifications
# * Pi mounted in an overhead position with a view of the sink
# 
# OPTIONAL
# * Update before you begin: https://www.raspberrypi.org/documentation/raspbian/updating.md
###########################################################################################

# Install packages we need through apt
apt -y install python-opencv numpy apache2 python-pip

# Install the slackclient through pip
pip install slackclient

# Create our image output directory for troubleshooting purposes
mkdir /var/www/html/images

# Create a home for our python script and copy it over
mkdir /opt/dishdetector
cp dishdetector.py /opt/dishdetector/

# Create a cronjob for our dishdetector that runs every 10 minutes from 9am to 10pm
crontab -l | { cat; echo "*/10 9-22 * * * SLACK_BOT_TOKEN="replace_with_your_slack_token" python /opt/dishdetector/dishdetector.py"; } | crontab -
