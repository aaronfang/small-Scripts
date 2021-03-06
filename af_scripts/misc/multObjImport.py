import maya.cmds as cmds
def multObjImport():
    files_to_import = cmds.fileDialog2(fileFilter =  '*.obj', dialogStyle = 2, caption = 'import multiple object files', fileMode = 4)
    for file_to_import in files_to_import:
        names_list  = file_to_import.split('/')
        object_name = names_list[-1].replace('.obj', '') 
        returnedNodes = cmds.file('%s' % file_to_import, i = True, type = "OBJ", rnn=True, ignoreVersion = True, options = "mo=0",  loadReferenceDepth  = "all"  )
        cmds.rename( returnedNodes[0], object_name)
        for nd in returnedNodes:
			if '|' in nd and 'Shape' not in nd:
				cmds.rename(nd, object_name)
multObjImport()
