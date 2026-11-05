import bpy, sys, os
d, res, dist = sys.argv[sys.argv.index('--')+1:]
res=int(res); dist=float(dist)
bpy.ops.wm.open_mainfile(filepath=os.path.join(d,'high.blend'))
sc=bpy.context.scene; sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=256
w=bpy.data.worlds.new('w'); sc.world=w; w.light_settings.distance=dist
o=[x for x in bpy.data.objects if x.type=='MESH'][0]
img=bpy.data.images.new('ao',res,res,float_buffer=True)
mat=bpy.data.materials.new('bake'); mat.use_nodes=True; nt=mat.node_tree
tn=nt.nodes.new('ShaderNodeTexImage'); tn.image=img; nt.nodes.active=tn
o.data.materials.clear(); o.data.materials.append(mat)
bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active=o
sc.render.bake.margin=16
bpy.ops.object.bake(type='AO')
import numpy as np; px=np.array(img.pixels[:]).reshape(-1,4); print('mean',px.mean(0), 'max', px.max(0))
from PIL import Image
a=(np.clip(px[:,0].reshape(res,res)[::-1],0,1)*255+0.5).astype(np.uint8)
Image.fromarray(a,'L').save(os.path.join(d,'ao_bake.png'))
print('ok')
