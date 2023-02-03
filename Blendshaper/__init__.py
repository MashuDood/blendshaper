bl_info = {
	"name": "Blendshaper",
	"author": "Mashu & OpenAI",
	"version": (1, 8),
	"blender": (3, 41, 0),
	"location": "View3D > Toolbar",
	"description": "A Blender Addon for creating blendshapes and mirroring shapes",
	"category": "Object"
}

import bpy

shape_keys = [
	"BrowInnerUp",
	"BrowDownLeft",
	"BrowDownRight",
	"BrowOuterUpLeft",
	"BrowOuterUpRight",
	"EyeLookUpLeft",
	"EyeLookUpRight",
	"EyeLookDownLeft",
	"EyeLookDownRight",
	"EyeLookInLeft",
	"EyeLookInRight",
	"EyeLookOutLeft",
	"EyeLookOutRight",
	"EyeBlinkLeft",
	"EyeBlinkRight",
	"EyeSquintRight",
	"EyeSquintLeft",
	"EyeWideLeft",
	"EyeWideRight",
	"CheekPuff",
	"CheekSquintLeft",
	"CheekSquintRight",
	"NoseSneerLeft",
	"NoseSneerRight",
	"JawOpen",
	"JawForward",
	"JawLeft",
	"JawRight",
	"MouthFunnel",
	"MouthPucker",
	"MouthLeft",
	"MouthRight",
	"MouthRollUpper",
	"MouthRollLower",
	"MouthShrugUpper",
	"MouthShrugLower",
	"MouthClose",
	"MouthSmileLeft",
	"MouthSmileRight",
	"MouthFrownLeft",
	"MouthFrownRight",
	"MouthDimpleLeft",
	"MouthDimpleRight",
	"MouthUpperUpLeft",
	"MouthUpperUpRight",
	"MouthLowerDownLeft",
	"MouthLowerDownRight",
	"MouthPressLeft",
	"MouthPressRight",
	"MouthStretchLeft",
	"MouthStretchRight",
	"TongueOut"
]

class CreateBlendshapesOperator(bpy.types.Operator):
	bl_idname = "object.create_blendshapes"
	bl_label = "Create Blendshapes"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		obj = bpy.context.active_object
		basis = obj.shape_key_add(name='Basis')

		for shape_key_name in shape_keys:
			obj.shape_key_add(name=shape_key_name)

		return {'FINISHED'}

class CopyData(bpy.types.Operator):
	"""Copy to Mirror"""
	bl_idname = "object.copy_data"
	bl_label = "Copy to Mirror"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		obj = bpy.context.object

		for shape_key in obj.data.shape_keys.key_blocks:
			if shape_key.name.endswith("Left"):
				right_key = obj.data.shape_keys.key_blocks.get(shape_key.name.replace("Left", "Right"))
				if right_key:
					for i in range(len(shape_key.data)):
						right_key.data[i].co = shape_key.data[i].co.copy()
		return {'FINISHED'}


class MirrorShape(bpy.types.Operator):
	"""Mirror Shape"""
	bl_idname = "object.mirror_shape"
	bl_label = "Mirror Shape"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		obj = bpy.context.object
		obj.data.shape_keys.key_blocks[obj.active_shape_key_index].value = 1
		bpy.ops.object.shape_key_mirror(use_topology=False)

		return {'FINISHED'}

class BlendshaperPanel(bpy.types.Panel):
	"""Blendshaper Panel"""
	bl_label = "Blendshaper"
	bl_idname = "OBJECT_PT_blendshaper"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_category = "Blendshaper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.operator("object.create_blendshapes", text="Create Blendshapes")
		row = layout.row()
		row.operator("object.copy_data", text="Copy to Mirror")
		row = layout.row()
		row.operator("object.mirror_shape", text="Mirror Shape")

def register():
	bpy.utils.register_class(CreateBlendshapesOperator)
	bpy.utils.register_class(CopyData)
	bpy.utils.register_class(MirrorShape)
	bpy.utils.register_class(BlendshaperPanel)

def unregister():
	bpy.utils.unregister_class(CreateBlendshapesOperator)
	bpy.utils.unregister_class(CopyData)
	bpy.utils.unregister_class(MirrorShape)
	bpy.utils.unregister_class(BlendshaperPanel)

if __name__ == "__main__":
	register()

