#!/opt/local/bin/python3.8
# ... !/usr/bin/env python37

#pip3 install ezdxf


#:se et
#:se ts=4
#:ret

# rotate a dxf containing a single part to minimize its height
# (i.e. put the part horizontally)

from posixpath import basename
import os
import ezdxf
import argparse
import math

from ezdxf.addons import Importer
from ezdxf import bbox


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



# https://github.com/awesomebytes/etherdream_tools/blob/master/web_engine/translation_dxf.py

def translation_x_y(dwg, x, y):
    """Given a dwg object, translate x and y coordinates of everything"""
    x = float(x)
    y = float(y)
    #Matrix44 translate(dx: float, dy: float, dz: float) → Matrix44
    m44 = ezdxf.math.Matrix44.translate(x,y,0)
    print("m44=", m44)
    #: :type dwg: ezdxf.drawing.Drawing
    for entity in dwg.entities:
        entity.transform(m44)

def rotate(dwg, ang_deg):
    ang_rad = ang_deg * math.pi / 180.0
    m44 = ezdxf.math.Matrix44.z_rotate(ang_rad)
    for entity in dwg.entities:
        entity.transform(m44)


def prt_layer(source):
    l1 = source.layers
    for l in l1:
        print("   layers : " + str(l) + " name: '" + l.dxf.name +"'")

def optimum_rotate(filename, seplayer=False):
    print("file : "+filename)
    org_dxf =  ezdxf.readfile(filename)
    n=1
    if seplayer:
        nl = 'L'+chr(ord('A')+n)
        np = 'P'+chr(ord('A')+n)
        rename_layer(org_dxf, '0', nl)
        rename_layer(org_dxf, 'Defpoints', np)
    hmin = 999999999
    bestdxf = None
    bestang  = None
    for ang in range(0, 360, 1):
        rdxf =  ezdxf.readfile(filename)
        rotate(rdxf, ang)
        s = bbox.extends(rdxf.modelspace()).size
        h = s[1]
        if (h < hmin) and (hmin-h >1E-5) :
            hmin = h
            bestang= ang
            bestdxf = rdxf
            #print("  angle=",ang, " h=", h)
            #print("      s   : ", s)
            #print("      s0  : ", bbox.extends(org_dxf.modelspace()).size)
           

    if bestdxf is None:
        print("no rotation")
        return org_dxf
    print("rotation ", bestang)
    return bestdxf



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('dxf_file', metavar='dxf_file', type=str, #nargs=1,
                    help='dxf file to process')
    parser.add_argument("--layers", help="one layer per input file", action="store_true")
   
    args = parser.parse_args()
    print("file: ", args.dxf_file)
    
    fn = args.dxf_file
    fbn = basename(fn)
    fxn = os.path.splitext(fbn)[0]
    fout = fxn + '_opt.dxf'
    d = optimum_rotate( args.dxf_file, args.layers)
    print("save to : ", fout)
    msp = d.modelspace()
    s = bbox.extends(msp).size
    print("final size: ",s)    
    d.saveas(fout)



