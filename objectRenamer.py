from maya import cmds

SUFFIXES = {
    'mesh': 'geo',
    'joint': 'jnt',
    'camera': None
}

DEFAULT_SUFFIX = 'grp'


def rename(selection=False):
    objects = cmds.ls(selection=seleciton, dag=True, long=True)

    if selection and not objects:
        raise RuntimeError('Nothing was selected')
    else:

        objects.sort(key=len, reverse=True)

        for obj in objects:
            short_name = obj.split('|')[-1]

            children = \
                cmds.listRelatives(obj, children=True, fullPath=True) or []

            if len(children) == 1:
                child = children[0]
                obj_type = cmds.objType(child)
            else:
                obj_type = cmds.objType(obj)

            suffix = SUFFIXES.get(obj_type, DEFAULT_SUFFIX)

            if not suffix:
                continue

            if obj.endswith('_' + suffix):
                continue
            else:
                new_name = short_name + '_' + suffix

                cmds.rename(obj, new_name)

                index = objects.index(obj)
                objects[index] = obj.replace(short_name, new_name)

        return objects
