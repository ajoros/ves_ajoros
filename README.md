# VES
Water4 Project

# Requirements to run
### NOTE: Please install Anaconda Python 3.5 from https://www.continuum.io/downloads
#### Create seperate environment
conda create -n pyqt5_win64 python=3.5
#### Install pyqt5 from anaconda repo cloud (works for osx, linux, win64)
conda install -c mmcauliffe pyqt5=5.5.1 
#### Install all required packages for ves
conda install -f backports cycler decorator get_terminal_size jpeg libpng libtiff matplotlib mkl numpy pandas patsy pyparsing python-dateutil pytz scipy setuptools six statsmodels tk zlibi

#### How to run program
After installing all previous requirements just type execute main.py in /ves folder:
python main.py