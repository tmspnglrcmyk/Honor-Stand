import bpy, sys, os, math
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:]
path,out=args[0],args[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
ext=os.path.splitext(path)[1].lower()
if ext=='.fbx': bpy.ops.import_scene.fbx(filepath=path)
elif ext=='.blend': bpy.ops.wm.open_mainfile(filepath=path)
elif ext=='.glb': bpy.ops.import_scene.gltf(filepath=path)
elif ext=='.obj': bpy.ops.wm.obj_import(filepath=path)
sc=bpy.context.scene
meshes=[o for o in sc.objects if o.type=='MESH']
pts=[o.matrix_world@Vector(c) for o in meshes for c in o.bound_box]
mn=Vector([min(p[i] for p in pts) for i in range(3)]); mx=Vector([max(p[i] for p in pts) for i in range(3)])
c=(mn+mx)/2; r=(mx-mn).length/2
cam=bpy.data.objects.new('cam',bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera=cam
d=Vector(tuple(float(x) for x in os.environ.get('VIEW','1,-1.3,0.7').split(','))).normalized(); cam.location=c+d*r*float(os.environ.get('DIST','2.6'))
cam.rotation_euler=(c-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.clip_end=r*20; cam.data.clip_start=r*0.01
sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=24; sc.cycles.use_denoising=False
w=bpy.data.worlds.new('w'); sc.world=w; w.use_nodes=True; w.node_tree.nodes['Background'].inputs[0].default_value=(0.6,0.6,0.62,1)
sun=bpy.data.objects.new('sun',bpy.data.lights.new('sun','SUN')); sun.data.energy=3; sun.rotation_euler=(0.7,0.2,0.5); sc.collection.objects.link(sun)
sc.render.resolution_x=800; sc.render.resolution_y=600; sc.render.filepath=out
bpy.ops.render.render(write_still=True)
