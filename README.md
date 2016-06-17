# ves
water4 project

# requirements to run
## create seperate environment
conda create -n pyqt5_win64 python=3.5 
## install pyqt5 from anaconda repo cloud (works for osx, linux, win64)
conda install -c mmcauliffe pyqt5=5.5.1 
## install all req'd packages for ves
conda install -f backports cycler decorator get_terminal_size jpeg libpng libtiff matplotlib mkl numpy pandas patsy pyparsing python-dateutil pytz scipy setuptools six statsmodels tk zlibi
