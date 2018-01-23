#!/usr/bin/env bash
PYTHON_VERSION=3.5
OPEN_CV_VERSION=3.3.1
RPI_CAMERA_EFFECTS=/home/pi/projects/sw

sudo apt-get purge wolfram-engine
sudo apt-get purge libreoffice*
sudo apt-get clean
sudo apt-get autoremove
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install build-essential cmake pkg-config
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
sudo apt-get install libgtk2.0-dev libgtk-3-dev
sudo apt-get install libatlas-base-dev gfortran
sudo apt-get install fswebcam
sudo python3 get-pip.py
sudo pip3 install virtualenv virtualenvwrapper
sudo pip3 install numpy
sudo rm -rf ~/.cache/pip
echo -e "\n# virtualenv and virtualenvwrapper" >> ~/.profile
echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.profile
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.profile

source ~/.profile
mkvirtualenv cv -p python3
source ~/.profile
workon cv

cd ~
wget -O opencv.zip https://github.com/Itseez/opencv/archive/$OPEN_CV_VERSION.zip
unzip opencv.zip

wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/$OPEN_CV_VERSION.zip
unzip opencv_contrib.zip

cd ~/opencv-$OPEN_CV_VERSION/
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-$OPEN_CV_VERSION/modules \
    -D BUILD_EXAMPLES=ON ..

sudo make -j4
sudo make install
sudo ldconfig
sudo mv /usr/local/lib/python$PYTHON_VERSION/site-packages/cv2.cpython-35m-arm-linux-gnueabihf.so /usr/local/lib/python$PYTHON_VERSION/site-packages/cv2.so
ln -s /usr/local/lib/python$PYTHON_VERSION/site-packages/cv2.so /usr/local/lib/python$PYTHON_VERSION/site-packages/cv2.soecho @lxterminal --command $RPI_CAMERA_EFFECTS/camera-effects-rpi-sw2017/engine/start.sh >> ~/.config/lxsession/LXDE-pi/autostart

sudo reboot