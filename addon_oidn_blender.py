bl_info = {
    "name": "Intel Denoise",
    "author": "Alfonso Annarumma",
    "version": (1, 5, 4),
    "blender": (2, 76, 0),
    "location": "Toolshelf > Intel Denoise",
    "warning": "",
    "description": "Intel Denoise",
    "category": "3D View",
}

import bpy
import subprocess
import os
import platform
from bpy.types import Menu, Panel, UIList, PropertyGroup, Operator, AddonPreferences

from bpy.props import (
        StringProperty,
        BoolProperty,
        FloatProperty,
        IntProperty,
        CollectionProperty,
        BoolVectorProperty,
        PointerProperty,
        )

class RENDER_PG_intel_denoise(PropertyGroup):
    image_name = StringProperty(
            name="Image Name",
            default="Render"
            )

class RENDER_AP_intel_denoise(AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    oidn = StringProperty(
            name="oidn Intel Denoise Directory",
            subtype='FILE_PATH',
            default=""
            )
    

    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Set the Directory of oidn")
        layout.prop(self, "oidn")


def image_conv():
    syst = platform.system()
    
    if syst == 'Linux':
        conv = "convert"
    else:
        conv = "magick"
           
    return conv

def denoise(file_name, ext, dir):
    
    print("Start...")
    user_preferences = bpy.context.user_preferences
    addon_prefs = user_preferences.addons[__name__].preferences
    conv = image_conv()
    print(conv)
    print(dir+file_name+ext)
    data = bpy.data
    oidn = os.path.abspath(bpy.path.abspath(addon_prefs.oidn))
    img_arg = [
        "convert",
        dir+file_name+ext,
        "-endian",
        "LSB",
        dir+file_name+".pfm"
        ]
    print(img_arg)
    subprocess.run(img_arg)    

    print("Denoise...")
    print(oidn)
    myargs = [
        oidn+"/bin/denoise",
        "-ldr",
        dir+file_name+".pfm",
        "-o",
        dir+file_name+"_denoise.pfm",
        ]
    
    try:
        result = subprocess.run(myargs,check=True)
 
    except:
        print("Error in Denoise")
        return
    img_arg = [
        conv,
        dir+file_name+"_denoise.pfm",
        dir+file_name+"_denoise"+ext
        ]
    subprocess.run(img_arg)    
    
    data.images.load("//"+file_name+"_denoise"+ext)
    


class RENDER_OT_intel_denoise(Operator):
    """Intel Denoise """
    bl_idname = "scene.intel_denoise"
    bl_label = "Intel Denoise "


    def execute(self, context):
        
        scene = context.scene
        data = bpy.data
        file_name = scene.intel_denoise.image_name
        ext = scene.render.file_extension
        path = bpy.path
        filepath = path.abspath("//"+file_name+ext)
        split = os.path.split(filepath)
        dir = split[0]+"/"
        scene.render.filepath = "//"+file_name+ext
        bpy.ops.render.render( write_still=True )

        

        bpy.app.handlers.render_complete.append(denoise(file_name,ext,dir))
        #data.images.load("//"+file_name+ext)
        return {'FINISHED'}

class RENDER_PT_intel_denoise(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    
    bl_category = "Intel Denoise"
    bl_label = "Intel Denoise"
    bl_options = {'DEFAULT_CLOSED'}

   

    def draw(self, context):
        scene = context.scene
        
        image_settings = scene.render.image_settings
        layout = self.layout
        col = layout.column()
        col.label(text="Image Settings:") 
        col.prop(scene.intel_denoise, "image_name", text="Image Name")
        col.prop(scene.render, "filepath", text="Output")
        col.template_image_settings(image_settings, color_management=False)        

        
        col.operator("scene.intel_denoise")
  
   


def register():
    bpy.utils.register_class(RENDER_PG_intel_denoise)
    bpy.utils.register_class(RENDER_PT_intel_denoise)
    bpy.utils.register_class(RENDER_OT_intel_denoise)
    bpy.utils.register_class(RENDER_AP_intel_denoise)
    
    bpy.types.Scene.intel_denoise = PointerProperty(type=RENDER_PG_intel_denoise)

def unregister():
    del bpy.types.Scene.plandraw
    bpy.utils.unregister_class(RENDER_PG_intel_denoise)
    bpy.utils.unregister_class(RENDER_PT_intel_denoise)
    bpy.utils.unregister_class(RENDER_OT_intel_denoise)
    bpy.utils.unregister_class(RENDER_AP_intel_denoise)

if __name__ == "__main__":
    register() 
