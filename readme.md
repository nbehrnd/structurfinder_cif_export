This is a concept study to retrieve a selection of data stored in the
structurefinder .sqlite application by Kratzert and Krossing as .cif.

Structurefinder (https://www.xs3.uni-freiburg.de/research/structurefinder,
https://github.com/dkratzert/StructureFinder) provides the infrastructure
to set up a local database of crystallographic data in .cif files.  It
is desirable to complement structural information with applications like
DataWarrior (http://openmolecules.org/datawarrior/index.html) already
offering access to the Crystallographic Open Database
(http://www.crystallography.net/cod/index.php) with a snapshot (
http://www.openmolecules.org/datawarrior/datafiles.html) with model data
not yet in the public, too 
(https://github.com/dkratzert/StructureFinder/issues/3).

This concept study seeks to retrieve a minimal subset of data from the
.sqlite database structurefinder writes: lattice constants, space group
symmetry, symmetry operators; atom label, atom label and atom coordinates.


