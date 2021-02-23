# CAD tools / files for Z-scale model railway

This repository contains

* tools : a few Fusion360 scripts and python script (using ezdxf)

* trackbed : my own layout, trackbed being laser cut. Probably not adapted for other people

* houses : some Z-scale houses, ready to laser-cut, sharable (GPL)


## Workflow

I use Fusion360 as main CAD software (free for hobbyist use) and deepnest.io for nesting

Fusion360 --> DXF4Laser plugin --> DXF files (plenty)
                                          |
                                          V
                                   merge.py script (in tools dir)
                                          |
                                          V
                                       merged.dxf
                                          |
                                          V
                                       deepnest.io
                                          |
                                          V
                                        nested.dxf

I the use again merge.py script to combine several nested DXF files in a single files (untested for now),
and I send it to sculpteo.com for laser cutting
                                          

