import bpy, sys, json, time
engine = sys.argv[sys.argv.index('--')+1]
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
bpy.ops.mesh.primitive_cube_add(size=2); cube = bpy.context.object
mat = bpy.data.materials.new('m'); mat.use_nodes = True
mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.12, 0.37, 0.23, 1)
cube.data.materials.append(mat)
bpy.ops.object.light_add(type='SUN'); bpy.context.object.data.energy = 3
bpy.ops.object.camera_add(location=(4, -4, 3), rotation=(1.1, 0, 0.8)); sc.camera = bpy.context.object
sc.render.engine = engine
if engine == 'CYCLES': sc.cycles.samples = 16; sc.cycles.device = 'CPU'
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 192, 108, 100
sc.render.filepath = sys.argv[sys.argv.index('--')+2]
t = time.time(); bpy.ops.render.render(write_still=True)
print('RESULT', json.dumps({'engine': engine, 'seconds': round(time.time()-t, 2), 'version': bpy.app.version_string}))
