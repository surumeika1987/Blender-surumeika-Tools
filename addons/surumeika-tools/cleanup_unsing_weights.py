import bpy

class TOOLS_OT_CleanupUnusingWeights(bpy.types.Operator):
    bl_idname = "object.tools_cleanup_unusing_weights"
    bl_label = "Remove Unuse Weights"
    bl_description = "Remove Unusing Weights"
    bl_options = {"REGISTER", "UNDO"}

    def survey(self, obj):
        maxWeight = {}
        nameByIndex = {}
        indexByName = {}
        for vg in obj.vertex_groups:
            maxWeight[vg.index] = 0
            nameByIndex[vg.index] = vg.name
            indexByName[vg.name] = vg.index
        for v in obj.data.vertices:
            for g in v.groups:
                gn = g.group
                w = obj.vertex_groups[g.group].weight(v.index)
                if (maxWeight.get(gn) is None or w > maxWeight[gn]):
                    maxWeight[gn] = w
        return maxWeight, nameByIndex, indexByName
    
    mirroredNameMap = {"L": "R", "R":"L", "l": "r", "r": "l"}
    def getMirroredName(self, name):
        prefix = self.mirroredNameMap.get(name[-1])
        return name[0:-1]+prefix if prefix is not None else name

    def execute(self, context):
        obj = context.active_object
        maxWeight, nameByIndex, indexByName = self.survey(obj)
        print(indexByName)
        ka = []
        ka.extend(maxWeight.keys())
        ka.sort(key=lambda gn: -gn)
        removalFlags = {}
        for gn in ka:
            if removalFlags.get(gn) is not None:
                continue
            removalFlags[gn] = maxWeight[gn] <= 0
            group_name = nameByIndex[gn]
            mirror = self.getMirroredName(group_name)
            mirror_index = indexByName.get(mirror)
            if mirror_index is not None:
                if removalFlags.get(mirror_index) is None:
                    removalFlags[gn] = maxWeight[gn] <= 0
                if maxWeight[gn] > 0 or maxWeight[mirror_index] > 0:
                    removalFlags[gn] = removalFlags[mirror_index] = False
            else:
                removalFlags[gn] = maxWeight[gn] <= 0
        for gn in ka:
            if removalFlags[gn]:
                obj.vertex_groups.remove(obj.vertex_groups[gn])
                print ("deleted: "+nameByIndex[gn])
        return {"FINISHED"}
