bl_info = {
    "name": "Meika's Tools Addon",
    "author": "surumeika1987",
    "version": (0, 0, 1),
    "blender": (4, 3, 2),
    "location": "",
    "description": "Useful Tools by surumeika1987",
    "warning": "This is Test Addon",
    "support": "TESTING",
    "doc_url": "",
    "tracker_url": "",
    "category": "Object"
}

if "bpy" in locals():
    import imp
    imp.reload(cleanup_unused_weights)
    imp.reload(remove_unused_bones)
else:
    from . import cleanup_unused_weights
    from . import remove_unused_bones

import bpy
    
def menu_fn1(self, context):
    self.layout.separator()
    self.layout.operator(remove_unused_bones.TOOLS_OT_RemoveUnusedBones.bl_idname)

def menu_fn2(self, context):
    self.layout.separator()
    self.layout.operator(cleanup_unused_weights.TOOLS_OT_CleanupUnusedWeights.bl_idname)

classes = [
    remove_unused_bones.TOOLS_OT_RemoveUnusedBones,
    cleanup_unused_weights.TOOLS_OT_CleanupUnusedWeights,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.VIEW3D_MT_edit_armature_delete.append(menu_fn1)
    bpy.types.VIEW3D_MT_object_cleanup.append(menu_fn2)
    print("Enable Meika's Tools Addon.")

def unregister():
    bpy.types.VIEW3D_MT_edit_armature_delete.remove(menu_fn1)
    bpy.types.VIEW3D_MT_object_cleanup.append(menu_fn2)
    for c in classes:
        bpy.utils.unregister_class(c)
    print("Disable Meika's Tools Addon.")

if __name__ == "__main__":
    register()