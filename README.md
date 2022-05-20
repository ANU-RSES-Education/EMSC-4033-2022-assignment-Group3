# EMSC-4033-2022-assignment - Group 3
Assignment for EMSC-4033/8033, Semester 1, 2022 

 **Group Members:**    
 
  Emma  
  Lucas  
  Anastasia  
  Lachlan
  
  ---
    

**Welcome to our Git repository!** 

The purpose of this Git repository is to provide notebook tutorials to easily create maps from structured data using functions, as well as to write code to test these functions. By following one of these tutorials, you will learn (1) how to use the popular map-making Python package cartopy and (2) how to write and modify simple functions and tests for functions. 

To get started, you will first need to copy, or "fork" the repository, which will allow you to freely experiment and modify the notebooks without affecting the original code.

Next, to make one of the maps, start on the main page and open one of the user folders (e.g. Lucas). Within this folder, you will find some important files:  

- **MapMaker.ipnyb**: Running this module will generate a seismic event map for the California region.

- **src folder**: This folder contains the source code for MapMaker.ipnyb. The functions that are called in **MapMaker.ipnyb** are contained within **my_functions.py**; the dependencies that are needed to be imported for **MapMaker.ipnyb** to run are contained within **dependencies.py** and the functions that are to be tested are contained within **functions.py**.

- **tests folder**: This folder contains tests for each of the functions within **"test_functions.py"**. 

- **RunTests.ipynb**: This module runs the tests contained within **"test_functions.py"**. 

In each mapper, you are able to specify the temporal and spatial scales of interest, the type and resolution of physical features displayed (e.g. lakes, oceans, rivers), the minimum magnitude of the seismic events displayed and the geographic projection of the map. Instructions on how to modify this map are contained within the documentation for **my_functions.py**. Each map displays the earthquakes in a colour-graded system that shows depth, as well a sea-floor layer that displays age.

Have fun! :)


