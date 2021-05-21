#!/usr/bin/env python3

#https://medium.com/@behreajj/scripting-curves-in-blender-with-python-c487097efd13

import bpy
import nibabel
import numpy
import sys
import random
import colorsys
import os
import json

with open('config.json') as config_json:
    config = json.load(config_json)

#bundles to include in the animation
bundles_to_show = [ 1, 2, 7, 12, 16, 17, 31, 32 ]
#bundles_to_show = [ 1, ]
bundles_to_animate = [ 16, 17 ]

##verified

# 1: AF_left         (Arcuate fascicle)
# 2: AF_right
# 3: ATR_left        (Anterior Thalamic Radiation)
# 4: ATR_right
# 15: ----          superior longitudinal fasiclus - left?

# 6: CC_1            (Rostrum) connecting the orbital surfaces of the frontal lobes
# 7: CC_2            (Genu) aka forceps minor
# 12: CC_7           (Splenium) aka forceps major

# 16: CST right
# 17: CST left

# 31: OR_right
# 32: OR_left        (Optic radiation) 

## not yet verified

# 5: CA              (Commissure Anterior)
# 8: CC_3            (Rostral body (Premotor))
# 9: CC_4            (Anterior midbody (Primary Motor))
# 10: CC_5           (Posterior midbody (Primary Somatosensory))
# 11: CC_6           (Isthmus)
# 13: CG_left        (Cingulum left)
# 14: CG_right   


# 17: MLF_left       (Middle longitudinal fascicle)
# 18: MLF_right

# 19: FPT_left       (Fronto-pontine tract)
# 20: FPT_right 
# 21: FX_left        (Fornix)
# 22: FX_right
# 23: ICP_left       (Inferior cerebellar peduncle)
# 24: ICP_right 
# 25: IFO_left       (Inferior occipito-frontal fascicle) 
# 26: IFO_right
# 27: ILF_left       (Inferior longitudinal fascicle) 
# 28: ILF_right 
# 29: MCP            (Middle cerebellar peduncle)
# 30: OR_left        (Optic radiation) 
# 31: OR_right
# 32: POPT_left      (Parieto‐occipital pontine)
# 33: POPT_right 
# 34: SCP_left       (Superior cerebellar peduncle)
# 35: SCP_right 
# 36: SLF_I_left     (Superior longitudinal fascicle I)
# 37: SLF_I_right 
# 38: SLF_II_left    (Superior longitudinal fascicle II)
# 39: SLF_II_right
# 40: SLF_III_left   (Superior longitudinal fascicle III)
# 41: SLF_III_right 
# 42: STR_left       (Superior Thalamic Radiation)
# 43: STR_right 
# 44: UF_left        (Uncinate fascicle) 
# 45: UF_right 
# 46: CC             (Corpus Callosum - all)
# 47: T_PREF_left    (Thalamo-prefrontal)
# 48: T_PREF_right 
# 49: T_PREM_left    (Thalamo-premotor)
# 50: T_PREM_right 
# 51: T_PREC_left    (Thalamo-precentral)
# 52: T_PREC_right 
# 53: T_POSTC_left   (Thalamo-postcentral)
# 54: T_POSTC_right 
# 55: T_PAR_left     (Thalamo-parietal)
# 56: T_PAR_right 
# 57: T_OCC_left     (Thalamo-occipital)
# 58: T_OCC_right 
# 59: ST_FO_left     (Striato-fronto-orbital)
# 60: ST_FO_right 
# 61: ST_PREF_left   (Striato-prefrontal)
# 62: ST_PREF_right 
# 63: ST_PREM_left   (Striato-premotor)
# 64: ST_PREM_right 
# 65: ST_PREC_left   (Striato-precentral)
# 66: ST_PREC_right 
# 67: ST_POSTC_left  (Striato-postcentral)
# 68: ST_POSTC_right
# 69: ST_PAR_left    (Striato-parietal)
# 70: ST_PAR_right 
# 71: ST_OCC_left    (Striato-occipital)
# 72: ST_OCC_right

random.seed(12) #for color

print("loading track.trk")
trk = nibabel.streamlines.load(config["track"])
sdata = trk.tractogram.data_per_streamline    

print("loading right pial surfaces")
bpy.ops.import_mesh.stl(filepath="rh.stl")
rh = bpy.data.objects["Rh"]
rh.scale = (-0.1, 0.1, 0.1) #need to flip x-axis (and scale it by 1/10)
rh.active_material = bpy.data.materials["pial"]
for p in rh.data.polygons:
    p.use_smooth = True

print("loading left pial surfaces")
bpy.ops.import_mesh.stl(filepath="lh.stl")
lh = bpy.data.objects["Lh"]
lh.scale = (-0.1, 0.1, 0.1) #need to flip x-axis (and scale it by 1/10)
lh.active_material = bpy.data.materials["pial"]
for p in lh.data.polygons:
    p.use_smooth = True

print("finxing min/max of all streamlines")
all_streamlines = numpy.concatenate(trk.streamlines)
min_coords = numpy.amin(all_streamlines, axis=0)/10
max_coords = numpy.amax(all_streamlines, axis=0)/10
mid_coords = (min_coords + max_coords)/2

#reorient fibers roughtly in the same direction
#from dipy.segment.clustering import QuickBundles
#qb = QuickBundles(numpy.inf, metric=metric)

#sort streamlines into separate bundles
bundles = {}
for idx in range(0, len(trk.streamlines)):

    #we need bundle_code to separate streamlines
    if "bundle_code" not in sdata[idx]:
        continue

    code = int(numpy.squeeze(sdata[idx]["bundle_code"]))
    if code not in bundles_to_show:
        continue

    if code not in bundles:
        bundles[code] = []
    bundle = bundles[code]

    #limit the number of streamlines per bundle
    if len(bundle) < 2000:
        bundle.append(trk.streamlines[idx])

#reorient streamlines
from dipy.tracking.streamline import orient_by_streamline
for code in bundles:
    print("reorienting", code)
    orient_by_streamline(bundles[code], bundles[code][0], in_place=True)

#TODO merge streamlines that are near each other and update its thickness? 
#for code in bundles:
#    streamlines = bundles[code]
#    print(streamlines[0])
#    sys.exit(1)

#TODO - should I move this to empty.blend?
def vecCircle(name):
    bpy.ops.mesh.primitive_circle_add(vertices=3, radius=0.010)
    obj = bpy.context.active_object
    obj.name = name
    bpy.ops.object.convert(target='CURVE', keep_original=False)
    return obj
tor0refCirc = vecCircle("streamline_template")

for code in bundles:
    groupname="group."+str(code)
    group = bpy.data.collections.new(groupname)
    print(groupname)

    matname = "Material."+str(code)
    #mat = bpy.data.materials.new(name=matname)
    #rgb = colorsys.hsv_to_rgb(random.random(), 0.8, 0.7)
    #mat.diffuse_color = (rgb[0], rgb[1], rgb[2], 1) #alpha doesn't matter?
    #mat.roughness = 0.2
    #mat.specular_intensity = 0.1 #intensity of sparkles

    mat = bpy.data.materials["streamline"].copy()
    nodes = mat.node_tree.nodes
    principled = next(n for n in nodes if n.type == 'BSDF_PRINCIPLED')
    rgb = colorsys.hsv_to_rgb(random.random(), 0.8, 0.7)
    principled.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1) #alpha doesn't matter?

    #w = 0
    for streamline in bundles[code]:
        #w+=1

        crv = bpy.data.curves.new(name='rcrv', type='CURVE')
        crv.dimensions = '3D'
        if code in bundles_to_animate:
            crv.bevel_factor_end = 0
            crv.keyframe_insert("bevel_factor_end", frame=120)
            crv.bevel_factor_end = 1
            crv.keyframe_insert("bevel_factor_end", frame=540)

        spline = crv.splines.new(type='NURBS') #type='NURBS'#POLY

        # streamline 
        #[[ 118.59422  -128.7478    -46.905884]
        # [ 120.05688  -131.50235   -45.590797]
        # [ 120.76991  -134.19774   -44.692375]
        # [ 120.876724 -137.37282   -44.030525]]
        coords = numpy.insert(streamline/10, 3, 1.0, axis=1) #recrease size by 10, then add 1.0 (weight) to the 3D coordinates
        #[[ 11.859423  -12.874781   -4.6905885   1.       ]
        # [ 12.005688  -13.150235   -4.5590796   1.       ]
        # [ 12.076991  -13.419774   -4.4692373   1.       ]
        # [ 12.087672  -13.737282   -4.4030523   1.       ]

        #ravel() will flatten the array into this
        #[ 11.859423  -12.874781   -4.6905885   1.         12.005688  -13.150235  -4.5590796   1.         12.076991  -13.419774   -4.4692373   1. ...

        spline.points.add(len(coords)-1) #first point contains number of coords-1?
        spline.points.foreach_set("co", coords.ravel())
        
        obj = bpy.data.objects.new('streamline.'+str(len(group.objects)), crv)
        obj.location = mid_coords*-1
        obj.data.bevel_object = tor0refCirc
        obj.active_material = mat
       
        group.objects.link(obj)

    print("..added streamlines", len(group.objects))
    bpy.context.scene.collection.children.link(group)

print("done drawing!")

# render to png (it only works if I set -b)
if bpy.app.background:
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    for frame_nr in range(1, 720+1, 1):
        filepath= "output/frame."+str(frame_nr)+".png"
        if os.path.exists(filepath):
            print("frame already exists", filepath)
            continue
        print("rendering frame", frame_nr)
        bpy.context.scene.frame_set(frame_nr)
        bpy.context.scene.render.filepath = filepath
        bpy.ops.render.render(use_viewport = True, write_still=True)


