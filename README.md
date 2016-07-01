# VES - Vertical Electrical Sounding software
### Water4 Project
#### Used for geophysics for groundwater, well siting, well drilling

#### Filesize requirements: ~740mb free space.

## Windows 64-bit Installation Instructions
1. **Download VES zip file** from https://dl.dropboxusercontent.com/u/561373/ves_ajoros.zip to C:/ drive
  * NOTE: If you run into permission (admin priviledge) error during download process just download to C:/Users/<username>. After this, drag and drop (or extract) the .zip file from C:/Users/<username> to C:/
  * *NOTE: If you have any issues, make sure to right-click and run as administrator*
2. **Unzip to C:/ drive.** Once successfully unzipped you should see the main.py in the folder path *C:/ves_ajoros/ves/main.py*
3. **Download Win64 miniconda installer**: https://repo.continuum.io/miniconda/Miniconda3-latest-Windows-x86_64.exe
4. **Right click .exe > Run as Administrator (IMPORTANT STEP)** and follow the instructions on the screen. Simply accept the defaults as they all can be changed later.
5. **Run run_ves_install.bat from C:/ves_ajoros**. This installs the dependencies that run_ves_field.bat uses.
6. After observed data is collected, **double click run_ves_field.bat**.

## Once inside VES software

1. **Insert observed/survey data into table**, and press **"Computer and Plot Resistivities"** to generate graph plot.
2. Press **"Launch VES Inverse Analysis"**
3. **Enter appropriate table data, longitude, latitude, and date/time information**
4. To launch Monte Carlo Simulation press **"Re-Run Using Monte Carlo Simultation"**
  * *NOTE: Please be patient while Monte Carlo simulations runs. Takes ~5-20 seconds. Program may hang but this is normal.*
5. PDF output will then be available at **C:/ves_ajoros/ves/report_pdfs**