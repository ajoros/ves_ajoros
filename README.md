# VES
Water4 Project
# Requirements to run
### NOTE: Please install Anaconda Python 3.5 from https://www.continuum.io/downloads
#### Create seperate environment
conda create -n pyqt5_env python=3.5

source activate pyqt5_env (do this on osx/linux)

OR

activate pyqt5_env (do this on win64)
#### Install pyqt5 from anaconda repo cloud (works for osx, linux, win64)
conda install -c mmcauliffe pyqt5=5.5.1 
#### Install all required packages for ves
conda install -f backports cycler decorator get_terminal_size jpeg libpng libtiff matplotlib mkl numpy pandas patsy pyparsing python-dateutil pytz scipy setuptools six statsmodels tk zlib
conda install reportlab

#### How to run program
After installing all previous requirements just execute main.py in /ves folder:
python main.py

#### NOTES FOR USING PYINSTALLER
MAKE SURE SETUPTOOLS IS VERSION 19.2 BEFORE USING PYINSTALLER
Make sure setuptools is version 19.2 before using PyInstaller

#### If you get "AttributeError: 'FrozenImporter' object has no attribute '_files'",
then try:

Decided to go look at where exactly the AttributeError was being thrown from so I inspected the reportlab/rl_config.py and reportlab/lib/utils.py files and found that it was checking objects recursively looking for directories (as insinuated by rl_isdir). Some how the FrozenImporter got stuck being checked with a list of other objects
so I replaced the line:
return len(list(filter(lambda x,pn=pn: x.startswith(pn),list(__loader__._files.keys()))))>0
with:

try:
    return len(list(filter(lambda x,pn=pn: x.startswith(pn),list(__loader__._files.keys()))))>0
except AttributeError:
    return False

#### IF YOU GET MKL_AVX AND MKL_DEF ERROR, try this:
I think I solved the problem. My NumPy 'site.cfg' file simply had the line "mkl_libs = mkl_rt", but when I explicitly added mkl_avx and mkl_def and recompiled, it worked fine. I guess there was some issue in libmkl_rt.so. I only have the 64-bit MKL installed, so that's not an issue.