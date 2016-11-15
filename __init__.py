import bpy

class ReprojectMask(bpy.types.Operator):
    """Reproject Mask"""
    bl_idname = "artist_paint.reproject_mask" 
                                     
     
    bl_label = "Reproject Mask by View"
    bl_options = { 'REGISTER', 'UNDO' }
    
    def execute(self, context):

        scene = context.scene


        #new code
        bpy.ops.object.editmode_toggle() #toggle edit mode
        bpy.ops.uv.project_from_view(camera_bounds=True, correct_aspect=False, scale_to_bounds=False) #project from view
        bpy.ops.object.editmode_toggle() #toggle back from edit mode
        bpy.ops.object.convert(target='MESH')#in obj mode, convert to mesh for correction on Artist Panel Vector Masks/Gpencil Masks

        bpy.ops.paint.texture_paint_toggle() #toggle texpaint
        return {'FINISHED'}
    
#next operator
class SolidfyDifference(bpy.types.Operator):
    """Solidify and Difference Mask"""
    bl_idname = "artist_paint.solidfy_difference"
    bl_label = "Add Solidy and Difference Bool"
    bl_options = { 'REGISTER','UNDO' }
    
    def execute(self, context):
        scene = context.scene
                
        
        #new code
        sel = bpy.context.selected_objects
        act = bpy.context.scene.objects.active
        
        for obj in sel:
            context.scene.objects.active = obj#set active to selected
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.dissolve_faces()#to get a clean single face for paint projection
            bpy.ops.object.editmode_toggle()

            bpy.ops.object.modifier_add(type='SOLIDIFY')#set soldifiy for bool
            bpy.context.object.modifiers["Solidify"].thickness = 0.3#thicker than active
            bpy.ops.transform.translate(value=(0, 0, 0.01), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, release_confirm=True)#attempt to only move bool brush up in Z
            
            context.scene.objects.active = act#reset active 
            
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.dissolve_faces()
            bpy.ops.object.editmode_toggle()

            
            bpy.ops.object.modifier_add(type='SOLIDIFY')#basic soldify for boolean
            bpy.ops.transform.translate(value=(0, 0, 0), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, release_confirm=True)#to move active 0 in Z
                
            
            bpy.ops.btool.boolean_diff()#call booltool
                
            
            return {'FINISHED'}           

        
        #user moves parent and then adjusts child
        #user calls reproject while in obj mode which returns mask to texpaint
        
#next operator
class SolidfyUnion(bpy.types.Operator):
    """Solidify and Union Mask"""
    bl_idname = "artist_paint.solidfy_union"
    bl_label = "Add Solidy and Union Bool"
    bl_options = { 'REGISTER','UNDO' }
    
    def execute(self, context):
        scene = context.scene
                
        
        #new code
        sel = bpy.context.selected_objects
        act = bpy.context.scene.objects.active
        
        for obj in sel:
            context.scene.objects.active = obj#set active to selected
            
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.dissolve_faces()#to get a single face for paint projection
            bpy.ops.object.editmode_toggle()
            
            bpy.ops.object.modifier_add(type='SOLIDIFY')#set soldifiy for bool
            bpy.context.object.modifiers["Solidify"].thickness = 0.3#thicker than active
            #bpy.ops.transform.translate(value=(0, 0, 0.01), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, release_confirm=True)#attempt to only move bool brush up in Z
            
            context.scene.objects.active = act#reset active 
            
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.dissolve_faces()
            bpy.ops.object.editmode_toggle()
            
            bpy.ops.object.modifier_add(type='SOLIDIFY')#basic soldify for boolean
            bpy.context.object.modifiers["Solidify"].thickness = 0.3#thicker than active
            #bpy.ops.transform.translate(value=(0, 0, 0), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, release_confirm=True)#to move active 0 in Z
                
            
            bpy.ops.btool.boolean_union()#call booltool
                
            
            return {'FINISHED'}           

        
        #user moves parent and then adjusts child
        #user calls reproject while in obj mode which returns mask to texpaint
        
        
#next operator
class RemoveMods(bpy.types.Operator):
    """Remove Modifiers"""
    bl_idname = "artist_paint.remove_modifiers"
    bl_label = "Remove Modifiers"
    bl_options = { 'REGISTER','UNDO' }
    
    def execute(self, context):
        scene = context.scene
                
        
        #new code
        context = bpy.context
        scene = context.scene
        obj = context.object

        # get a reference to the current obj.data
        old_mesh = obj.data

        # settings for to_mesh
        apply_modifiers = False
        settings = 'PREVIEW'
        new_mesh = obj.to_mesh(scene, apply_modifiers, settings)

        # object will still have modifiers, remove them
        obj.modifiers.clear()

        # assign the new mesh to obj.data 
        obj.data = new_mesh

        # remove the old mesh from the .blend
        bpy.data.meshes.remove(old_mesh)
        bpy.context.object.draw_type = 'TEXTURED'

        
                
            
        return {'FINISHED'}

class GenericOper(bpy.types.Operator):
    """Generic Operator"""
    bl_idname = "object.generic_operator" 
                                     
     
    bl_label = "Generic Operator Template"
    bl_options = { 'REGISTER', 'UNDO' }
    
    def execute(self, context):

        scene = context.scene


        #new code
        
        bpy.ops.paint.texture_paint_toggle() #toggle texpaint
        
        return {'FINISHED'}

class AlignLeft(bpy.types.Operator):
    """Left Align"""
    bl_idname = "object.align_left" 
                                     
     
    bl_label = "Align Objects Left"
    bl_options = { 'REGISTER', 'UNDO' }
    
    def execute(self, context):

        scene = context.scene


        #new code
        
        bpy.ops.object.align(align_mode='OPT_1', relative_to='OPT_4', align_axis={'X'}) #toggle texpaint
        
        return {'FINISHED'}
    
class AlignCenter(bpy.types.Operator):
    """Center Align"""
    bl_idname = "object.align_center" 
                                     
     
    bl_label = "Align Objects Center"
    bl_options = { 'REGISTER', 'UNDO' }
    
    def execute(self, context):

        scene = context.scene


        #new code
        
        bpy.ops.object.align(align_mode='OPT_2', relative_to='OPT_4', align_axis={'X'}) #toggle texpaint
        
        return {'FINISHED'}

class AlignRight(bpy.types.Operator):
    """Center Align"""
    bl_idname = "object.align_right" 
                                     
     
    bl_label = "Align Objects Right"
    bl_options = { 'REGISTER', 'UNDO' }
    
    def execute(self, context):

        scene = context.scene


        #new code
        
        bpy.ops.object.align(align_mode='OPT_3', relative_to='OPT_4', align_axis={'X'}) #toggle texpaint
        
        return {'FINISHED'}
    
class AlignTop(bpy.types.Operator):
    """Top Align"""
    bl_idname = "object.align_top" 
                                     
     
    bl_label = "Align Objects Top"
    bl_options = { 'REGISTER', 'UNDO' }
    
    def execute(self, context):

        scene = context.scene


        #new code
        
        bpy.ops.object.align(align_mode='OPT_3', relative_to='OPT_4', align_axis={'Y'}) 
        
        return {'FINISHED'}
    
class AlignHcenter(bpy.types.Operator):
    """Horizontal Center Align"""
    bl_idname = "object.align_hcenter" 
                                     
     
    bl_label = "Align Objects Horizontal Center"
    bl_options = { 'REGISTER', 'UNDO' }
    
    def execute(self, context):

        scene = context.scene


        #new code
        
        bpy.ops.object.align(align_mode='OPT_2', relative_to='OPT_4', align_axis={'Y'}) 
        
        return {'FINISHED'}
    
class AlignBottom(bpy.types.Operator):
    """Horizontal Bottom Align"""
    bl_idname = "object.align_bottom" 
                                     
     
    bl_label = "Align Objects Horizontal Bottom"
    bl_options = { 'REGISTER', 'UNDO' }
    
    def execute(self, context):

        scene = context.scene


        #new code
        
        bpy.ops.object.align(align_mode='OPT_1', relative_to='OPT_4', align_axis={'Y'}) 
        
        return {'FINISHED'}

class SculptView(bpy.types.Operator):
    """Sculpt View Reference Camera"""
    bl_idname = "object.sculpt_camera" 
                                     
     
    bl_label = "Sculpt Camera"
    bl_options = { 'REGISTER', 'UNDO' }
    
    def execute(self, context):

        scene = context.scene


        #new code
        
        bpy.ops.object.camera_add(
                    view_align=False,
                    enter_editmode=False,
                    location=(0, -4, 0),
                    rotation=(1.5708, 0, 0)
                    )

        context.object.name="Reference Cam" #add camera to front view
        
        bpy.context.object.data.show_passepartout = False

        #change to camera view
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                override = bpy.context.copy()
                override['area'] = area
                bpy.ops.view3d.viewnumpad(override, type = 'CAMERA')
                break # this will break the loop after the first ran
            
#            
        #bpy.ops.view3d.background_image_add()#ADD IMAGE TO BACKGROUND
        
        #bpy.context.space_data.show_background_images = True 
        
        bpy.context.scene.render.resolution_x = 1920
        bpy.context.scene.render.resolution_y = 1080
        
        
    
        
        return {'FINISHED'}

class ToggleLock(bpy.types.Operator):
    """Lock Screen"""
    bl_idname = "object.lock_screen" 
                                     
     
    bl_label = "Lock Screen Toggle"
    bl_options = { 'REGISTER', 'UNDO' }
    
    def execute(self, context):
    
        A = context.space_data.lock_camera
        B = context.space_data.show_only_render
        if A and B == True:
            context.space_data.lock_camera = False
            context.space_data.show_only_render = False
        else:
            context.space_data.lock_camera = True
            context.space_data.show_only_render = True
        return {'FINISHED'}

        

#bpy.context.space_data.show_only_render = True


        
    
    
class TestPanel(bpy.types.Panel):
    """A custom panel in the viewport toolbar"""
    bl_label = "Test Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Tests"
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        
        row.label(text="Mask Bool Ops")
        row = layout.row()
        row.operator("artist_paint.solidfy_difference", text = "Solidify Diff", icon = 'ROTACTIVE')
        row = layout.row()
        row.operator("artist_paint.solidfy_union", text = "Solidify Union", icon = 'ROTATECOLLECTION')
        row = layout.row()
        row.operator("artist_paint.reproject_mask", text = "Reproject Mask", icon = 'NODE_SEL')
        
        row = layout.row()
        row.operator("artist_paint.remove_modifiers", text = "Remove Modifiers", icon = 'RECOVER_LAST')  
        
        ########generic example#####
        row = layout.row()
        
        row.label(text="Generic Operator")
        row = layout.row()
        row.operator("object.generic_operator", text = "Generic Operator", icon = 'BLENDER')  
        
        ########sculpt camera and lock toggle#####
        box = layout.box()                        #BOOL MASK AND REUSE
        col = box.column(align = True)
        row = col.row(align = True)
        row1 = row.split(align=True)
        row1.label(text="Sculpt View")
        row1.scale_x = 0.50
        row.separator()
        row2 = row.split(align=True)
        row2.operator("object.sculpt_camera", text = "Sculpt Ref View", icon = 'RENDER_REGION')
        row2.scale_x = 1.00
        row3 = row.split(align=True)
        if context.space_data.lock_camera == True:
            row3.operator("object.lock_screen", text="", icon='LOCKED')
        if context.space_data.lock_camera == False:
            row3.operator("object.lock_screen", text="", icon='UNLOCKED')
        
        
        
        box = layout.box()                        #BOOL MASK AND REUSE
        col = box.column(align = True)
        row = col.row(align = True)
        row1 = row.split(align=True)
        row1.label(text="Bool")
        row1.scale_x = 0.50
        row.separator()
        row2 = row.split(align=True)
        row2.operator("artist_paint.solidfy_difference", text="Difference", icon = 'ROTACTIVE')
        row2.operator("artist_paint.solidfy_union", text="Union", icon = 'ROTATECOLLECTION')
        row2.scale_x = 1.00
        row.separator()
        row3 = row.split(align=True)
        row3.operator("artist_paint.reproject_mask",
                    text="Reproject", icon = 'NODE_SEL')
        row4 = row.split(align=True)
        row4.operator("artist_paint.remove_modifiers",
                    text="", icon='RECOVER_LAST')
                    
        row = layout.row()
        
        row.label(text="ALIGN PRESETS")
        box = layout.box()                        #VERTICAL ALIGN
        col = box.column(align = True)
        row = col.row(align = True)
        row1 = row.split(align=True)
        row1.label(text="VERTICAL")
        row1.scale_x = 0.50
        row.separator()
        row2 = row.split(align=False)
        row2.operator("object.align_left", text="Left", icon = 'LOOP_BACK')
        
        row2.operator("object.align_center", text="Center", icon = 'PAUSE')
        row2.scale_x = 1.00
        row.separator()
        row3 = row.split(align=True)
        row3.operator("object.align_right",
                    text="Right", icon = 'LOOP_FORWARDS')
        #row4 = row.split(align=True)
        #row4.operator("artist_paint.remove_modifiers",
                    #text="", icon='RECOVER_LAST')
        
        box = layout.box()                        #HORIZONTAL ALIGN
        col = box.column(align = True)
        row = col.row(align = True)
        row1 = row.split(align=True)
        row1.label(text="HORIZONTAL")
        row1.scale_x = 0.50
        row.separator()
        row2 = row.split(align=False)
        row2.operator("object.align_top", text="Top", icon = 'TRIA_UP')
        
        row2.operator("object.align_hcenter", text="Horizon", icon = 'GRIP')
        row2.scale_x = 1.00
        row.separator()
        row3 = row.split(align=True)
        row3.operator("object.align_bottom",
                    text="Bottom", icon = 'TRIA_DOWN')
                    
        





def register():
    bpy.utils.register_class(ReprojectMask)
    bpy.utils.register_class(SolidfyDifference)
    bpy.utils.register_class(SolidfyUnion)
    bpy.utils.register_class(RemoveMods)
    bpy.utils.register_class(GenericOper)
    bpy.utils.register_class(AlignLeft)
    bpy.utils.register_class(AlignCenter)
    bpy.utils.register_class(AlignRight)
    bpy.utils.register_class(AlignTop)
    bpy.utils.register_class(AlignHcenter)
    bpy.utils.register_class(AlignBottom)
    bpy.utils.register_class(SculptView)
    bpy.utils.register_class(ToggleLock)
    bpy.utils.register_class(TestPanel)
    
def unregister():
    bpy.utils.unregister_class(ReprojectMask)
    bpy.utils.unregister_class(SolidfyDifference)
    bpy.utils.unregister_class(SolidfyUnion)
    bpy.utils.unregister_class(RemoveMods)
    bpy.utils.unregister_class(GenericOper)
    bpy.utils.unregister_class(AlignLeft)
    bpy.utils.unregister_class(AlignCenter)
    bpy.utils.unregister_class(AlignRight)
    bpy.utils.unregister_class(AlignTop)
    bpy.utils.unregister_class(AlignHcenter)
    bpy.utils.unregister_class(AlignBottom)
    bpy.utils.unregister_class(SculptView)
    bpy.utils.unregister_class(ToggleLock)
    bpy.utils.unregister_class(TestPanel)
    
    
       
if __name__ == "__main__":
    register()

