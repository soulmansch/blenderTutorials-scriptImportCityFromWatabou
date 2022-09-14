import bpy;
import json;

# Open THE JSON file
f = open('LINK_OF_THE_JSON_FILE.json')
data = json.load(f)
f.close()

scaleDown = 100

#clear the scene
for collection in bpy.data.collections:
    bpy.data.collections.remove(collection)
    
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.ops.outliner.orphans_purge()
bpy.ops.outliner.orphans_purge()
bpy.ops.outliner.orphans_purge()


#add objects and collections
for item in data['features']:
    if item["id"] != "values" and item["id"] != "prisms":
        new_mesh = bpy.data.meshes.new(item["id"])
        new_object = bpy.data.objects.new(item["id"], new_mesh)
        new_collection = bpy.data.collections.new(item["id"])
        bpy.context.scene.collection.children.link(new_collection)
        new_collection.objects.link(new_object)
        
        verts =[]
        edges = []
        faces = []
        vertsIndeces = 0
        if item["type"] == "MultiPolygon":
            for itemData in item["coordinates"]:
                newFace = []
                for coords in itemData[0]:
                    verts.append([coords[0]/scaleDown,coords[1]/scaleDown,0])
                    newFace.append(vertsIndeces)
                    vertsIndeces +=1
                faces.append(newFace)

        elif item["type"] == "Polygon":
            newFace = []
            for coords in item["coordinates"][0]:
                verts.append([coords[0]/scaleDown,coords[1]/scaleDown,0])
                newFace.append(vertsIndeces)
                vertsIndeces +=1
            faces.append(newFace)
        elif item["type"] == "GeometryCollection":
#            newArrayOfVertsForEdges = []
            for geometry in item["geometries"]:
                newArrayOfVerts = []
                if geometry["type"]=="LineString":
                    for coords in geometry["coordinates"]:
                        verts.append([coords[0]/scaleDown,coords[1]/scaleDown,0])
                        newArrayOfVerts.append(len(verts)-1)
                    
                    for index, itemCoord in enumerate(newArrayOfVerts):
                        if index < len(newArrayOfVerts)-1:
                            edges.append([newArrayOfVerts[index],newArrayOfVerts[index+1]])
#                  
                elif geometry["type"]=="Polygon":
                    newFace = []
                    for coords in geometry["coordinates"][0]:
                        verts.append([coords[0]/scaleDown,coords[1]/scaleDown,0])
                        newFace.append(vertsIndeces)
                        vertsIndeces +=1
                    faces.append(newFace)
                
                                
            
        
        
        new_mesh.from_pydata(verts, edges, faces)
        new_mesh.update()
                    
                    
