#!/usr/bin/env python
import os
import bpy

# loops over all subfolder
CONVERT_DIR = "absolut/path/to/meshes/directory"


def file_iter(path, ext):
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
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
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                obj.select = True
            else:
                obj.select = False
            bpy.ops.object.delete()
        bpy.ops.import_mesh.stl(filepath=filepath_src)
        bpy.ops.export_scene.fbx(filepath=filepath_dst)

    for filepath_src in file_iter(base_path, ".dae"):
        filepath_dst = os.path.splitext(filepath_src)[0] + ".fbx"

        print("Converting %r -> %r" % (filepath_src, filepath_dst))

        for obj in bpy.context.scene.objects:
            print(" delete obj ")
            try:
                if obj.type == 'MESH':
                    print("if true")
                    obj.select = True
                else:
                    print("if false")
                    obj.select = False
                bpy.ops.object.delete()
                print("after delete")
            except:
                print("Error during deleting object")
                break

        print("Import ", filepath_src)
        try:
            bpy.ops.wm.collada_import(filepath=filepath_src, import_units=True)
        except:
            print("Could not import ", filepath_src)
            continue

        print("Export ", filepath_dst)
        try:
            bpy.ops.export_scene.fbx(filepath=filepath_dst)
        except:
            print("Could not export ", filepath_dst)
            continue
           
    for filepath_src in file_iter(base_path, ".obj"):
        filepath_dst = os.path.splitext(filepath_src)[0] + ".fbx"

        print("Converting %r -> %r" % (filepath_src, filepath_dst))

    #     reset_blend()
        for obj in bpy.context.scene.objects:
            bpy.ops.object.select_all(action='DESELECT')
            if obj.type == 'MESH':
                #obj.select = True
                obj.select_set(True)
            else:
                obj.select_set(False)
            bpy.ops.object.delete()
        bpy.ops.import_scene.obj(filepath=filepath_src)
        bpy.ops.export_scene.fbx(filepath=filepath_dst, global_scale=0.1)

if __name__ == "__main__":
    convert_recursive(CONVERT_DIR)
