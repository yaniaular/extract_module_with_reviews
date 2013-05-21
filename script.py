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
from subprocess import Popen

module = 'base_module_doc_rst'

print '\n\n*****************Creando registro de revisiones donde se involucre el modulo %s...' % module
os.system('echo "revno" > revno.txt')
os.system('bzr log addons/base_module_doc_rst | grep revno >> revno.txt')

print '\n\n*****************Limpiando registro...'
os.system('find revno.txt -type f -print0 | xargs -0 sed -i "s/revno: //g"')
os.system('find revno.txt -type f -print0 | xargs -0 sed -i "s/ \[merge\]//g"')

print '\n\n*****************Creando branch vacio a partir de addons...'
os.system('bzr branch addons/ %s -r 0' % (module,) )

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
os.system('bzr merge ../addons/%s/ -r %s..%s' % (module,int(invert[0])-1,int(invert[0]),))

print '\n\n*****************Limpiando commit de apoyo...'
os.system('bzr resolve %s' % module) 
os.system('bzr uncommit --force')
os.system('bzr rm ci.txt')
os.system('bzr ci -m """[MERGE] from openobject-addons 6.1 revno %s"""' % int(invert[0]) )
invert.remove( invert[0] ) 

print '\n\n*****************Realizando merges restantes...'
for rev in invert:
    print '\n******************************************\n'
    os.system('bzr merge ../addons/%s/ -r %s..%s' % (module,int(rev)-1,int(rev),))
    os.system('bzr resolve %s' % module) 
    os.system('bzr ci -m """[MERGE] from openobject-addons 6.1 revno %s"""' % rev )

print '\n\n*****************Finalizando...'
os.system('rm ../revno.txt')

print '\n\n*****************Branch con modulo %s y sus revisiones fueron creadas correctamente!' % module 
