# LOD per Blender-Decimate (Collapse), Quelle OBJ -> Ziel OBJ
import bpy, sys, os
src, dst, target = sys.argv[sys.argv.index('--')+1:]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.obj_import(filepath=src, forward_axis='Y', up_axis='Z')
o = bpy.context.selected_objects[0]; bpy.context.view_layer.objects.active = o
n0 = sum(len(p.vertices) - 2 for p in o.data.polygons)
m = o.modifiers.new('d', 'DECIMATE'); m.decimate_type = 'COLLAPSE'; m.ratio = int(target) / n0; m.use_collapse_triangulate = True
bpy.ops.object.modifier_apply(modifier='d')
print('Dreiecke', sum(len(p.vertices) - 2 for p in o.data.polygons))
bpy.ops.wm.obj_export(filepath=dst, export_selected_objects=True, export_materials=False, export_normals=False, export_uv=True, forward_axis='Y', up_axis='Z')
