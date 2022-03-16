## medial

#Medial axis visualisation software

* Requires pyopengl for builtin visualisations on top of standard numpy, scipy etc
* Generator folder has several scripts for generating triangulations of surfaces
* Medial axes computation is done in medial_axis_approx.py (you dont need to recompute the medial axes for each time you run the visualisation)
* Visualisation is done in stupid_opengl.py
* To see the visualisation use vis_script.py you can select which triangulation you want to use from some commented options there
* Within the visualisation "space bar" toggles the rotation, "s" toggles the surfaces, "m" toggles the medial axes and "q" quits the visualisation.
* You can also use the mouse to change the viewing angle.
* Use the write_obj function to create a .obj file to read into blender
* /generators/bing.json has a frame from which to create a lambda medial axis frame




