This script, `sf_reader.py`, written for the CLI of Python 3, retrieves
information from the .sqlite data base StructureFinder (by Kratzert and
Krossing) writes.

StructureFinder (https://www.xs3.uni-freiburg.de/research/structurefinder,
https://github.com/dkratzert/StructureFinder) provides the infrastructure
to set up a local database of crystallographic data in .cif files.  It
is desirable to complement structural information with applications like
DataWarrior (http://openmolecules.org/datawarrior/index.html) already
offering access to the Crystallographic Open Database
(http://www.crystallography.net/cod/index.php) with a snapshot (
http://www.openmolecules.org/datawarrior/datafiles.html) with model data
not yet in the public, too 
(https://github.com/dkratzert/StructureFinder/issues/3).

By a call of

`python sf_reader.py example.sqlite`

the script will retrieve a _minimal subset_ of data from the .sqlite data
base StructureFinder writes: lattice constants, space group
symmetry, symmetry operators; atom label, atom label and atom coordinates.

The script does not consider additional crystallographic information
such as site occupancy factors used to describe positional disorder,
or anisotropic displacement parameters.


As a training, the repository contains test data.  File
`three_data.sqlite` is a test data base written by StructureFinder
(version 47) while accessing structure models `ACSALA01.cif`,
`ADRENL.cif`, and `BAPLOT01.cif`; these files are part of CCDC's freely
accessible [teaching subset](https://www.ccdc.cam.ac.uk/Community/educationalresources/teaching-database/),
section [Drug molecules]()https://www.ccdc.cam.ac.uk/structures/search?compound=drug%20molecules), 
and are copied in sub-folder `input`.

Running `python sf_reader.py three_data.sqlite` restores the three
`.cif` files deposit in sub-folder `output`.
