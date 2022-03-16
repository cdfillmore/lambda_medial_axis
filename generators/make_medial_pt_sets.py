path1 = "../medial/"
path2 = "bing_anim/longer/"
path4 = "../distortion/"
path5 = "bing_anim/longer_pts/"

from sys import path, argv
path.append(path1)
path.append(path4)
from medial_axis_approx import approx_medial_axis2
from half_edge_slurm import write_obj
import numpy as np
import random as rd
import json

def dist(x, y):
    return np.sqrt( np.sum( np.square(y-x) ) )

def area_tri(tri):
	a = dist(tri[0], tri[1])
	b = dist(tri[0], tri[2])
	c = dist(tri[1], tri[2])
	s = (a+b+c)/2
	return np.sqrt(s*(s-a)*(s-b)*(s-c))

def read_obj(path):
	pts = []
	simps = []
	with open(path,"r") as f:
		for line in f:
			if line[0] == 'v':
				pts += [[float(i) for i in line.strip('\n').strip(' ').split(' ')[1:4]]]
			elif line[0] == 'f':
				simps += [[ int(i)-1 for i in line.strip('\n').strip(' ').split(' ')[1:4]]]
	return np.array(pts), np.array(simps)


file = argv[1].split("_")[-1]

def main():
	file = argv[1].split("_")[-1]

	num_pts = 50000
	pts, simps = read_obj(path2 + "bing4_triangulation_" + file)
	pts = pts + 0.05 * np.random.rand(len(pts),3)
	samples = []
	areas = np.array([area_tri(pts[i]) for i in simps])
	areas = areas/areas.sum()
	for simp_id in list(rd.choices(range(len(simps)), areas, k=num_pts)):
		simp = simps[simp_id]
		r1 = np.random.rand()
		r2 = np.random.rand()
		samples.append( (1 - np.sqrt(r1))*pts[simp[0]] + np.sqrt(r1)*(1 - r2)*pts[simp[1]] + r2*np.sqrt(r1)*pts[simp[2]] )

	samples = np.array(samples)
	with open( path5 + "longer_pts_" + file[:-4] + '.json', 'w') as out:
	    json.dump([samples.tolist(), ['Red']*num_pts], out)



if __name__ == '__main__':
	main()
