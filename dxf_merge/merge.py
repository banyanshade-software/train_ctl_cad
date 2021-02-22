#!/opt/local/bin/python3.8
# ... !/usr/bin/env python37

#pip3 install ezdxf


#:se et
#:se ts=4
#:ret

import ezdxf
import argparse

from ezdxf.addons import Importer
from ezdxf import bbox



def merge(source, target):
    importer = Importer(source, target)
    # import all entities from source modelspace into target modelspace
    importer.import_modelspace()
    #importer.import_paperspace_layouts()
    # import all required resources and dependencies
    importer.finalize()

# https://github.com/awesomebytes/etherdream_tools/blob/master/web_engine/translation_dxf.py

def translation_x_y(dwg, x, y):
    """Given a dwg object, translate x and y coordinates of everything"""
    x = float(x)
    y = float(y)
    #: :type dwg: ezdxf.drawing.Drawing
    for entity in dwg.entities:
        print("Entity of type: " + str(entity.dxftype()))
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
            print( "ERROR: I don't know this entity type... " + str(entity.dxftype()))

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


def merge_dxfs(listname, seplayer=False, shifth=0, shiftv=0):
    n = -1
    tx = 10
    ty = 0
    for filename in listname:
        n = n+1
        merge_dxf = ezdxf.readfile(filename)
        print("file : "+filename)
        #print("header : ", merge_dxf.header)
        #print("EXTMAX ", merge_dxf.header['$EXTMAX'])
        #print("EXTMIN ", merge_dxf.header['$EXTMIN'])
        #print("LIMMAX ", merge_dxf.header['$LIMMAX'])
        #print("LIMMIN ", merge_dxf.header['$LIMMIN'])
       
        if seplayer:
            nl = 'L'+chr(ord('A')+n)
            np = 'P'+chr(ord('A')+n)
            rename_layer(merge_dxf, '0', nl)
            rename_layer(merge_dxf, 'Defpoints', np)
        if shifth>0 or shiftv>0 :
            msp = merge_dxf.modelspace()
            cache = bbox.Cache()
            bounds = bbox.extends(msp, cache)
            minpt = bounds.extmin
            s = bounds.size
            print("bbox : ", bounds)
            print("  min : ", minpt)
            print("  s   : ", s)
            dx = tx - minpt[0]
            dy = ty - minpt[1]
            print("dx = ", dx, " dy = ", dy)

            #translation_x_y(merge_dxf, n*500, n*100)
            translation_x_y(merge_dxf, dx, dy)
            if shifth>0:
                tx = tx + s[0] + shifth
            if shiftv>0:
                ty = ty + s[1] + shiftv
        if n > 0:
            merge(merge_dxf, base_dxf)
        else:
            base_dxf = merge_dxf
    return base_dxf
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('dxf_files', metavar='dxf_file', type=str, nargs='+',
                    help='dxf files to be merged')
    parser.add_argument("--layers", help="one layer per input file", action="store_true")
    parser.add_argument("--vspace", nargs=1, help="space dxf horizontaly", type=int, default=[0])
    parser.add_argument("--hspace", nargs=1, help="space dxf vertically",  type=int,default=[0])
    args = parser.parse_args()
    print("files: ", args.dxf_files)
    print("vspace: ", args.vspace)
    print("hspace: ", args.hspace)
    vspace = args.vspace[0] 
    hspace = args.hspace[0] 
    d = merge_dxfs( args.dxf_files, args.layers, hspace, vspace)
    d.saveas('merged.dxf')
    #if args.layers:
    #    print("with layers")
    #else:
    #    print("without layers")



#def merge_dxfs(listname, seplayer=False, shifth=True, shiftv=False):
#d = merge_dxfs( ('t1.dxf', 't2.dxf', 't3.dxf', 't4.dxf', 't5.dxf'), True, False, False)


