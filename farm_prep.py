#Lines 4 to 59 is in ArcMap
#Lines 67 to the end is in QGIS

import arcpy
arcpy.env.workspace=r"C:\Users\leighton\OneDrive\Documents\farm data\Chief Surveyor General Cadastral April 2022\WC - NC - EC\WC - NC - EC\CADC\WC\Arcpy test"

#--------------- Step 3: Add new field to farm shapefile called "Farm"

arcpy.AddField_management("WC_Parent_Farm","Farm","TEXT")
print "!!!!!!! Step 3 DONE: The new field called Farm has been added !!!!!!!"

#--------------- Step 4: Copy TAG VALUE field to the new field called Farm.

arcpy.CalculateField_management(in_table="WC_Parent_Farm", field="Farm", expression="[TAG_VALUE]", expression_type="VB", code_block="")
print "!!!!!!! Step 4 DONE: TAG_VALUE has been copied to the Farm field !!!!!!!"

#--------------- Step 5: Replace farm names to proper case using in field calculator !Farm!.title()

arcpy.CalculateField_management(in_table="WC_Parent_Farm", field="Farm", expression="!Farm!.title() ", expression_type="PYTHON_9.3", code_block="")
print "!!!!!!! Step 5 DONE: Farm fields has been changed to proper case !!!!!!!"


#--------------- Step 6: Replace spaces with a comma (,) using !Farm!.replace(" ", ",")

arcpy.CalculateField_management(in_table="WC_Parent_Farm", field="Farm", expression='!Farm!.replace(" ", ",")', expression_type="PYTHON_9.3", code_block="")
print "!!!!!!! Step 6 DONE: Farm fields spaces has been replaced with comma !!!!!!!"

#--------------- Step 7: Replace hyphen (-) with number sign (#) using !Farm!.replace("-", "#")

arcpy.CalculateField_management(in_table="WC_Parent_Farm", field="Farm", expression='!Farm!.replace("-", "#")', expression_type="PYTHON_9.3", code_block="")
print "!!!!!!! Step 7 DONE: Farm fields hyphen (-) has been replaced with number sign (#) !!!!!!!"

#--------------- Step 8: Add a new field called Farm_Name (to remove number in Farm field)

arcpy.AddField_management("WC_Parent_Farm","Farm_Name","TEXT")
print "!!!!!!! Step 8 DONE: A new field called Farm_Name has been added !!!!!!!"

#--------------- Step 9: Copy Farm to Farm_Name without the parcel numbers at the end of the farm names

arcpy.CalculateField_management(in_table="WC_Parent_Farm", field="Farm_Name", expression="conv( !Farm! )",
expression_type="PYTHON_9.3",
code_block="def conv(myword):\n    mysting=''\n    for chr in myword:\n        if not((ord(chr) >= 48 and ord(chr) <= 57) or ord(chr) == 47 or ord(chr) == 32 or ord(chr) == 45):\n            mysting = mysting + chr\n    return mysting")
print "!!!!!!! Step 9 DONE: Farm names without numbers has been copied to new field Farm_Name !!!!!!!"

#--------------- Step 10: Replace "No." with blank: !Farm_Name!.replace("No.", "")

arcpy.CalculateField_management(in_table="WC_Parent_Farm", field="Farm_Name", expression='!Farm_Name!.replace("No.", "")', expression_type="PYTHON_9.3", code_block="")
print "!!!!!!! Step 10 DONE: Farm names with 'No.' in the name has been replaced with blank !!!!!!!"

#--------------- Step 11: Replace comma back to spaces using !Farm_Name!.replace(",", " ")

arcpy.CalculateField_management(in_table="WC_Parent_Farm", field="Farm_Name", expression='!Farm_Name!.replace(",", " ")', expression_type="PYTHON_9.3", code_block="")
print "!!!!!!! Step 11 DONE: Farm names with with comma's has be replaced back with spaces !!!!!!!"

#--------------- Step 12. Replace hyphen (-) back using !Farm_Name!.replace("#", "-")

arcpy.CalculateField_management(in_table="WC_Parent_Farm", field="Farm_Name", expression='!Farm_Name!.replace("#", "-")', expression_type="PYTHON_9.3", code_block="")
print "!!!!!!! Step 12 DONE: Farm names with # for hyphen has been changed back !!!!!!!"



#*************************************** NEXT STEPS ARE IN QGIS **************************************************************

#------- load farm layer and generate centroids

fn = "C:/Users/leighton/OneDrive/Documents/farm data/Chief Surveyor General Cadastral April 2022/\
WC - NC - EC/WC - NC - EC/CADC/WC/Arcpy test/WC_Parent_Farm.shp"

vlayer = iface.addVectorLayer(fn, '', 'ogr')

import processing
processing.run("native:centroids",{'INPUT':'C:/Users/leighton/OneDrive/Documents/farm data/\
Chief Surveyor General Cadastral April 2022/WC - NC - EC/WC - NC - EC/CADC/WC/Arcpy test/\
WC_Parent_Farm.shp','ALL_PARTS':False,
'OUTPUT':'C:/Users/leighton/OneDrive/Documents/farm data/Chief Surveyor General Cadastral April 2022/\
WC - NC - EC/WC - NC - EC/CADC/WC/Arcpy test/WC_Parent_Farm_Cent.shp'})

fn2 = "C:/Users/leighton/OneDrive/Documents/farm data/\
Chief Surveyor General Cadastral April 2022/\
WC - NC - EC/WC - NC - EC/CADC/WC/Arcpy test/WC_Parent_Farm_Cent.shp"

vlayer2 = iface.addVectorLayer(fn2, '', 'ogr')

#--------------- Step 13: Export centroid layer with new name


layers = QgsProject.instance().mapLayersByName('WC_Parent_Farm_Cent2')
layer = layers[0]

#output shapefile
fn_ex = 'C:/Users/leighton/OneDrive/Documents/farm data/\
Chief Surveyor General Cadastral April 2022/\
WC - NC - EC/WC - NC - EC/CADC/WC/Arcpy test/WC_Farms.shp'

writer = QgsVectorFileWriter.writeAsVectorFormat(layer, fn_ex, 'utf-8', \
driverName='ESRI Shapefile')

new_layer = iface.addVectorLayer(fn_ex, '', 'ogr')

del(writer)

#  Add new fields

fn = "C:/Users/leighton/OneDrive/Documents/farm data/\
Chief Surveyor General Cadastral April 2022/\
WC - NC - EC/WC - NC - EC/CADC/WC/Arcpy test/WC_Farms.shp"

layer = iface.addVectorLayer(fn, '', 'ogr')
print (layer.fields().names())

layer_provider = layer.dataProvider()
layer_provider.addAttributes([QgsField('name', QVariant.String), QgsField('category_id', QVariant.Int)])
layer.updateFields
print(layer.fields().names())

#  Copy Farm_Name to name field. Set "category_id" = 95

expression1 = QgsExpression('Farm_Name')
expression2 = QgsExpression('95')

context = QgsExpressionContext()
context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer))

with edit(layer):
    for f in layer.getFeatures():
        context.setFeature(f)
        f['name'] = expression1.evaluate(context)
        layer.updateFeature(f)
        f['category_i'] = expression2.evaluate(context)
        layer.updateFeature(f)

#   Remove all fields except, t4a_name and category_id.

layer_provider = layer.dataProvider()
layer_provider.deleteAttributes([1,2,3,4,5]) #check this
layer.updateFields

root = QgsProject.instance().layerTreeRoot() #remove layer
layer = QgsProject.instance().mapLayersByName('WC_Farms')[0]
root.removeLayer(layer)


fn = "C:/Users/leighton/OneDrive/Documents/farm data/\
Chief Surveyor General Cadastral April 2022/\
WC - NC - EC/WC - NC - EC/CADC/WC/Arcpy test/WC_Farms.shp"
layer = iface.addVectorLayer(fn, '', 'ogr') #add layer again for changes to reflect
