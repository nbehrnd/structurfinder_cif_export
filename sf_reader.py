# name:    sf_reader.py
# author:  nbehrnd@yahoo.com
# license: MIT, 2020
# date:    2020-05-07 (YYYY-MM-DD)
# edit:    2020-05-11 (YYYY-MM-DD)
#
""" Collect a selection of information of Structurefinder's database.

    The re-creation of a minimal .cif file for each of the entries may
    offer a bridge between the .cif managed by Daniel Kratzert's Python
    application of Structurefinder toward Thomas Sander's DataWarrior.

    This script expects a call from the CLI of Python 3 with the name
    of the .sqlite file to work with as parameter:

    python sf_reader.py example.sqlite

    Other permitted parameters are -h to access the help menue, and
    -v to access the version information.  Module sqlite3, which is
    called here, is part of the standard library of Python, so 'already
    present' by default. """

import sqlite3
import sys

# Safety guard, limiting the execution to Python 3.
if sys.version_info > (3, 0):
    pass
else:
    print("\nThe script's proper execution requires Python 3.")
    print("Without change of any data, the script closes now.\n")
    sys.exit()

# Instead of using argparse:
INPUT_FILE = ""
if len(sys.argv) >= 2:
    if str(sys.argv[1]) == str("-h"):
        print("""
This is sf_reader.py, a script to extract a minimal .cif per model entry
from the .sqlite database written by Structurefinder (Kratzert and
Krossing, J. Appl. Cryst. 2019, 52, 468-471).

Deposit this Python 3 script in the same folder as the closed (i.e., not
concurrently accessed) .sqlite file to work with.  Retrieved data will be
written into individual .cif files named according to the names initially
used in the .cif files by the command of

python sf_reader.py example.sqlite

where example.sqlite is the database of interest.  This reader uses only
modules already included in standard installations of Python 3.  At any
time, the program may be shutdown by Ctrl + C.\n""")
        sys.exit(0)

    elif str(sys.argv[1]) == str("-v"):
        print("\nScript sf_reader.py, version 0.0.7.\n")
        sys.exit(0)

    elif sys.argv[1] is not None:
        INPUT_FILE = sys.argv[1]
        print("Database file:", INPUT_FILE)

        CONN = sqlite3.connect(INPUT_FILE)
        C = CONN.cursor()

else:
    print("""
Error: either parameter missing, or incorrect.  Run
    python test_read.py -h
for guidance.\n""")
    sys.exit(0)


def count_models():
    """ Count the number of model entries (.cif) in the .sqlite file. """
    C.execute('SELECT ID FROM STRUCTURE')
    data = C.fetchall()

    number_of_models = len(data)
    print(number_of_models, "model data to consider.\n")
    return number_of_models


def model_name_b(model_id):
    """ Determine the name of the structure entries in the set with ID. """
    global model_name
    model_name = ""
#    C.execute('SELECT DATANAME FROM STRUCTURE WHERE ID={}'.format(model_id))
    C.execute('SELECT FILENAME FROM STRUCTURE WHERE ID={}'.format(model_id))
    data = C.fetchone()

    model_name = str(data)[3:-3]
    print("Work on: ", model_name)

    # keep track of the information retrieved from the sqlite database
    global restore_register
    restore_register = []
#    cif_model_entry = ''.join(['data_', model_name])
    cif_model_entry = ''.join(['data_', model_name[:-4]])
    restore_register.append(cif_model_entry)


def model_unit_cell_dimensions(model_id):
    """ Retrieve lengths a, b, c and angles alpha, beta, gamma of the cell """
    C.execute('SELECT * FROM CELL WHERE ID={}'.format(model_id))
    data = C.fetchall()

    length_a = ''.join(['_cell_length_a ', str(data).split(", ")[2]])
    length_b = ''.join(['_cell_length_b ', str(data).split(", ")[3]])
    length_c = ''.join(['_cell_length_c ', str(data).split(", ")[4]])

    angle_alpha = ''.join(['_cell_angle_alpha ', str(data).split(", ")[5]])
    angle_beta = ''.join(['_cell_angle_beta ', str(data).split(", ")[6]])
    angle_gamma = ''.join(['_cell_angle_gamma ', str(data).split(", ")[7]])

    # print("a, b, c: ", length_a, length_b, length_c)
    # print("alpha, beta, gamma: ", angle_alpha, angle_beta, angle_gamma)

    restore_register.append(length_a)
    restore_register.append(length_b)
    restore_register.append(length_c)

    restore_register.append(angle_alpha)
    restore_register.append(angle_beta)
    restore_register.append(angle_gamma)


def model_spacegroup(model_id):
    """ Readout the Herman-Maguin space-group """
    spacegroup = ""
    C.execute('SELECT * FROM RESIDUALS WHERE ID={}'.format(model_id))
    data = C.fetchall()

    spacegroup = str(data).strip().split(', ')[3]
    cif_spacegroup = ''.join(['_symmetry_space_group_name_H-M  ', spacegroup])
    restore_register.append(cif_spacegroup)


def model_symmetry_operations(model_id):
    """ Retrieve the symmetry operations """
    symmetry_operations = []
    C.execute('SELECT * FROM RESIDUALS WHERE ID={}'.format(model_id))
    data = C.fetchall()

    # heading marker in the .cif file about the following loop:
    restore_register.append("\nloop_")
    restore_register.append("_symmetry_equiv_pos_site_id")
    restore_register.append("_symmetry_equiv_pos_as_xyz")

    # isolation of the entry in the sqlite database:
    operators = str(str(data).strip().split(', ')[8])[1:-1]

    # separation of the symmetry operations in this retrieved string:
    symmetry_operations = operators.split('\\n')

    j = 1
    for operation in symmetry_operations:
        retain = str("{} {}".format(j, operation))
        restore_register.append(retain)
        j += 1


def model_atom_coordinates(model_id):
    """ Retrieve atom label, atom type and atom coordinates _per model_ """
    # Note a change a different db-definition of the model ID.
    C.execute('SELECT * FROM ATOMS WHERE STRUCTUREID={}'.format(model_id))
    data = C.fetchall()

    # heading marker in the .cif file about the following loop:
    restore_register.append("\nloop_")
    restore_register.append("_atom_site_label")
    restore_register.append("_atom_site_type_symbol")
    restore_register.append("_atom_site_fract_x")
    restore_register.append("_atom_site_fract_y")
    restore_register.append("_atom_site_fract_z")

    for line in data:
        atom_label = str(str(line).strip().split(', ')[2])[1:-1]
        atom_type = str(str(line).strip().split(', ')[3])[1:-1]

        atom_x = str(line).strip().split(', ')[4]
        atom_y = str(line).strip().split(', ')[5]
        atom_z = str(line).strip().split(', ')[6]

        atom_line = ' '.join([atom_label, atom_type, atom_x, atom_y, atom_z])
        # print(atom_line)
        restore_register.append(atom_line)


def restore_model():
    """ Write a minimal .cif file about the retrieved information. """
#    file_name = ''.join([model_name, '.cif'])
    file_name = ''.join([model_name])
    with open(file_name, mode="w") as newfile:
        for entry in restore_register:
            newfile.write("{}\n".format(entry))


def main():
    """ Joining the functions. """
    for model_id in range(1, count_models() + 1):
        model_name_b(model_id)
        model_unit_cell_dimensions(model_id)
        model_spacegroup(model_id)
        model_symmetry_operations(model_id)
        model_atom_coordinates(model_id)

        restore_model()

    # close pointer and database file:
    C.close()
    CONN.close()


main()
