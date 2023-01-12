bl_info = {
    "name" : "My Cursor",
    "version": (0, 1, 0),
    "author" : "Franco Cappellaro",
    "description" : "move objects in between 2 points",
    "blender" : (3, 3, 0),
    "location" : "View3D",
    "category" : "3D View" 
}


import bpy
import mathutils
from mathutils import Vector
import math 



def Distance_Between_Cursors():
    
    if bpy.context.scene.unit_settings.system == 'METRIC':
        if bpy.context.scene.unit_settings.length_unit == 'MILLIMETERS' :
            offset = 1000
        elif bpy.context.scene.unit_settings.length_unit == 'CENTIMETERS' :
            offset = 100
        else:
            offset = 1    
    

    x1 = bpy.context.scene.mycursor_x
    y1 = bpy.context.scene.mycursor_y
    z1 = bpy.context.scene.mycursor_z
    
    x2 = bpy.context.scene.cursor.location[0]
    y2 = bpy.context.scene.cursor.location[1]
    z2 = bpy.context.scene.cursor.location[2]
    
    
    dx= abs(round((x1-x2)*offset, 2))
    dy= abs(round((y1-y2)*offset, 2))
    dz= abs(round((z1-z2)*offset, 2))
    
    dist=math.sqrt(pow((x2-x1), 2) + pow((y2-y1), 2) + pow((z2-z1), 2))
    dist = dist * offset
    distance = abs(round(dist, 2))
   
    
    misx = str(dx)
    distX = "Distance X:  " + misx
    misy = str(dy)
    distY = "Distance Y:  " + misy
    misz = str(dz)
    distZ = "Distance Z:  " + misz
    distance = str(distance)
    distance = "Total Distance:  " + distance

        
    def draw(self, context):
        row = self.layout.row() 
        row.label(text=distX)
        row = self.layout.row() 
        row.label(text=distY)
        row = self.layout.row() 
        row.label(text=distZ)        
        row = self.layout.row() 
        row.label(text=distance)   
                        
    bpy.context.window_manager.popup_menu(draw, title = "Distance", icon = 'INFO')



class distance_3dcursor(bpy.types.Operator):
    bl_idname = "tocurs.distance"
    bl_label = "Distance Between Cursors"


    def execute(self, context):

        Distance_Between_Cursors()
        
        return {'FINISHED'}


class save_3dcursor(bpy.types.Operator):
    bl_idname = "tocurs.savecursor"
    bl_label = "Copy Cursor Location"

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None

    def execute(self, context):
                
        context.scene.mycursor_x = bpy.context.scene.cursor.location[0] 
        context.scene.mycursor_y = bpy.context.scene.cursor.location[1]
        context.scene.mycursor_z = bpy.context.scene.cursor.location[2] 


        
        return {'FINISHED'}
    

class move_object_at_cursor(bpy.types.Operator):
    bl_idname = "tocurs.movetocursor"
    bl_label = "Move Objects to Cursor"

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None

    def execute(self, context):
        
        vect_loc_mycursor = Vector((context.scene.mycursor_x,
                            context.scene.mycursor_y, 
                            context.scene.mycursor_z))  
              
        newloc = vect_loc_mycursor - bpy.context.scene.cursor.location        
        
        for obj in bpy.context.selected_objects:
            obj.location -= newloc

        
        return {'FINISHED'}



class ADDON_PT_to_cursor(bpy.types.Panel):
    bl_idname = "ADDON_PT_tocursor"
    bl_label = "My Cursor"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"
    bl_context = "objectmode"

    
    @classmethod
    def poll(self, context):
        return True


    def draw(self, context):
        layout = self.layout
        row = layout.row()   
 #       row.scale_y = 3.0    

        box = self.layout.box()
        box.row().label(text="Location MyCursor") 
        split = box.row(align=True).split(factor=0.0, align=True)        
        split.prop(context.scene, "mycursor_x", text="X")
        split = box.row(align=True).split(factor=0.0, align=True)         
        split.prop(context.scene, "mycursor_y", text="Y")
        split = box.row(align=True).split(factor=0.0, align=True)         
        split.prop(context.scene, "mycursor_z", text="Z")

        row = layout.row()
        row.operator("tocurs.savecursor", text="Copy Cursor Location",icon='ORIENTATION_CURSOR')
              
        row = layout.row() 
        row.operator("tocurs.movetocursor",icon='UV_SYNC_SELECT')
        row = layout.row()
        row.operator("tocurs.distance",icon='DRIVER_DISTANCE')        




#class ToCursor(bpy.types.Menu):
#    bl_label = "Move to cursor"
#    bl_idname = "VIEW_MT_Move_to_Cursor"

#    def draw(self, context):
#        layout = self.layout        
#        layout.operator("tocurs.savecursor",icon='ORIENTATION_CURSOR')
#        layout.operator("tocurs.movetocursor",icon='UV_SYNC_SELECT')
#        layout.operator("tocurs.distance",icon='DRIVER_DISTANCE')




#def draw_item(self, context):
#    layout = self.layout
#    layout.menu("VIEW_MT_Move_to_Cursor")
    
    

classes = [
    save_3dcursor,
    move_object_at_cursor,
 #   ToCursor,
    distance_3dcursor,
    ADDON_PT_to_cursor,

    
]


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

    bpy.types.Scene.mycursor_x = bpy.props.FloatProperty(name="mycursor_x", default=0.0, unit='LENGTH')        
    bpy.types.Scene.mycursor_y = bpy.props.FloatProperty(name="mycursor_y", default=0.0, unit='LENGTH') 
    bpy.types.Scene.mycursor_z = bpy.props.FloatProperty(name="mycursor_z", default=0.0, unit='LENGTH')

#    bpy.types.VIEW3D_MT_object.append(draw_item)
    
  

def unregister():
    from bpy.utils import unregister_class
    
    for cls in classes:
        unregister_class(cls)

  #  bpy.types.VIEW3D_MT_object.remove(draw_item)
    
    

if __name__ == "__main__":
    register()
