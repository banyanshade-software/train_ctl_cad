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

def prt_layer(source):
    l1 = source.layers
    for l in l1:
        print("   layers : " + str(l) + " name: '" + l.dxf.name +"'")

#Component1 - droite.dxf			Component1 - fond ext.dxf		Component1 - interieur gauche.dxf
base_dxf = ezdxf.readfile('t1.dxf')
n = 0
nl = base_dxf.layers.new(name='L'+chr(ord('A')+n))
np = base_dxf.layers.new(name='P'+chr(ord('A')+n))
base_dxf.layers.replace('0', nl)
base_dxf.layers.replace('Defpoints', np)

for filename in ('t2.dxf', 't3.dxf', 't4.dxf', 't5.dxf'):
    merge_dxf = ezdxf.readfile(filename)
    print("filename : " + filename)
    prt_layer(merge_dxf)
    li = iter(merge_dxf.layers)
    ol = next(li)
    print("-- ol : "+str(ol) + " name:"+ol.dxf.name)
    n = n +1
    #nl = merge_dxf.layers.new(name='ML'+chr(ord('A')+n))
    #np = merge_dxf.layers.new(name='MP'+chr(ord('A')+n))
    #print("after create:")
    #prt_layer(merge_dxf)
    #merge_dxf.layers.replace('Defpoints', np)
    #merge_dxf.layers.replace(ol.dxf.name, nl)
    #n0 = merge_dxf.layers.new('0')
    #print("after replace:")
    #prt_layer(merge_dxf)
    merge(merge_dxf, base_dxf)
    nl = base_dxf.layers.new(name='ML'+chr(ord('A')+n))
    #np = base_dxf.layers.new(name='MP'+chr(ord('A')+n))
    base_dxf.layers.replace('0', nl)
    #base_dxf.layers.replace('Defpoints', np)
    print("after replace base:")
    prt_layer(base_dxf)
    print("")

print("merged layer:")
prt_layer(base_dxf)

base_dxf.saveas('merged.dxf')


