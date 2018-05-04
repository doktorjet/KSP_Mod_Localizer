# KSP AutoLoc 0.2
#
# This script is meant to replace boring manual text replacement tasks
# for implementing localization to non-localized-yet part mods in KSP 1.3+
#
# Beware, it does not use KSP API for clean node processing, so it may produce errors.
# Beware, it definitely WILL produce errors if you have:
# 1) Any .cfg files with MORE THAN ONE PART in them.
# 2) More than one single agency in /Agencies/Agents.cfg
#
# Also it will NOT localize ModuleManager patches, GUI commands or science definitions - you should do them manually.

import sys
import os
agency = False

# Fail function
def kaput(p):
    print p
    try:
        input("Press enter to continue")
    except SyntaxError:
        pass
    sys.exit(0)
        
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

print('***  KSP Automatic Localizer 0.2 ***')	
	
# Aquiring mod folder from command line parameter
if len(sys.argv)>1:
    pdir = sys.argv[1]
else:
    kaput('You are supposed to supply a path to mod folder as a command line parameter.')

if not os.path.isdir(pdir):
    kaput('Your input is: '+pdir+'.\nIt is vot a valid folder.\nYou are supposed to supply a path to mod folder as a command line parameter.')
 
# Reading mod name (equals to folder name as in CKAN)
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
    kaput('Localization file already exists! Stopping execution to prevent string damage!')

else:
    print('Localization file not found. Creating!')
floc = open(pdir+'\Localization\en-us.cfg','w+')
floc.write("Localization\n{\nen-us\n{\n")

# Check if we have an agency. If we do, we'll treat it as the only one!
# And will also use it's title for all parts 'manufacturer' property.

if filecheck(pdir+'\Agencies\Agents.cfg','AGENT'):
    floc.write('// Agencies\n\n')
    cfg = cfgread(pdir+'\Agencies\Agents.cfg')
    agency = True
    if not cfg[1]:
        print ('Found an agency, but it does not have a title, which is a severe bug. Fixing by assigning a title equal to it\'s name: '+ cfg[0])
        cfg[1] = cfg[0]
        ReplaceLineInFile(pdir+'\Agencies\Agents.cfg',cfg[4],'title = #LOC_'+modname+'_Agency_title\ndescription = #LOC_'+modname+'_Agency_desc\n')
    else:
        print ('Found an agency, named '+cfg[1]+'. Using it as the one and only part manufacturer.')
        ReplaceLineInFile(pdir+'\Agencies\Agents.cfg',cfg[3],'title = #LOC_'+modname+'_Agency_title\n')
        ReplaceLineInFile(pdir+'\Agencies\Agents.cfg',cfg[4],'description = #LOC_'+modname+'_Agency_desc\n')
    floc.write('#LOC_'+modname+'_Agency_title = '+cfg[1]+'\n')
    floc.write('#LOC_'+modname+'_Agency_desc = '+cfg[2]+'\n')


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
               floc.write('#LOC_'+modname+'_'+cfg[0]+'_desc = '+cfg[2]+'\n\n')
               ReplaceLineInFile(path+'\\'+fname,cfg[3],'title\t\t\t= #LOC_'+modname+'_'+cfg[0]+'_title\n')
               ReplaceLineInFile(path+'\\'+fname,cfg[4],'description\t\t= #LOC_'+modname+'_'+cfg[0]+'_desc\n')
               if agency:
                   ReplaceLineInFile(path+'\\'+fname,cfg[5],'manufacturer\t= #LOC_'+modname+'_Agency_title\n')
# Close en-us.cfg, we're done with it.
floc.write('}\n}')
floc.close()
kaput('We are done here! Check your newly localized mod for bugs!')
