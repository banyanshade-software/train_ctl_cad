#!/opt/local/bin/python3.8
# ... !/usr/bin/env python37

#pip3 install ezdxf


#:se et
#:se ts=4
#:ret

import ezdxf

def remove_layer_view_port(dwg):
     if 'VIEW_PORT' in dwg.layers:
             dwg.layers.remove('VIEW_PORT')
     if 'View Port' in dwg.layers:
             dwg.layers.remove('View Port')

def remove_all_dim_styles(dwg):
     delete = [dimstyle.dxf.name for dimstyle in dwg.dimstyles if dimstyle.dxf.name.upper() != 'STANDARD']
     for name in delete:
         dwg.dimstyles.remove(name)


def remove_all_linetypes_styles(dwg):
     protect = {'bylayer', 'byblock', 'continuous'}
     delete = [ltype.dxf.name for ltype in dwg.linetypes if ltype.dxf.name.lower() not in protect]
     for name in delete:
         dwg.linetypes.remove(name)

def remove_all_text_styles(dwg):
     delete = []
     for style in dwg.styles:
         if style.dxf.name.upper() == 'STANDARD':
             style.dxf.font = 'txt'
         else:
             delete.append(style.dxf.name)
     for name in delete:
         dwg.styles.remove(name)


d = ezdxf.readfile('t5.dxf')
remove_all_dim_styles(d)
remove_all_linetypes_styles(d)
remove_all_text_styles(d)
remove_layer_view_port(d)
#print("...",d.dimstyles)
d.saveas('merged.dxf')


