#          DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 1, June 2013
#
#Copyright (C) 2013 Yanina Aular 
#
#Everyone is permitted to copy and distribute verbatim or modified
#copies of this license document, and changing it is allowed as long
#as the name is changed.
#
#          DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#0. You just DO WHAT THE FUCK YOU WANT TO.

#This code creates a branch of a module with your reviews 
#extracting from the addons.

import os
import csv
import argparse
from subprocess import Popen

def argument_parser():
    """
    This function create the help command line and manage and filter the
    parameters of this program (default values, choices values)
    """
    parser = argparse.ArgumentParser(
        prog='script',
        description='Extact a module revision from a branch.',
        epilog="""

This program will create a new branch that containg only the
directory of the module indicate in the cli arguments and will be
containg only the revision associated to that module (Extract module
from a branch with its revisions). You can find this new branch
directory at the same directory you use to run the script 

To run do this Example:

    python script mrp_button_box -a 7.0-addons-vauxoo/

If you want to use this script whatevere place you are you can edit
your ~.bash_aliases file and add the alias

    alias my_tool = "python/<your-path-to>/script.py"

Openerp Developer Comunity Tool
Development by Vauxoo Team (lp:~vauxoo)
Coded by Yanina Aular <yani@vauxoo.com>.
Source code at lp:~yanina-aular/+junk/extraer_modulo_con_revisiones/
""",
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        'name',
        metavar='MODULE_NAME',
        type=str,
        help='name of the module to separate.')

    parser.add_argument(
        '-a', '--addon_path',
        metavar='ADDONS FOLDER NAME',
        type=str,
        help='name of the branch where to be straxct module.',
        required=True)

    return parser.parse_args()

args = argument_parser()
module, addon_path = (args.name, args.addon_path)

print 'script configuration'
print 'module     =', module
print 'addon_path =', addon_path


print '\n\n*****************Creando registro de revisiones donde se involucre el modulo %s...' % module
os.system('echo "revno" > revno.txt')
os.system('bzr log %s/%s | grep revno >> revno.txt' % (addon_path, module))

print '\n\n*****************Limpiando registro revno.txt...'
os.system('find revno.txt -type f -print0 | xargs -0 sed -i "s/revno: //g"')
os.system('find revno.txt -type f -print0 | xargs -0 sed -i "s/ \[merge\]//g"')

print '\n\n*****************Creando branch vacio a partir de addon path...'
os.system('bzr branch %s/ %s -r 0' % (addon_path, module) )

print '\n\n*****************Registrando commit inicial para poder hacer merge la primera vez...'
os.chdir(module)
os.system('touch ci.txt')
os.system('bzr add')
os.system('bzr ci -m """main"""')

print '\n\n*****************Leyendo registro de branches donde se involucra el modulo %s...' % module
archivo = csv.DictReader(open('../revno.txt'))

print '\n\n*****************Preparando lista de revisiones...'
invert = []
for line in archivo:
    invert.append(line.get('revno'))
invert.reverse()

print '\n\n*****************Realizando primer merge...'
os.system('bzr merge ../%s/%s/ -r %s..%s' % (addon_path, module,int(invert[0])-1,int(invert[0]),))

print '\n\n*****************Limpiando commit de apoyo...'
os.system('bzr resolve %s' % module) 
os.system('bzr uncommit --force')
os.system('bzr rm ci.txt')
os.system('bzr ci -m """[MERGE] from something revno %s"""' % int(invert[0]) )
invert.remove( invert[0] ) 

print '\n\n*****************Realizando merges restantes...'
for rev in invert:
    print '\n******************************************\n'
    os.system('bzr merge ../%s/%s/ -r %s..%s' % (addon_path,module,int(rev)-1,int(rev),))
    os.system('bzr resolve %s' % module) 
    os.system('bzr ci -m """[MERGE] from something-addons revno %s"""' % rev )

print '\n\n*****************Finalizando...'
os.system('rm ../revno.txt')

print '\n\n*****************Branch con modulo %s y sus revisiones fueron creadas correctamente!' % module 
