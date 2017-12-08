"""
Context
https://docs.blender.org/api/current/bpy.context.html

bpy.context.scene: Scene
bpy.context.active_object: Object

Scene
https://docs.blender.org/api/current/bpy.types.Scene.html

scene.camera: Object<Camera>
scene.render: RenderSetting

Object<T>
https://docs.blender.org/api/current/bpy.types.Object.html

object.data: T


Camera
https://docs.blender.org/api/current/bpy.types.Camera.html

rotation: GUIだとdegree, pythonだとradian
rotation.x: pitch, 0:地, 90:水平, 180:天
rotation.y: roll, +:右回転(左傾き), -:左回転(右傾き)

RenderSetting
https://docs.blender.org/api/current/bpy.types.RenderSettings.html

"""

import datetime
import bpy
import numpy as np

today = datetime.datetime.today

V = np.array
VZ = V((0, 0, 0))
pi = np.pi

r2d = lambda rad: rad / np.pi * 180
d2r = lambda deg: deg / 180 * np.pi

rv2d = lambda rads: [r2d(n) for n in rads]
dv2r = lambda degs: [d2r(n) for n in degs]


class TimerLogger:
    def __init__(self, name='null', message='start'):
        self.name = name
        self.start = today()
        print("TimerLogger '%s' start: %s" % (name, str(self.start)))

    def log(self, message='logging'):
        time = today()
        print("TimerLogger '%s' %s: %s, %s" % (self.name, message, str(time), str(time-self.start)))


# (カメラ位置, 注視点) -> rotation
def lookat(src: list, dst: list, roll_deg=0) -> list:
    d = V(dst) - V(src)
    rad_h = np.arctan2(d[1], d[0])
    rad_v = np.arctan2(d[2], d[0]*d[0]+d[1]*d[1])
    rot_z = rad_h + d2r(90)
    rot_y = d2r(roll_deg)
    rot_x = rad_v - d2r(90)
    return (rot_x, rot_y, rot_z)

def set_render_resolution(w, h, scene=bpy.context.scene):
    render = scene.render
    render.resolution_x = w
    render.resolution_y = h

def set_camera(fov=70, loc=VZ, rot=VZ, mode='XYZ', scene=bpy.context.scene):
    camera = scene.camera

    # Set camera fov in degrees
    camera.data.angle = fov*(pi/180.0)

    # Set camera rotation in euler angles
    camera.rotation_mode = mode
    camera.rotation_euler[0] = rot[0]
    camera.rotation_euler[1] = rot[1]
    camera.rotation_euler[2] = rot[2]

    # Set camera translation
    camera.location.x = loc[0]
    camera.location.y = loc[1]
    camera.location.z = loc[2]

def test():
    src = (0, -5, 2)
    dst = (0, 0, 1)
    set_camera(70, src, lookat(src, dst))

test()
"""
Operation
https://docs.blender.org/api/current/bpy.ops.html

https://docs.blender.org/api/current/bpy.ops.object.html

bpy.ops.object.delete()
Delete selected objects
対象はobject.select=True

bpy.ops.mesh.primitive_plane_add(radius=0.5)
bpy.ops.mesh.primitive_circle_add(vertices=24, radius=0.5)
bpy.ops.mesh.primitive_grid_add(x_subdivisions=dx, y_subdivisions=dy, radius=0.5)
bpy.ops.mesh.primitive_cube_add(radius=0.5)
bpy.ops.mesh.primitive_cylinder_add(vertices=vertex, radius=0.5, depth=1.0)
bpy.ops.mesh.primitive_cone_add(vertices=vertex, radius1=0.5, radius2=0, depth=1.0)
bpy.ops.mesh.primitive_uv_sphere_add(size=0.5, segments=vertexXY, ring_count=vertexZ)
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=divide, size=0.5)
bpy.ops.mesh.primitive_torus_add(major_radius=0.5, minor_radius=radiusS, major_segments=vertexL, minor_segments=vertexS)
生成物はbpy.context.active_object

Context
https://docs.blender.org/api/current/bpy.context.html

bpy.context.scene: Scene
bpy.context.active_object: Object
bpy.context.selected_objects

Scene
https://docs.blender.org/api/current/bpy.types.Scene.html

scene.camera: Object<Camera>
scene.render: RenderSetting
scene.objects.unlink(obj)
scene.objects.active = obj
scene.cursor_location = coord

Object<T>
https://docs.blender.org/api/current/bpy.types.Object.html

object.data: T
object.select: boolean

Camera
https://docs.blender.org/api/current/bpy.types.Camera.html

rotation: GUIだとdegree, pythonだとradian
rotation.x: pitch, 0:地, 90:水平, 180:天
rotation.y: roll, +:右回転(左傾き), -:左回転(右傾き)

RenderSetting
https://docs.blender.org/api/current/bpy.types.RenderSettings.html

"""

import bpy
import numpy as np

V = np.array
V0 = V((0, 0, 0))
V1 = V((1, 1, 1))
pi = np.pi

r2d = lambda rad: rad / np.pi * 180
d2r = lambda deg: deg / 180 * np.pi

rv2d = lambda rads: [r2d(n) for n in rads]
dv2r = lambda degs: [d2r(n) for n in degs]

# (カメラ位置, 注視点) -> rotation
def lookat(src: list, dst: list, roll_deg=0) -> list:
    d = V(dst) - V(src)
    rad_h = np.arctan2(d[1], d[0])
    rad_v = np.arctan2(d[2], d[0]*d[0]+d[1]*d[1])
    rot_z = rad_h + d2r(90)
    rot_y = d2r(roll_deg)
    rot_x = rad_v - d2r(90)
    return (rot_x, rot_y, rot_z)

def set_render_resolution(w, h):
    render = bpy.context.scene.render
    render.resolution_x = w
    render.resolution_y = h

def set_camera(fov=None, loc=None, rot=None, mode=None):
    camera = bpy.context.scene.camera

    # Set camera fov in degrees
    if fov is not None:
        camera.data.angle = fov*(pi/180.0)

    # Set camera rotation in euler angles
    if mode is not None:
        camera.rotation_mode = mode # 'XYZ', etc
    if rot is not None:
        camera.rotation_euler[0] = rot[0]
        camera.rotation_euler[1] = rot[1]
        camera.rotation_euler[2] = rot[2]

    # Set camera translation
    if loc is not None:
        camera.location.x = loc[0]
        camera.location.y = loc[1]
        camera.location.z = loc[2]

# () -> Object[]
def get_selects():
    return bpy.context.selected_objects
# (Object[]) -> void
def set_selects(objs):
    for obj in objs:
        obj.select = True
# () -> void
def clear_selects():
    for obj in bpy.context.scene.objects:
        obj.select = False

def set_cursor(loc=V0):
    bpy.context.scene.cursor_location = loc

# UNION, DIFFERENCE, INTERSECT
csg_union = 'UNION'
csg_diff = 'DIFFERENCE'
csg_isect = 'INTERSECT'
def op_csg(obj1, obj2, op=csg_union, obj2del=True):
    bpy.context.scene.objects.active = obj1
    bpy.ops.object.modifier_add(type='BOOLEAN')
    bpy.context.object.modifiers["Boolean"].operation = op
    bpy.context.object.modifiers["Boolean"].object = obj2
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")
    if obj2del == True:
        bpy.context.scene.objects.unlink(obj2)
    return bpy.context.active_object

# (Object[]) -> Object
def join_objs(objs):
    set_selects(objs)
    bpy.context.active_object = objs[0]
    bpy.ops.object.join()
    return bpy.context.active_object

# moveはobjからの相対座標（move=V0だと同一座標）
def dupl_obj(obj, move=V0):
    set_selects((obj,))
    bpy.ops.object.duplicate_move(
        OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'},
        TRANSFORM_OT_translate={"value":move})
    return bpy.context.active_object

def del_objs(objs):
    set_selects(objs)
    bpy.ops.object.delete(use_global=False)

def set_obj_origin(obj, loc=V0):
    set_selects((obj,))
    set_cursor(loc)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    return obj

def export_objs(path, objs, global_scale=1.0):
    set_selects(objs)
    bpy.ops.export_scene.obj(
        filepath=path, 
        check_existing=False, 
        use_selection=True,
        global_scale=global_scale)


def assign_v3(l, r):
    for i in range(3):
        l[i] = r[i]

def lrs(l=None, r=None, s=None):
    def op(obj):
        if l is not None:
            assign_v3(obj.location, l)
        if r is not None:
            assign_v3(obj.rotation, r)
        if s is not None:
            assign_v3(obj.scale, s)
        return obj
    return op

op_null_lrs = lambda obj: obj

def new_cube(r=0.5, op=op_null_lrs):
    bpy.ops.mesh.primitive_cube_add(radius=r)
    return op(bpy.context.active_object)


def test_camera():
    src = (0, -5, 2)
    dst = (0, 0, 1)
    set_camera(70, src, lookat(src, dst))

def test_clone():
    obj1 = new_cube(1, lrs((1, 0, 0)))
    obj2 = dupl_obj(obj1)
    print(obj1)
    print(test_boolean)

def test_csg_export(file: string):
    obj1 = new_cube(1, lrs((0, 0, 0)))
    obj2 = new_cube(1, lrs((1, -1, 1)))
    obj3 = op_csg(obj1, obj2, csg_diff)  # obj1, obj2 は削除される
    export_objs(file, [obj3])

