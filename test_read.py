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


def model_names_b(ID):
    """ Determine the name of the structure entries in the set with ID. """
    global model_name
    model_name = ""
    c.execute('SELECT DATANAME FROM STRUCTURE WHERE ID={}'.format(ID))
    data = c.fetchone()
    model_name = str(data)[3:-3]
    cif_model_entry = ''.join(['data_', model_name])
    print(cif_model_entry)

    # keep track of the information retrieved from the sqlite database
    global restore_register
    restore_register = []
    restore_register.append(cif_model_entry)

def model_unit_cell_dimensions_b(ID):
    """ Retrieve lengths a, b, c and angles alpha, beta, gamma of the cell """

    c.execute('SELECT * FROM CELL WHERE ID={}'.format(ID))
    data = c.fetchall()
    for line in data:
        length_a = ''.join(['_cell_length_a ', str(line).split(", ")[2]])
        length_b = ''.join(['_cell_length_b ', str(line).split(", ")[3]])
        length_c = ''.join(['_cell_length_c ', str(line).split(", ")[4]])

        angle_alpha = ''.join(['_cell_angle_alpha ', str(line).split(", ")[5]])
        angle_beta = ''.join(['_cell_angle_beta ', str(line).split(", ")[6]])
        angle_gamma = ''.join(['_cell_angle_gamma ', str(line).split(", ")[7]])

        print("a, b, c: ", length_a, length_b, length_c)
        print("alpha, beta, gamma: ", angle_alpha, angle_beta, angle_gamma)

        restore_register.append(length_a)
        restore_register.append(length_b)
        restore_register.append(length_c)

        restore_register.append(angle_alpha)
        restore_register.append(angle_beta)
        restore_register.append(angle_gamma)


def model_spacegroup_b(ID):
    """ Readout the Hermann-Maguin spacegroup """

    spacegroup_HM = ""
    c.execute('SELECT * FROM RESIDUALS WHERE ID={}'.format(ID))
    data = c.fetchall()
    for line in data:
        spacegroup_HM = str(line).strip().split(', ')[3]
        cif_HM = ''.join(['_symmetry_space_group_name_H-M   ', spacegroup_HM])
        restore_register.append(cif_HM)
        restore_register.append(" ")


def model_symmetry_operations_b(ID):
    """ Retrieve the symmetry operations """

    symmetry_operations = []
    c.execute('SELECT * FROM RESIDUALS WHERE ID={}'.format(ID))
    data = c.fetchall()

    # heading marker in the .cif file about the following loop:
    restore_register.append("loop_")
    restore_register.append("_symmetry_equiv_pos_site_id")
    restore_register.append("_symmetry_equiv_pos_as_xyz")

    for line in data:
        # isolation of the entry in the sqlite database:
        operators = str(str(line).strip().split(', ')[8])[1:-1]

        # separation of the symmetry operations in this retrieved string:
        symmetry_operations = operators.split('\\n')
#        print("symmetry_operations: ", symmetry_operations)
        j = 1
        for operation in symmetry_operations:
            print("{} {}".format(j, operation))
            restore_register.append("{} {}".format(j, operation))
            j += 1


def model_atom_coordinates_b(ID):
    """ Retrieve atom label, atom type and atom coordinates _per model_ """

    # Note a change a different db-definition of the model ID.
    c.execute('SELECT * FROM ATOMS WHERE STRUCTUREID={}'.format(ID))
    data = c.fetchall()

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
        print(atom_line)
        restore_register.append(atom_line)

def restored_model(ID):
    """ Write a minimal .cif file about the retrieved information. """
    file_name = ''.join([model_name, '.cif'])
    with open(file_name, mode="w") as newfile:
        for entry in restore_register:
            newfile.write("{}\n".format(entry))


# action calls:
model_number()  # identify the number of models to consider
for ID in range(1, model_number + 1):
    model_names_b(ID)
    model_unit_cell_dimensions_b(ID)
    model_spacegroup_b(ID)
    model_symmetry_operations_b(ID)
    model_atom_coordinates_b(ID)
    restored_model(ID)

# close pointer and database file:
c.close()
conn.close()
