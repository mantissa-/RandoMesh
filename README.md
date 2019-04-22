# RandoMesh
v0.1.1

A Blender addon to add randomized geometry to any mesh. Supports Blender 2.80.  
**To install, download the zip file and install as an addon in the Blender preferences panel.**

![RandoMesh 0.1.1 UI](https://i.imgur.com/p0UM6Oa.jpg)

RandoMesh works by taking your geometry and adding random subdivisions to it. It was created to start learning Python in Blender and automate some of my workflow, so expect bugs. **Make sure to always save your work before using this addon!**

I've found the best results occur with meshes under 5000 polygons. Lots of iterations can really slow things down, so beware. Opening blender from a terminal will give you detailed output of each step of the process.

#### Example (Processed with default settings)
![RandoMesh 0.1.0  Result](https://i.imgur.com/Vy40HBm.jpg)


Processing Log (Example terminal output):

```
Iterations: 5
--------
Iteration #1: 0.226s	G:12 | S:1 | Extrude: -0.0009	P:T	T:F
Iteration #2: 0.507s	G:6  | S:2 | Extrude: -0.0007	P:F	T:F
Iteration #3: 1.453s	G:7  | S:3 | Extrude: -0.0006	P:T	T:F
Iteration #4: 1.738s	G:7  | S:3 | Extrude: 0.0007	P:T	T:F
Iteration #5: 1.671s	G:7  | S:3 | Extrude: 0.0007	P:F	T:F

Decimation: 1.4232s	Ratio: 0.29
Smoothing: 1.7921s	Iterations: 7
Done! (10.0s total)
```

License: GPL v3

## Changelog

**0.1.1:**
- Added option to adjust subdivision smoothing factor for all iterations
- Github zip install now works

**0.1.0:**
Initial Release
