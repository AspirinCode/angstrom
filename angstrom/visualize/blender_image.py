"""
--- Ångström ---
Render image of a molecule file using Blender.
"""
import pickle
import bpy
import sys


def render_pdb(settings):
    """
    Render pdb file using Blender pdb reader.
    """
    # Delete the cube
    bpy.ops.object.delete(use_global=False)
    # bpy.ops.import_mesh.pdb(filepath=pdb_file)
    bpy.ops.import_mesh.pdb(**settings['pdb'])

    if settings['colors'] is not None:
        # Find intersection of atoms of the molecule and atoms that have color defined
        for atom in set(settings['colors'].keys()).intersection(bpy.data.materials.keys()):
            bpy.data.materials[atom].diffuse_color = settings['colors'][atom]

    # Make materials shiny (mirror)
    # for Item in bpy.data.materials:
    #     Item.raytrace_mirror.use = True
    #     Item.raytrace_mirror.reflect_factor = 0.1

    # Move Camera and set rotation to normal
    bpy.data.objects['Camera'].location = settings['camera']['location']
    bpy.data.objects['Camera'].rotation_euler = settings['camera']['rotation']
    bpy.data.objects['Camera'].data.type = settings['camera']['type']
    if settings['camera']['type'] == 'ORTHO':
        bpy.data.objects['Camera'].data.ortho_scale = settings['camera']['zoom']
    elif settings['camera']['type'] == 'PERSP':
        bpy.data.objects['Camera'].data.lens = settings['camera']['zoom']

    bpy.data.objects['Lamp'].location = settings['camera']['location']
    bpy.data.objects['Lamp'].rotation_euler = [0, 0, 0]
    bpy.data.objects['Lamp'].data.energy = settings['lamp']

    # Set render x resolution lower (compress screen in x direction)
    bpy.context.scene.render.resolution_x = settings['resolution'][0]
    bpy.context.scene.render.resolution_y = settings['resolution'][1]
    bpy.context.scene.render.resolution_percentage = 100

    # Turn off sky/background
    bpy.context.scene.render.layers["RenderLayer"].use_sky = False
    # Turn on environmental lighting
    bpy.context.scene.world.light_settings.use_environment_light = True
    bpy.context.scene.world.light_settings.environment_energy = settings['brightness']
    # Save .blend file
    if settings['save'] != '':
        bpy.ops.wm.save_as_mainfile(filepath=settings['save'])
    if settings['render']:
        # Set the output file and name it!
        bpy.data.scenes['Scene'].render.filepath = settings['output']
        # Render
        bpy.ops.render.render(write_still=True)


if __name__ == '__main__':
    argv = sys.argv[sys.argv.index("--") + 1:]  # get all args after "--"
    with open(argv[0], 'rb') as handle:
        settings = pickle.load(handle)
    print(settings)
    render_pdb(settings)