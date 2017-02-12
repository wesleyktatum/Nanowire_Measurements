## Big Picture Design  (Nick)
- Feed in data file (SEM, TEM, SPM, etc.)
- Use edge detection and depth detection algorithms to determine height and width of objects in micrographs (e.g. nanowires, nanoparticles)
- Ideally, this software can read any image and determine the width and height of any "picture" of any object, given appropriate scale
- ???
- Profit

## Use Cases  
- Measure height of nanowires (Yatong)
 - Use Case Name: Height Measurement of Nanowires
 - Actor: user, the program we are about to build
 - Description: The user will upload the data from Atomic Force Microscope of nanowires into the program. The program will then identify the intensity difference, screen out the special situation in which there is, for example, an overlap of nanowires, a random bent of nanowires or a lift by nods that causes the height to rise, and at last return the accurate average height of nanowires inside the scan size. 

- Measure the width of the nanowires (Arushi) . 

## About the Data (Wes)
- The dataset is generated experimentally through AFM imaging by the group
  - One training set will be used for nanowire/edge identification, as well as "node" and defect exclusion
  - One training set will be used for measurement training (minimum width/height, exclude AFM tip influences)
  - Testing and verification datasets can be generated as well
- Pixels contain x, y, and z data, where z is really just intensity
  - The z data can be a number of things, like: Phase, height, conductivity, IR activity at a given $\lambda$
- Raw data needs to be leveled (background) and treated for line scars
- The data files are *SHAPE and SIZE*
