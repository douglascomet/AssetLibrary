import os
import json
import pprint

from maya import cmds

USER_APP_DIR = cmds.internalVar(userAppDir=True)
# print USER_APP_DIR

# DIRECTORY = os.path.join(USER_APP_DIR, 'controllerLibrary')

# In this instance the directory variable is defined as the directory of where
# the python script is located
DIRECTORY = os.path.dirname(os.path.realpath(__file__))
LIBRARY_PATH = os.path.join(DIRECTORY, 'Library')

# print DIRECTORY
# print LIBRARY_PATH


def create_directory(directory=LIBRARY_PATH):
    '''If the default library directory or a new library directory is not
        found a new one is created

    Keyword Arguments:
        directory {string} -- Input directory to create asset library
                                (default: {LIBRARY_PATH})
    '''

    # if controllerLibrary directory does not exists
    # make the directory
    if not os.path.exists(directory):
        os.mkdir(directory)


class AssetLibrary(dict):
    '''Dictionary based class used to store information about Maya assets
    '''

    def save_ctrl(self, name, directory=LIBRARY_PATH, screenshot=True, **info):
        '''Creates new entry into asset library and stores information into
            json files

        Arguments:
            name {string} -- Name of the asset to be saved
            **info {string} -- Any additional information the user wants to
                                save into a asset's dictionary entry

        Keyword Arguments:
            directory {string} -- Path of the asset library
                                    (default: {LIBRARY_PATH})
            screenshot {boolean} -- Toggle used to determine if when saving a
                                    new asset should a screenshot of the asset
                                    be included or not
                                    (default: {True})
        '''

        create_directory(directory)

        path = os.path.join(directory, '{0}.ma'.format(name))
        info_file = os.path.join(directory, '{0}.json'.format(name))

        info['name'] = name
        info['path'] = path

        cmds.file(rename=path)

        if cmds.ls(selection=True):
            cmds.file(type='mayaAscii', exportSelected=True)
        else:
            cmds.file(save=True, type='mayaAscii', force=True)

        if screenshot:
            info['screenshot'] = self.save_screenshot(
                name, directory=directory)

        with open(info_file, 'w') as f:
            json.dump(info, f, indent=4)

        self[name] = info

    def find_ctrl(self, directory=LIBRARY_PATH):
        '''Find assets within asset library

        Keyword Arguments:
            directory {string} -- Path of the asset library
                                    (default: {LIBRARY_PATH})
        '''

        self.clear()

        if not os.path.exists(directory):
            return

        files = os.listdir(directory)

        # filter out non maya files
        maya_files = \
            [f for f in files if f.endswith('.ma') or f.endswith('.mb')]

        for maya_file in maya_files:
            file_name, ext = os.path.splitext(maya_file)

            path = os.path.join(directory, maya_file)

            info_file = '{0}.json'.format(maya_file)
            if info_file in files:
                info_file = os.path.join(directory, info_file)

                with open(info_file, 'r') as f:
                    info = json.load(f)

                    pprint.pprint(info)
            else:
                print 'No info found'
                info = {}

            screenshot = '{0}.jpg'.format(file_name)
            if screenshot in files:
                info['screenshot'] = os.path.join(directory, file_name)

            info['name'] = file_name
            info['path'] = path

            # since this class is of type dict, it can be treated like a dict
            self[file_name] = info

        pprint.pprint(self)

    def load_ctrl(self, name):
        '''Imports selected asset into current Maya scene

        Arguments:
            name {string} -- Name of the asset to be imported
        '''

        path = self[name]['path']

        cmds.file(path, i=True, usingNamespaces=False)

    def save_screenshot(self, name, directory=DIRECTORY):
        '''[summary]

        Arguments:
            name {string} -- Name of the asset to be used to make
                              screenshot file

        Keyword Arguments:
            directory {string} -- Path of the asset library
                                    (default: {LIBRARY_PATH})

        Returns:
            string -- Returns path of the screenshot file
        '''

        path = os.path.join(directory, '{0}.jpg'.format(name))

        cmds.viewFit()
        cmds.setAttr('defaultRenderGlobals.imageFormat', 8)

        cmds.playblast(
            completeFilename=path,
            forceOverwrite=True,
            format='image',
            width=200,
            height=200,
            showOrnaments=False,
            startTime=1,
            endTime=1,
            viewer=False)

        return path
