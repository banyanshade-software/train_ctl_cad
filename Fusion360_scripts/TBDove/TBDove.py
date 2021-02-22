#Author-Steven Kraemer
#Description-Connect sketch points that are very close.

import adsk.core, adsk.fusion, adsk.cam, traceback, time

def run(context):
    ret = False
    ui = None
    #t0 = time.clock()
    #------------
    epaisseur = 0.2
    #------------
    h_ext = 1.0
    dh2_ext = 0.5
    dh_ext = 0.2
    #------------
    h2_int = 0.4
    #------------
    h2_dove = 0.2
    l_dove = 0.5
    d_dove = 0.3
    #------------

    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        selection = ui.activeSelections.all
        points = adsk.core.ObjectCollection.create()
        
        #Add only sketchpoints to the points collection
        [points.add(item) for item in selection if isinstance(item, adsk.fusion.SketchPoint)]
        #print(len(points))
        #ui.messageBox("DBDove " + str(points.count) + " points.")
        if points.count != 2:
             ui.messageBox("select exactly 2 points")
             return False
        #ui.messageBox("hop")
        pt1 = points[0]
        pt2 = points[1]
        if pt1.geometry.y < pt2.geometry.y :
                t = pt1
                pt1 = pt2
                pt2 = t  
        #ui.messageBox("PT1 " + str(pt1.parentSketch.classType()) )
        sketch = pt2.parentSketch
        if not sketch :
                ui.messageBox("no sketch")
                return False
        lines = sketch.sketchCurves.sketchLines
        points = sketch.sketchPoints
        arcs = sketch.sketchCurves.sketchArcs
        #ui.messageBox("DBDove " + str(lines.count) + " lines.")
        v1 = pt1.geometry.asVector()
        v2 = pt1.geometry.vectorTo(pt2.geometry)
        #ui.messageBox("DBDove v1" + str(v1.classType()))
        #ui.messageBox("DBDove v2" + str(v1.classType()))
        #v2.substract(v1);
        vm = v1.copy()
        v2.scaleBy(0.5)
        vm.add(v2);
        uv = v2.copy()
        uv.normalize()
        z = adsk.core.Vector3D.create(0,0,1)
        uh = uv.crossProduct(z)

        # ---------------- ext1
        vr1 = vm.copy()
        vt = uh.copy()
        vt.scaleBy(dh_ext)
        vr1.add(vt)
        vt = uv.copy()
        vt.scaleBy(dh2_ext)
        vr1.add(vt)

        vr2 = vr1.copy()
        vt = uv.copy()
        vt.scaleBy(h_ext)
        vr2.add(vt)
     
        vr4 = vr1.copy()
        vt = uh.copy()
        vt.scaleBy(epaisseur)
        vr4.add(vt)

        pr1 = adsk.core.Point3D.create(vr1.x, vr1.y, vr1.z)
        pr2 = adsk.core.Point3D.create(vr2.x, vr2.y, vr2.z)
        pr4 = adsk.core.Point3D.create(vr4.x, vr4.y, vr4.z)
        lines.addThreePointRectangle(pr1,pr2,pr4)


        # ---------------- ext2
        vr1 = vm.copy()
        vt = uh.copy()
        vt.scaleBy(dh_ext)
        vr1.add(vt)
        vt = uv.copy()
        vt.scaleBy(-dh2_ext)
        vr1.add(vt)

        vr2 = vr1.copy()
        vt = uv.copy()
        vt.scaleBy(-h_ext)
        vr2.add(vt)
     
        vr4 = vr1.copy()
        vt = uh.copy()
        vt.scaleBy(epaisseur)
        vr4.add(vt)

        pr1 = adsk.core.Point3D.create(vr1.x, vr1.y, vr1.z)
        pr2 = adsk.core.Point3D.create(vr2.x, vr2.y, vr2.z)
        pr4 = adsk.core.Point3D.create(vr4.x, vr4.y, vr4.z)
        lines.addThreePointRectangle(pr1,pr2,pr4)


        # ---------------- int
        vr1 = vm.copy()
        vt = uh.copy()
        vt.scaleBy(-0.6)
        vr1.add(vt)
        vt = uv.copy()
        vt.scaleBy(-h2_int)
        vr1.add(vt)

        vr2 = vr1.copy()
        vt = uv.copy()
        vt.scaleBy(h2_int*2)
        vr2.add(vt)
     
        vr4 = vr1.copy()
        vt = uh.copy()
        vt.scaleBy(-epaisseur)
        vr4.add(vt)

        pr1 = adsk.core.Point3D.create(vr1.x, vr1.y, vr1.z)
        pr2 = adsk.core.Point3D.create(vr2.x, vr2.y, vr2.z)
        pr4 = adsk.core.Point3D.create(vr4.x, vr4.y, vr4.z)
        lines.addThreePointRectangle(pr1,pr2,pr4)


        # ---------------- rect dove
        vr1 = vm.copy()
        vt = uv.copy()
        vt.scaleBy(-h2_dove)
        vr1.add(vt)

        vr2 = vm.copy()
        vt = uv.copy()
        vt.scaleBy(h2_dove)
        vr2.add(vt)
     
        vr4 = vr1.copy()
        vt = uh.copy()
        vt.scaleBy(l_dove)
        vr4.add(vt)

        pr1 = adsk.core.Point3D.create(vr1.x, vr1.y, vr1.z)
        pr2 = adsk.core.Point3D.create(vr2.x, vr2.y, vr2.z)
        pr4 = adsk.core.Point3D.create(vr4.x, vr4.y, vr4.z)
        lines.addThreePointRectangle(pr1,pr2,pr4)

        # ------------ dove arc
        vr5 = vr4.copy()
        vt = uv.copy()
        vt.scaleBy(h2_dove*2)
        vr5.add(vt)
        pr5 = adsk.core.Point3D.create(vr5.x, vr5.y, vr5.z)

        vo = vr4.copy()
        vt = uv.copy()
        vt.scaleBy(-h2_dove)
        vo.add(vt)
        vt = uh.copy()
        vt.scaleBy(d_dove)
        vo.add(vt)
        po = adsk.core.Point3D.create(vo.x, vo.y, vo.z)

        arcs.addByThreePoints(pr4, po, pr5)


        #pc = adsk.core.Point3D.create(vm.x, vm.y, vm.z)
        #spc  = points.add(pc)

        #s1 = lines.addByTwoPoints(pt1,pt2)
        #(returnValue, intersectingCurves, intersectionPoints) = sketchLine_var.intersections(sketchCurves)


    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
    return ret
