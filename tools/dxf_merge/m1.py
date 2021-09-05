#!/opt/local/bin/python3.8
# ... !/usr/bin/env python37

#pip3 install ezdxf

import ezdxf
import argparse

from ezdxf.addons import Importer


def merge(source, target):
    importer = Importer(source, target)
    # import all entities from source modelspace into target modelspace
    importer.import_modelspace()
    # import all required resources and dependencies
    importer.finalize()


#Component1 - droite.dxf			Component1 - fond ext.dxf		Component1 - interieur gauche.dxf
base_dxf = ezdxf.readfile('t1.dxf')
l1 = base_dxf.layers
n = 0
for l in l1:
    print("layers : " + str(l))
    s = "L" + chr(48+n)
    on = l.dxf.name
    print("  rename " + on + " to "+s)
    #nl = base_dxf.layers.new(name=s)
    #base_dxf.layers.replace(on, nl)
    #l.rename(s)
    n = n +1
#return

#'Component1 - droite.dxf', 'Component1 - fond ext.dxf',	'Component1 - interieur gauche.dxf')

#for filename in ('t2.dxf', 't3.dxf'):
#    merge_dxf = ezdxf.readfile(filename)
#    merge(merge_dxf, base_dxf)
#
## base_dxf.save()  # to save as file1.dxf
base_dxf.saveas('merged.dxf')


