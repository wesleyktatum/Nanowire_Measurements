# NaRWHAL: Nanowire Recognition, Width and Height Analytical Library #

NaRWHAL is a software for the identification and measuring of nanowires in AFM micrographs. From a raw .txt file data of AFM, the software helps users eliminate background noise, detect nanowires and measure the width and height of desired nanowires in the frame of a graphical user interface (GUI). 


### Software Dependencies: ###
python version 3

python packages: astropy, opencv, photutils, scikit-image, tkinter

Mac OS X and Windows are both able to download python without any dependencies. Tkinter package comes with python, but for opencv, scikit-image, photutils and astropy performing pip install in command line is needed. 

Note: To run the software in version lower than python 3, please change "import tkinter" in .py files to "import Tkinter". 

### Folders: ###
- NaRWHAL
  - Data: there are three subfolders with backgrounded, unbackgrounded and raw data collected from AFM in .txt files.
  - Test: this folder contains test functions for backgrounding and nanowire detecting in .py files. 
  - Other files are code for this software, including backgrounding, nanowire dectecting and graphical user interface, in .py files. 

- ipynb's
  - This folder contains all of the working code in .ipynb files.

### Running the software: ###
1. To run the software, first git clone the whole repository into your computer. 

2. In a shell script, open the directory "NaRWHAL", type in and run:
   python viewlims.py
   
3. The graphical user interface then opens. On the top left corner, there are options shown as "File" and "Image Processing". 

4. Click on "File", then "Upload" to upload the text file from AFM. After uploading, the image of nanowires will show on the canvas of GUI. Click on the "Zoom in Rectangle" button beside the image to zoom into desired detecting region.  

5. Click on "Image Processing", then "Background slope removal" to remove percetible slopes from the background of image. There is also an option "Colors" under "Image Processing" for users to choose different colormaps ("Viridis", "Inferno", "Plasma" or "Magma") they would like the image to display.

6. The backgrounded image will show on a pop-up window. There are also two buttons on the pop-up window. Click "Dismiss Changes" to ignore the backgrounding and quit this window. Click on "Accept Background and Analyze" to calculate height profile and detecting outline of a single nanowire. Two detected images will show on the pop-up window with one showing the line along cross-section of nanowire in desired region and the other showing height profile along the line.

7. Click on "Documentation" under "File" to access the information in this README file. 

8. Click on "Quit" under "File to quit the software. 

### Running the tests: ###
In a shell script, open the directory "NaRWHAL", type in and run: nosetests -m Test.(the name of test .py file desired to run)

### Acknowledgements: ###
We appreciate feedback and suggestions on the structure and coding of this software from Professor David Beck and Professor Jim Pfaendtner, as well as other people in the DIRECT program at University of Washington. 
We would also like to thank Micah Glaz from Molecular Analysis Facility at University of Washington for helping with AFM techniques and Ariel Rokem from eScience Institute at University of Washington for gaving suggestions on image processing of this software.
