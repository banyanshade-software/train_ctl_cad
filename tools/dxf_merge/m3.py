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

# https://github.com/awesomebytes/etherdream_tools/blob/master/web_engine/translation_dxf.py

def translation_x_y(dwg, x, y):
    """Given a dwg object, translate x and y coordinates of everything"""
    x = float(x)
    y = float(y)
    #: :type dwg: ezdxf.drawing.Drawing
    for entity in dwg.entities:
        #print "Entity of type: " + str(entity.dxftype())
        if "LINE" == entity.dxftype():
            # This is madness for accesing!
            sx, sy, sz = entity.get_dxf_attrib('start') # I found it in the docs, I actually couldnt find it in attribs
            ex, ey, ez = entity.get_dxf_attrib('end')
            #print "Initial Start -> End"
            #print str((sx, sy, sz)) + " -> " + str((ex, ey, ez))
            
            entity.set_dxf_attrib('start', (sx + x, sy + y, sz))
            entity.set_dxf_attrib('end', (ex + x, ey + y, ez))
            
            #print "Modified Start -> End (+" + str(x) + ", +" + str(y) + ")"
            #print str(entity.get_dxf_attrib('start')) + " -> " + str(entity.get_dxf_attrib('end'))
            #print
        elif "ARC" == entity.dxftype():
            cx, cy, cz = entity.get_dxf_attrib('center')
            #print "Initial center"
            #print str((cx, cy, cz))
            
            entity.set_dxf_attrib('center', (cx + x, cy + y, cz))

            #print "Modified center (+" + str(x) + ", +" + str(y) + ")"
            #print entity.get_dxf_attrib('center')
            #print
        elif "CIRCLE" == entity.dxftype():
            cx, cy, cz = entity.get_dxf_attrib('center')
            entity.set_dxf_attrib('center', (cx + x, cy + y, cz))
            
        elif "POINT" == entity.dxftype():
            # This is madness for accesing!
            lx, ly, lz = entity.get_dxf_attrib('location') # I found it in the docs, I actually couldnt find it in attribs
            entity.set_dxf_attrib('location', (lx + x, ly + y, lz))
            
        else:
            print( "\n\n!!!! ERROR: I don't know this entity type... " + str(entity.dxftype()))

# https://stackoverflow.com/questions/57389079/move-dimension-line-to-new-layer-using-ezdxf
def rename_layer(doc, old, new):
    """ 
    Works only for layers with an entry in the layer table, 
    layers can be used without such an entry. 
    """
    if old not in doc.layers:
        raise ValueError('Old layer "{}" does not exist.'.format(old))
    if new in doc.layers:
        raise ValueError('New layer "{}" does already exist.'.format(new))

    def rename_layer_table_entry():
        layer = doc.layers.get(old)
        layer.dxf.name = new
        # this is an internal API call, renaming table entries isn't implemented (yet)
        doc.layers.replace(old, layer)

    def rename_entities_layer_attribute():
        # layer names are case insensitive
        old_lower = old.lower()
        # iterate over all entities of modelspace, paperspace layouts
        # and block definitions
        for e in doc.chain_layouts_and_blocks():
            if e.get_dxf_attrib('layer', '0').lower() == old_lower:
                e.dxf.layer = new


    rename_layer_table_entry()
    rename_entities_layer_attribute()

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
n = n +1

for filename in ('t2.dxf', 't3.dxf', 't4.dxf', 't5.dxf'):
    print("filename : " + filename)
    merge_dxf = ezdxf.readfile(filename)
    #ms = merge_dxf.modelspace()
    #print("  modelspace: "+str(ms))
    #gd = ms.get_geodata()
    #print("  geodata: "+str(gd))
    #gdat = ms.new_geodata()
    #gdat.dxf.design_point = (0, n*500, 0)
    #continue
    translation_x_y(merge_dxf, n*500, n*100)
    prt_layer(merge_dxf)
    li = iter(merge_dxf.layers)
    ol = next(li)
    print("-- ol : "+str(ol) + " name:"+ol.dxf.name)
    n = n +1
    nl = 'L'+chr(ord('A')+n)
    np = 'P'+chr(ord('A')+n)
    rename_layer(merge_dxf, '0', nl)
    rename_layer(merge_dxf, 'Defpoints', np)
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
    #nl = base_dxf.layers.new(name='ML'+chr(ord('A')+n))
    #np = base_dxf.layers.new(name='MP'+chr(ord('A')+n))
    #base_dxf.layers.replace('0', nl)
    #base_dxf.layers.replace('Defpoints', np)
    print("after replace base:")
    prt_layer(base_dxf)
    print("")

print("merged layer:")
prt_layer(base_dxf)

base_dxf.saveas('merged.dxf')


