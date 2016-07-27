import bpy

class ReprojectMask(bpy.types.Operator):
    """Reproject Mask"""
    bl_idname = "object.reproject_mask" 
                                     
     
    bl_label = "Reproject Mask by View"
    bl_options = { 'REGISTER', 'UNDO' }
    
    def execute(self, context):

        scene = context.scene


        #new code
        bpy.ops.object.editmode_toggle() #toggle edit mode
        bpy.ops.uv.project_from_view(camera_bounds=True, correct_aspect=False, scale_to_bounds=False) #project from view
        bpy.ops.object.editmode_toggle() #toggle back from edit mode
        bpy.ops.paint.texture_paint_toggle() #toggle texpaint
        return {'FINISHED'}
    
#next operator
class SolidfyDifference(bpy.types.Operator):
    """Solidify and Difference Mask"""
    bl_idname = "object.solidfy_difference"
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
            bpy.ops.mesh.dissolve_faces()
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
    bl_idname = "object.solidfy_union"
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
            bpy.ops.mesh.dissolve_faces()
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
    bl_idname = "object.remove_modifiers"
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
        bpy.context.object.draw_type = 'SOLID'

        
                
            
        return {'FINISHED'}




        
    
    
class TestPanel(bpy.types.Panel):
    """A custom panel in the viewport toolbar"""
    bl_label = "Test Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Tests"
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        
        row.label(text="Test Panel")
        
        row = layout.row()
        row.operator("object.reproject_mask", text = "Reproject Mask", icon = 'NODE_SEL')
        row = layout.row()
        row.operator("object.solidfy_difference", text = "Solidify Diff", icon = 'ROTACTIVE')
        row = layout.row()
        row.operator("object.solidfy_union", text = "Solidify Union", icon = 'ROTATECOLLECTION')
        row = layout.row()
        row.operator("object.remove_modifiers", text = "Remove Modifiers", icon = 'RECOVER_LAST')    





def register():
    bpy.utils.register_class(ReprojectMask)
    bpy.utils.register_class(SolidfyDifference)
    bpy.utils.register_class(SolidfyUnion)
    bpy.utils.register_class(RemoveMods)
    bpy.utils.register_class(TestPanel)
    
def unregister():
    bpy.utils.unregister_class(ReprojectMask)
    bpy.utils.unregister_class(SolidfyDifference)
    bpy.utils.unregister_class(SolidfyUnion)
    bpy.utils.unregister_class(RemoveMods)
    bpy.utils.unregister_class(TestPanel)
    
    
       
if __name__ == "__main__":
    register()

