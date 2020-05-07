# name:    test_read.py
# author:  nbehrnd@yahoo.com
# license:
# date:    2020-05-07 (YYYY-MM-DD)
# edit:
""" Collect a selection of information of Structurefinder's database.

    The re-creation of a minimal .cif file for each of the entries may
    offer a bridge between the .cif managed by Daniel Kratzert's Python
    application of Structurefinder toward Thomas Sander's DataWarrior.

    This script serves as proof of concept only and expects a call from
    the CLI of Python 3 without provision of parameters.  Module sqlite3
    is part of the standard library of Python, so 'already present' by
    default. """

import sqlite3

conn = sqlite3.connect('two_data.sqlite')
c = conn.cursor()


def model_number():
    """ Determine the number of structure entries in the set. """
    global model_number
    model_number = 0
    c.execute('SELECT ID FROM STRUCTURE')
    data = c.fetchall()
    model_number = len(data)
    print("model_number: ", model_number)


model_number()

# ----  test start:

def model_names_b(ID):
    """ Determine the name of the structure entries in the set with ID. """
    model_name = ""
    c.execute('SELECT DATANAME FROM STRUCTURE WHERE ID={}'.format(ID))
    data = c.fetchall()
    for entry in data:
        model_name = str(entry)[3:-3]
        cif_model_entry = ''.join(['{}: '.format(ID), 'data_', model_name])
        print(cif_model_entry)

#for ID in range(1, model_number + 1):
#    model_names_b(ID)

# ----  test end.

#def model_unit_cell_dimensions():
#    """ Retrieve lengths a, b, c and angles alpha, beta, gamma of the cell """

#    if model_number > 0:
#        for ID in range(1, model_number + 1):

#            c.execute('SELECT * FROM CELL WHERE ID={}'.format(ID))
#            data = c.fetchall()
#            for line in data:
#                length_a = ''.join(['_cell_length_a ', str(line).split(", ")[2]])
#                length_b = ''.join(['_cell_length_b ', str(line).split(", ")[3]])
#                length_c = ''.join(['_cell_length_c ', str(line).split(", ")[4]])

#                angle_alpha = ''.join(['_cell_angle_alpha ', str(line).split(", ")[5]])
#                angle_beta = ''.join(['_cell_angle_beta ', str(line).split(", ")[6]])
#                angle_gamma = ''.join(['_cell_angle_gamma ', str(line).split(", ")[7]])

#                print("ID; a, b, c: ", ID, length_a, length_b, length_c)
#                print("alpha, beta, gamma: ", angle_alpha, angle_beta, angle_gamma)
#model_unit_cell_dimensions()

# ---- test start:

def model_unit_cell_dimensions_b(ID):
    """ Retrieve lengths a, b, c and angles alpha, beta, gamma of the cell """

#    if model_number > 0:
#        for ID in range(1, model_number + 1):

    c.execute('SELECT * FROM CELL WHERE ID={}'.format(ID))
    data = c.fetchall()
    for line in data:
        length_a = ''.join(['_cell_length_a ', str(line).split(", ")[2]])
        length_b = ''.join(['_cell_length_b ', str(line).split(", ")[3]])
        length_c = ''.join(['_cell_length_c ', str(line).split(", ")[4]])

        angle_alpha = ''.join(['_cell_angle_alpha ', str(line).split(", ")[5]])
        angle_beta = ''.join(['_cell_angle_beta ', str(line).split(", ")[6]])
        angle_gamma = ''.join(['_cell_angle_gamma ', str(line).split(", ")[7]])

        print("ID; a, b, c: ", ID, length_a, length_b, length_c)
        print("alpha, beta, gamma: ", angle_alpha, angle_beta, angle_gamma)
# model_unit_cell_dimensions_b()

for ID in range(1, model_number + 1):
    model_names_b(ID)
    model_unit_cell_dimensions_b(ID)

# ---- test end.

def model_spacegroup():
    """ Readout the Hermann-Maguin spacegroup """
    if model_number > 0:
        for ID in range(1, model_number + 1):

            spacegroup_HM = ""
            c.execute('SELECT * FROM RESIDUALS WHERE ID={}'.format(ID))
            data = c.fetchall()
            for line in data:
                spacegroup_HM = str(str(line).strip().split(', ')[3])[1:-1]
                print("ID; spacegroup: ", ID, spacegroup_HM)


# model_spacegroup()


def model_symmetry_operations():
    """ Retrieve the symmetry operations """
    if model_number > 0:
        for ID in range(1, model_number + 1):

            symmetry_operations = []
            c.execute('SELECT * FROM RESIDUALS WHERE ID={}'.format(ID))
            data = c.fetchall()
            for line in data:
                # isolation of the entry in the sqlite database:
                operators = str(str(line).strip().split(', ')[8])[1:-1]
        #         print("operators: ", operators)

                # separation of the symmetry operations in this retrieved string:
                symmetry_operations = operators.split('\\n')
                print("\n len symmetry_operations: ", len(symmetry_operations))
                print("ID, symmetry_operations: ", ID, symmetry_operations)
                j = 1
                for operation in symmetry_operations:
                    print("{} {}".format(j, operation))
                    j += 1


# model_symmetry_operations()


def model_atom_coordinates():
    """ Retrieve atom label, atom type and atom coordinates _per model_ """
    if model_number > 0:
        for ID in range(1, model_number + 1):

            # Note a change a different db-definition of the model ID.
            c.execute('SELECT * FROM ATOMS WHERE STRUCTUREID={}'.format(ID))
            data = c.fetchall()
            for line in data:
                atom_label = str(str(line).strip().split(', ')[2])[1:-1]
                atom_type = str(str(line).strip().split(', ')[3])[1:-1]

                atom_x = str(line).strip().split(', ')[4]
                atom_y = str(line).strip().split(', ')[5]
                atom_z = str(line).strip().split(', ')[6]

                atom_line = ' '.join([atom_label, atom_type, atom_x, atom_y, atom_z])
                print("ID, atom_line: ", ID, atom_line)


# model_atom_coordinates()

# close pointer and database file:
c.close()
conn.close()
