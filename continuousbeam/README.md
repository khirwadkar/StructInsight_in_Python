# Introduction
This package acts as a Graphical User Interface (GUI) for another package with name *continuousbeam-backend*. Through the graphical interface of this package, the user inputs the data about the geometry of a continuous beam and the loads acting upon it. The *backend* package then performs the structural analysis of the given beam under the given loading and makes it available to our *frontend* package in numeric format. Our frontend package converts this numeric information to graphical format and displays various structural engineering diagrams, such as Reaction diagram, Shear Force diagram, Bending Moment diagram, and Deflection diagram.  


## Modules in the Package
There are four modules in the *continuousbeam* package. They are as described below.
- **contibeam_main**: This is the starting point of the program. It produces a GUI menu, through which the user can invoke the remaining three modules. 
- **beam_data**: This module collects the data about the geometry of the continuous beam from the user. The data includes such things as number of beam members, length, modulus of elasticity, moment of inertia of each beam member, and the type of each joint in the continuous beam.
- **load_data**: The user inputs the data about the loads acting on the continuous beam through this module. The types of loads accepted by this module are: joint loads (point loads and moments), and member loads (uniformly distributed loads and point loads). In this version of the package, only vertical point loads are considered; also the uniformly distributed loads that cover the full length of a member are allowed.
- **analysis**: This module takes the numeric results of analysis from the *backend* package. Then using those results, it produces and displays various diagrams needed by a structural engineer. It also stores the numeric data in a file with name '*structinsight_results.txt*'. The file is saved in the current directory, that is, the directory from where the program was invoked. 


# Installation and usage
Issue the following command to install the package on your system.
```
pip install continuousbeam
```

**Requirements**

```
"continuousbeam-backend >= 2023.11"
```
> **Notes** 
> - 1. The above requirements will be installed automatically while installing this package.
> - 2. Besides these, the package requires Python >= 3.8 and tkinter >= 8.6. (tkinter is the graphics library which is in-built in the Windows version of Python. On Linux and Mac platforms, some distributions of Python do not include it. In such cases, it will have to be installed separately.) 



### Using the package
This package can be executed directly from the command prompt by issuing the command in any of the following formats.
```
 $ python -m continuousbeam.contibeam_main

# or

 $ contibeam
```

The package can be imported also. It is expected that it would be imported by a larger GUI program which deals with different types of structures, such as trusses, frames, etc. The suitable format of import under these circumstances would be as follows. 
```
from continuousbeam import contibeam_main
```

After importing the 'contibeam_main' module, the importing program can display the GUI menu of the continuous beam by a statement as shown below.
```
contibeam_main.ContiBeamMenuWindow(parent_window_reference) 
```
The '*parent_window_reference*' in the above statement would be some tkinter window handle in the importing program.



