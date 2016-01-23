import os
import subprocess

from PyQt4 import QtGui


def showMessageAlertBox(parent, title, message):
    error_message = QtGui.QMessageBox(parent)
    error_message.setWindowTitle(title)
    error_message.setText(message)
    error_message.exec_()


def transform_ui_files_into_py():
    print "[+] Transforming ui files into py"
    from edat import get_edat_directory
    edat_dir = get_edat_directory()
    transformer_script = os.path.abspath(os.path.join(edat_dir, 'utils', 'ui', 'transformer.py'))
    design_path = os.path.abspath(os.path.join(edat_dir, 'ui', 'design'))

    for file in os.listdir(design_path):
        if file.endswith('.ui'):
            print "\t-{0}".format(file)
            file_output_name = file.replace('.ui', '.py')
            input_file = os.path.abspath(os.path.join(design_path, file))
            output_file = os.path.abspath(os.path.join(edat_dir, 'ui', file_output_name))
            subprocess.call(['python', transformer_script, input_file, '-o', output_file])

    print "[+] Finished transforming."