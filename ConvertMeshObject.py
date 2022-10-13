#!/usr/bin/env python
import os
import bpy

# loops over all subfolder
CONVERT_DIR = "/path/to/meshes/"


def file_iter(path, ext):
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            print(filename)
            extension = os.path.splitext(filename)[1]
            if extension.lower().endswith(ext):
                yield os.path.join(dirpath, filename)



def reset_blend():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def convert_recursive(base_path):
    for filepath_src in file_iter(base_path, ".stl"):
        filepath_dst = os.path.splitext(filepath_src)[0] + ".fbx"

        print("Converting %r -> %r" % (filepath_src, filepath_dst))

    #     reset_blend()
        #select all objects in scene
        for obj in bpy.context.scene.objects:
                obj.select_set(True)
        #delete all selected objects
        try:
            bpy.ops.object.delete()
        except Exception as e:
            print("Error during object deletion: ",e)

        try:
            print(obj.type)
            for obj in bpy.context.scene.objects:
                if obj.type != 'MESH':
                    obj.select_set(True)
                else:
                    obj.select_set(False)
            bpy.ops.object.delete()
            bpy.ops.import_mesh.stl(filepath=filepath_src)
            bpy.ops.export_scene.fbx(filepath=filepath_dst)
        except Exception as e:
            print("Error during stl conversion: ",e)


    for filepath_src in file_iter(base_path, ".dae"):
        filepath_dst = os.path.splitext(filepath_src)[0] + ".fbx"

        print("Converting %r -> %r" % (filepath_src, filepath_dst))

        for obj in bpy.context.scene.objects:
            try:
                print(obj)
                obj.select_set(True)
                #else:
               #     obj.select_set(False)
            except Exception as e:
                print("Error during deleting object ", e)
                break
        try:
            bpy.ops.object.delete()
            print("Import ", filepath_src)
            bpy.ops.wm.collada_import(filepath=filepath_src, import_units=True)
        except Exception as e:
            print("Could not import ", filepath_src, "Error: ", e)
            continue


        try:
            print("Export ", filepath_dst)
            bpy.ops.export_scene.fbx(filepath=filepath_dst)
        except Exception as e:
            print("Could not export ", filepath_dst, "Error: ", e)
            continue

if __name__ == "__main__":
    print("start")
    convert_recursive(CONVERT_DIR)
