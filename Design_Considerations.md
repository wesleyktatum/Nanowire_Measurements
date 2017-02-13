## Big Picture Design  (Nick)
- Project Name: Micrograph Visual Analysis for Nanometer-Scale Characterization
- Software that reads in a micrograph, likely from a scanning probe microscopy, and determines physical characteristics of the material being scanned
- This will be most intuitive on AFM-type data, but we plan to find a way to generalize it to electron microscopy as well (where depth tends not to be well defined)
- Software will be useful to scientists who have little working knowledge of python but need to quickly interpret the results of their experiments, especially if they are looking for materials with certain shapes and sizes
- Visual analysis like this applies to all kinds of work in nanotechnology and should be useful for optimizing any material that requires nanoscale precision (e.g. plasmonic metamaterials, quantum computing, organic or inorganic PV devices, etc.)

## Use Cases  
###1. Measure height of nanowires (Yatong)
 - Use Case Name: Height Measurement of Nanowires
 - Actor: user, the program we are about to build
 - Description: The user will upload the .txt file or .png image data of scanned nanowires from Atomic Force Microscope into the program. The program will then identify the intensity difference, transform it into height information, screen out the special situation in which there is, for example, an overlap of nanowires, a random bent of nanowires or a lift by nodes that causes the unusual rise in height, and at last return the individual and total average height of nanowires inside the scan size. 

###2. Measure the width of the nanowires (Arushi) . 
- **Name**: Girth Detector
- **Desription**: For a given AFM input data (.txt file with height data or .png image), the code can identify the outlines of the nanowires and identify the cross-sectional width of the nanowire. After collecting this data from input, it can generate a histogram of wire widths.  
- **Actors** - A user without knowledge of python should be able to use it, preferably with command line inputs where the user can specify filenames, and other conditions. 
- **Precondition** - It assumes that all samples in the AFM image are nanowires and all other structures are absent. For the simplest case, the code will ignore errors that arise from a tilted samples, over exposure, et cetera.  

## About the Data (Wes)
- The dataset is generated experimentally through AFM imaging by the group
  - One training set will be used for nanowire/edge identification, as well as "node" and defect exclusion
  - One training set will be used for measurement training (minimum width/height, exclude AFM tip influences)
  - Testing and verification datasets can be generated as well
- Pixels contain x, y, and z data, where z is really just intensity
  - The z data can be a number of things, like: Phase, height, conductivity, IR activity at a given $\lambda$
- Raw data needs to be leveled (background) and treated for line scars
- The data files are *SHAPE and SIZE*
