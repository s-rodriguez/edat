import os
import subprocess
import sys
from optparse import Values

from PyQt4 import QtGui
from PyQt4.uic.driver import Driver

if sys.hexversion >= 0x03000000:
    from PyQt4.uic.port_v3.invoke import invoke
else:
    from PyQt4.uic.port_v2.invoke import invoke


def showMessageAlertBox(parent, title, message):
    error_message = QtGui.QMessageBox(parent)
    error_message.setWindowTitle(title)
    error_message.setText(message)
    error_message.exec_()


def transform_ui_files_into_py():
    print "[+] Transforming ui files into py"
    from edat import get_edat_directory
    edat_dir = get_edat_directory()
    design_path = os.path.abspath(os.path.join(edat_dir, 'ui', 'design'))

    for file in os.listdir(design_path):
        if file.endswith('.ui'):
            print "\t-{0}".format(file)
            file_output_name = file.replace('.ui', '.py')
            input_file = os.path.abspath(os.path.join(design_path, file))
            output_file = os.path.abspath(os.path.join(edat_dir, 'ui', file_output_name))
            transform_ui(input_file, output_file)

    print "[+] Finished transforming."


def transform_ui(input_path_file, output_path_file):

    options = Values({
        'execute': False,
        'from_imports': False,
        'indent': 4,
        'debug': False,
        'output': output_path_file,
        'preview': False,
        'pyqt3_wrapper': False,
        'resource_suffix': '_rc'
    })

    invoke(Driver(options, input_path_file))
