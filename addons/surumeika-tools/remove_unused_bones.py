import bpy

class TOOLS_OT_RemoveUnusedBones(bpy.types.Operator):
    bl_idname = "object.tools_remove_unused_bones"
    bl_label = "Remove Unused Bones"
    bl_description = "Remove Unused Bones"
    bl_options = {"REGISTER", "UNDO"}

    def get_children_bones_name(self, bone: bpy.types.Object):
        if (bone.parent == None):
            return [bone.name]
        childrens_name = [bone.name]
        childrens = [bone]
        while (childrens[-1].parent != None):
            childrens_name.append(childrens[-1].parent.name)
            childrens.append(childrens[-1].parent)
        return childrens_name

    # When Exec menu
    def execute(self, context):
        armature_obj = context.active_object
        bones_name_set = set()
        for obj in context.selected_objects:
            if obj.vertex_groups is not None:
                for vg in obj.vertex_groups:
                    bones_name_set.add(vg.name)
        bones_set = set()
        for bone in bones_name_set:
            bones_set |= set(self.get_children_bones_name(armature_obj.data.bones[bone]))
        for bone in armature_obj.data.edit_bones:
            if bone.name not in bones_set:
                armature_obj.data.edit_bones.remove(bone)
        return {"FINISHED"}
