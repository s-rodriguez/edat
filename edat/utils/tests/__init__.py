
def create_full_project():
    import os
    from af.utils.tests.af_test import create_db_and_data_config_associated
    from edat.model.Project import Project

    data_config = create_db_and_data_config_associated()
    path_location = os.path.abspath('.')

    print "Creating Full Project..."
    project = Project('FullProject', path_location)
    project.data_config = data_config

    file_location = project.project_file_location()
    with open(file_location, 'w') as f_output:
        f_output.write(project.project_file_representation(save=True))

    print "Project file created on: %s" % file_location

create_full_project()