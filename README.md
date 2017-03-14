# NaRWHAL: Nanowire Recognition, Width and Height Analytical Library

NaRWHAL is a software for the identification and measuring of nanowires in AFM micrographs. From a raw .txt file data of AFM, the software helps users eliminate background noise, detect nanowires and measure the width of desired nanowires in the frame of a graphical user interface (GUI). 


### Software Dependencies
python version 3
python packages: opencv, scikit-image, tkinter, photutils, astropy

Mac OS X and Windows are both able to download python without any dependencies. Tkinter package comes with the python but for opencv, scikit-image, photutils and astropy performing pip install in command line is needed. 

### Folders 
- NaRWHAL
  - Data: there are three subfolders with backgrounded, unbackgrounded and raw data collected from AFM in .txt files.
  - Test: this folder contains test functions for backgrounding and nanowire detecting in .py files. 
  - Other files are all codes for this software, including backgrounding, nanowire dectecting and graphical user interface, in .py files. 

- ipynb's
  - This folder contains all of the working code in .ipynb files.

### Running the software
1. To run the software, first git clone the whole repository into your computer. 
2. In a shell script, open the directory "NaRWHAL" and type in:
   python viewlims.py
3. The graphical user interface then opens. On the top left corner, there are options shown as "File", "Nanowire Detection" and "Image Manipulation". 
4. Click on "File", then "Upload" to upload the text file from AFM. After uploading, the image of nanowires will show on the canvas of GUI. Click on the "Zoom in Rectangle" button beside the image to zoom into desired detecting region.  
5. Click on "Image Manipulation", then "Background slope removal" to remove background noise. There is also an option "Colors" under "Image Manipulation" for users to choose different colormaps ("Viridis", "Inferno", "Plasma" or "Magma") they would like the image to display. 
6. Click on "Nanowire Detection", then "Process in opencv Algorithm" to detect the nanowire and measure the width of desired nanowires. 

### Running the tests
