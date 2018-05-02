# KSP AutoLoc 0.1
#
# This script is meant to replace boring manual text replacement tasks
# for implementing localization to non-localized-yet part mods in KSP 1.3+
#
# Beware, it does not use KSP API for clean node processing, so it may produce errors.
# Beware, it definitely WILL produce errors if you have:
# 1) Any .cfg files with MORE THAN ONE PART in them.
# 2) More than one single agency in /Agencies/Agents.cfg
#
# Also it will NOT localize ModuleManager patches - you should do it manually.


# Open this script in Python editor,
# than change pdir value for where your mod is,
# than run ther script.

pdir = 'c:\Games\KSPx64_dev\GameData\CONTARES'

import os
agency = False
print('***  KSP Automatic Localizer 0.1 ***')

# Line replacer function
def ReplaceLineInFile(fileName, sourceText, replaceText):
    file = open(fileName, 'r')
    text = file.read()
    file.close()
    file = open(fileName, 'w')
    file.write(text.replace(sourceText, replaceText, 1))
    file.close()

# Check-if-cfg-is-part-cfg function
def filecheck(ff,ss):
    fh = open(ff)
    for line in fh:
        if line.startswith(ss):
            fh.close()
            return 1
    fh.close()
    return 0

# CFG reader function
def cfgread(ff):
    cr = ['','','','','','']
    with open(ff) as fh:
        for line in fh:
            if 'name' in line:
                if not cr[0]:
                    cr[0] = line.rpartition('=')[2].strip()
            elif 'title' in line:
                if not cr[1]:
                    cr[1] = line.rpartition('=')[2].strip()
                    cr[3]=line
            elif 'description' in line:
                if not cr[2]:
                    cr[2] = line.rpartition('=')[2].strip()
                    cr[4]=line
            elif 'manufacturer' in line:
                cr[5]=line
    return(cr)

# Reading mod name (equals to folder name)
modname = pdir.rpartition("\\")[2]
print ('Processing the '+modname+' mod...')
l = len(pdir)+1
pstring = ''

# Localization checks

if not os.path.isdir(pdir+'\Localization'):
    print('Localization folder not found! Creating!')
    os.makedirs(pdir+'\Localization')

# Check if basic en-us localization is there already.
# Repetitive execution while having that file will definitely ruin the strings, so we'll stop instead.
if os.path.isfile(pdir+'\Localization\en-us.cfg'):
    print('Localization file already exists! Stopping execution to prevent string damage!')
    quit()
else:
    print('Localization file not found. Creating it!')
floc = open(pdir+'\Localization\en-us.cfg','w+')
floc.write("Localization\n{\nen-us\n{\n")

# Check if we have an agency. If we do, we'll treat it as the only one!
# And will also use it's title for all parts 'manufacturer' property.

if os.path.isfile(pdir+'\Agencies\Agents.cfg'):
    floc.write('// Agencies\n\n')
    cfg = cfgread(pdir+'\Agencies\Agents.cfg')
    agency = True
    print ('Found an agency, named '+cfg[1]+'. Using it as the one and only part manufacturer.')
    floc.write('#LOC_'+modname+'_Agency_title = '+cfg[1]+'\n')
    floc.write('#LOC_'+modname+'_Agency_desc = '+cfg[2]+'\n')
    ReplaceLineInFile(pdir+'\Agencies\Agents.cfg',cfg[3],'title = #LOC_'+modname+'_Agency_title\n')
    ReplaceLineInFile(pdir+'\Agencies\Agents.cfg',cfg[4],'title = #LOC_'+modname+'_Agency_desc\n')


# Dir walk and parts writing.

for path, dirs, files in os.walk(pdir):
   for fname in files:
       if fname.endswith('cfg'):
           if filecheck(path+'\\'+fname,'PART'):
               if pstring != path[l:]:
                   pstring = path[l:]
                   print ('Processing '+pstring+' folder...')
                   floc.write('\n// '+pstring+'\n\n')
               cfg = cfgread(path+'\\'+fname)
               floc.write('#LOC_'+modname+'_'+cfg[0]+'_title = '+cfg[1]+'\n')
               floc.write('#LOC_'+modname+'_'+cfg[0]+'_desc = '+cfg[2]+'\n')
               ReplaceLineInFile(path+'\\'+fname,cfg[3],'title\t\t\t= #LOC_'+modname+'_'+cfg[0]+'_title\n')
               ReplaceLineInFile(path+'\\'+fname,cfg[4],'description\t\t= #LOC_'+modname+'_'+cfg[0]+'_desc\n')
               if agency:
                   ReplaceLineInFile(path+'\\'+fname,cfg[5],'manufacturer\t= #LOC_'+modname+'_Agency_title\n')
# Close en-us.cfg, we're done with it.
floc.write('}\n}')
floc.close()
print('Done.\n')
