# Introduction
This package is a library of classes dealing with structural analysis of a continuous beam. Stiffness matrix method is used for the analysis. The package acts as a back-end for computing shear forces, bending moments, and deformations occurring in the members of the continuous beam. The data about the geometry of the continuous beam and the loads acting on it, is to be supplied to this package by the importing front-end program.

## Sub-packages and Classes
The 'continuousbeam_backend' package comprises two sub-packages. These sub-packages and the importable classes belonging to them are as follows.
- **beam_classes**
    - **Beam**: this class encapsulates the attributes and behaviour of a member of a continuous beam. It is assumed that the object member is prismatic, has same cross-section, modulus of elasticity, and moment of inertia over its length. 
    - **ContinuousBeam**: this class models a continuous beam and thus keeps track of the individual *Beam* class members, joints and support conditions, as well as loads on them.
- **base_classes**
    - **PointLoad**: the attributes of this class are the magnitude of a point load and its position relative to the left end of the beam member upon which it is acting. 
    - **UdLoadFull**: this class represents a load that is uniformly distributed over the full length of a member beam. Its attributes are magnitude of the UDL and the length of the beam member on which it is acting.  

# Installation and usage
```
pip install continuousbeam-backend
```

**Requirements**

```
"numpy>=1.23"
```
> **Note** The requirements will be installed automatically while installing this package.



### Importing the module
Any of the following formats of importing can be used.
```
from beam_classes import Beam, ContinuousBeam
from base_classes import PointLoad, UdLoadFull
#or 
from beam_classes.beam import Beam 
from beam_classes.continuousbeam import ContinuousBeam
from base_classes.loading import PointLoad, UdLoadFull
```

