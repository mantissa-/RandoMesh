# RandoMesh created by Midge "mantissa" Sinnaeve (mantissa.xyz)
# Downloaded form https://github.com/mantissa-/RandoMesh
# Licensed under GPL v3

bl_info = {
    "name": "RandoMesh",
    "author": "Midge \"Mantissa\" Sinnaeve",
    "version": (0, 1, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Tool Shelf > RandoMesh Tab",
    "description": "Add randomized geometry to a mesh",
    "warning": "This addon can be slow and use a lot of RAM, keep an eye on your system resources with high numbers of iterations",
    "wiki_url": "https://github.com/mantissa-/RandoMesh",
    "category": "3D View",
}

import bpy
import time
import math
import random
from random import randint
from bpy.props import (IntProperty, FloatProperty, BoolProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, PropertyGroup)

#------------#
# PROPERTIES #
#------------#

class RandoMeshProps(PropertyGroup):

    keep : BoolProperty(
        name = "Keep Original Mesh",
        description = "Keep a copy of the source mesh",
        default = True,
        subtype = 'ANGLE'
        )
    
    mode : EnumProperty(
        name = "Mode",
        description = "Mesh Mode",
        items = [
            ('VERT', "Vertices", "Operate on vertices"),
            ('EDGE', "Edges", "Operate on edges"),
            ('FACE', "Faces", "Operate on faces")
        ],
        default = 'EDGE'
        )

    iterations : IntProperty(
        name = "Iterations",
        description = "RandoMesh Iterations",
        default = 5,
        min = 0,
        max = 20,
        soft_max = 10
        )
        
    subSmooth : FloatProperty(
        name = "Subdiv Smooth:",
        description = "Subdivision Smoothing",
        default = 0,
        soft_min = 0,
        max = 1.0,
        precision = 1
        )

    extrude : BoolProperty(
        name = "Extrude Random",
        description = "Enable Random Extrusion",
        default = True
        )
        
    extrudeMin : FloatProperty(
        name = "Min:",
        description = "Minimum Extrusion",
        default = -0.001,
        soft_min = -1.0,
        max = 0.0,
        precision = 3
        )
        
    extrudeMax : FloatProperty(
        name = "Max:",
        description = "Minimum Extrusion",
        default = 0.001,
        soft_min = 1.0,
        max = 1.0,
        precision = 3
        )
        
    poke : BoolProperty(
        name = "Poking",
        description = "Enable Random Poking",
        default = True
        )
        
    tri : BoolProperty(
        name = "Triangulation",
        description = "Enable Random Triangulation",
        default = True
        )

    decimate : BoolProperty(
        name = "Decimation",
        description = "Enable Random Decimation",
        default = True
        )
        
    smooth : BoolProperty(
        name = "Smoothing",
        description = "Enable Random Smoothing",
        default = True
        )
    
    wireframe : BoolProperty(
        name = "Wireframe",
        description = "Enable Wireframe",
        default = False
        )


#----#
# UI #
#----#

class RandoMeshPanel(bpy.types.Panel):
    """Creates a Panel in the sidebar"""
    bl_label = "RandoMesh"
    bl_idname = "OBJECT_PT_randomesh"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    #bl_context = "object"
    bl_category = "RandoMesh"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        col = layout.column(align=False)
        row = col.row(align=True)

        col.prop(scene.rmprop, "keep")

        col.separator()
        col.label(text="ITERATION OPTIONS")
        col.prop(scene.rmprop, "mode")
        col.prop(scene.rmprop, "iterations")
        col.prop(scene.rmprop, "subSmooth")
        col.separator()

        #extrusion
        col.prop(scene.rmprop, "extrude")
        col = layout.column(align=True)
        if scene.rmprop.extrude == False:
            col.enabled = False
        col.prop(scene.rmprop, "extrudeMin")
        col.prop(scene.rmprop, "extrudeMax")
        
        #switches
        col = layout.column(align=False)
        col.prop(scene.rmprop, "poke")
        col.prop(scene.rmprop, "tri")
        col.separator()
        col.label(text="POST FX")
        col.prop(scene.rmprop, "decimate")
        col.prop(scene.rmprop, "smooth")
        col.prop(scene.rmprop, "wireframe")

        col.separator()
        sub = col.row()
        sub.scale_y = 2.0
        sub.operator("wm.randomesh")


#----------#
# OPERATOR #
#----------#

class RandoMesh(bpy.types.Operator):
    """RandoMesh Operator"""
    bl_idname = "wm.randomesh"
    bl_label = "DESTROY THAT MESH"
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        
        rmp = bpy.context.scene.rmprop
        
        def randfloat(low, high):
            return random.random()*(high-low) + low

        def rsl(pct):
            if (2, 93, 0) > bpy.app.version:
                bpy.ops.mesh.select_random(percent=pct, seed=randint(1,9999))
            else:
                bpy.ops.mesh.select_random(ratio=pct/100, seed=randint(1,9999))
            
        def rgs(pct, min, max):
            rsl(pct)
            for j in range (min, max):
                bpy.ops.mesh.select_more()

        def randomesh(iter):
            opstart = time.time()
            
            boo = bpy.ops.object
            bom = bpy.ops.mesh
            
            print("Iterations: " + str(iter) + '\n' +"-------")
            

            if rmp.keep == True:
                boo.duplicate()
            
            boo.convert(target='MESH')

            #deselect
            boo.editmode_toggle()
            bom.select_mode(use_extend=False, use_expand=False, type=rmp.mode)
            bom.select_all(action='SELECT')
            
            max = 0

            for i in range (0, iter):
                start = time.time()

                bom.select_all(action='DESELECT')

                grow = randint(6, 12) - max
                shrink = randint (1, 3)
                print()
                
                #select random & grow
                rgs(0.15, 0, grow)
                if grow > 10:
                    max += 1
                
                #shrink selection
                for j in range (0, shrink):
                    bom.select_less()
                
                #extrude
                ext = round(randfloat(rmp.extrudeMin, rmp.extrudeMax), 4)
                if rmp.extrude == True:
                    if ext != 0:
                        bom.extrude_region_shrink_fatten(TRANSFORM_OT_shrink_fatten={"value":-ext}) #"use_even_offset":True

                mutate = randint(0,6)
                poke = False
                tri = False
                
                #poke
                if rmp.poke == True and mutate < 2:
                    for j in range(3,10):
                        bom.select_less()    
                    bom.poke(offset=0, use_relative_offset=True)
                    poke = True
                
                
                # triangulate
                if rmp.tri == True and mutate > 4:
                    for j in range(3,10):
                        bom.select_less()    
                    bom.quads_convert_to_tris(quad_method='SHORTEST_DIAGONAL', ngon_method='CLIP')
                    tri = True
                
                #subdivide
                bom.subdivide(number_cuts=1, quadcorner='INNERVERT',fractal=0.0, smoothness=rmp.subSmooth)
                
                end = time.time()
                print("Iteration #" + str(i + 1) + ": "  + str(round((end - start), 3))  + "s\tG:" + str(grow) +" | S:" + str(shrink) + " | Extrude: " + str(ext) + "\tP:" + (str(poke)[0:1]) + "\tT:" + (str(tri)[0:1]))
            
            if rmp.decimate == True:
                #vgroup
                bom.select_all(action='DESELECT')
                rgs(0.5, 5, 8)
                boo.vertex_group_add()
                boo.vertex_group_assign()
                boo.vertex_group_smooth(repeat=randint(0,10))
                
                #decimate
                start = time.time()
                ratio = round(randfloat(0.25, 0.5), 2)
                bom.decimate(ratio=ratio, use_vertex_group=True)
                end = time.time()
                print("\nDecimation: " + str(round((end - start),4)) + "s\tRatio: " + str(ratio))
            
            if rmp.smooth == True:
                #smooth
                start = time.time()
                repeat = randint(5,30)
                bom.vertices_smooth(repeat=repeat)
                end = time.time()
                print("Smoothing: " + str(round((end - start),4)) + "s\tIterations: " + str(repeat))
                
            if rmp.wireframe == True:
                #wire
                start = time.time()
                thickness = round(randfloat(0.1, 0.4), 2)
                bom.select_all(action='SELECT')
                bom.duplicate()
                bom.faces_shade_flat()
                bom.separate()
                bom.select_all(action='SELECT')
                bom.wireframe(use_boundary=True, use_even_offset=False, use_relative_offset=True, use_replace=True, thickness=thickness)
                end = time.time()
                print("Wireframe: " + str(round((end - start),4)) + "s\tThickness: " + str(thickness))

            boo.editmode_toggle()
            
            opend = time.time()
            print("Done! (" + str(round((opend - opstart),0)) + "s total)")
            
        
        def errmsg(message = "", title = "Message Box", icon = 'INFO'):

            def draw(self, context):
                self.layout.label(text=message)

            bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

        if bpy.context.object.mode != 'OBJECT':
            errmsg("RandoMesh only works in object mode", "Uh Oh!", 'ERROR')
        else:
            randomesh(rmp.iterations)
        
        return {'FINISHED'}


#----------#
# REGISTER #
#----------#

def register():
    bpy.utils.register_class(RandoMeshPanel)
    bpy.utils.register_class(RandoMesh)
    bpy.utils.register_class(RandoMeshProps)
    bpy.types.Scene.rmprop = PointerProperty(type=RandoMeshProps)

def unregister():
    bpy.utils.unregister_class(RandoMeshPanel)
    bpy.utils.unregister_class(RandoMesh)
    bpy.utils.unregister_class(RandoMeshProps)
    del bpy.types.Scene.rmprop

if __name__ == "__main__":
    register()
