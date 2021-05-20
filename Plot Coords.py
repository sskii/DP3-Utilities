# takes an input for the subtruss start and end coords and the number of members
# and returns the coordinates for all of the joints to make it easy to draw the
# designs by hand easier.

# also includes functionality to scale the output dimensions

import math

# environment parameters #
kComp = (200) * ((60) ** 2)				# compression constant
kTens = 230								# tension constant
phi = 0.8								# reduction factor

# evaluate a given subtruss #
def evaluateSubtruss(length, triangles, precision):

	thetaStep = math.radians(10 ** (-1 * precision))				# because python works in radians
	RHS = (kTens * (length ** 2)) / (2 * kComp * (triangles ** 2))

	# run results
	success = False
	stMaxCompLoad = 0
	stMaxTensLoad = 0
	diagLength = 0
	vertLength = 0

	theta = 0			# test theta
	run = True			# flag

	while run:

		if theta > math.radians(90):
			#stop execution
			run = False

		# evaluate LHS for current value of theta
		LHS = (math.sin(theta)) * ((math.cos(theta)) ** 2)

		if LHS > RHS:
			#solution found

			# calc expected subtruss capacity
			stMaxCompLoad = (2 * kComp * phi * (math.cos(theta) ** 3) * (triangles ** 2)) / (length ** 2)
			stMaxTensLoad = (kTens * phi) / (math.tan(theta))

			# calc member lengths
			diagLength = (length) / (triangles * math.cos(theta))
			vertLength = (2 * length * math.tan(theta)) / (triangles)

			# stop execution
			run = False

			# note that run was successful
			success = True

		else:
			#no solution found
			theta += thetaStep	# increment theta
	
	return [
		success,
		math.degrees(theta),
		stMaxCompLoad,
		stMaxTensLoad,
		diagLength, 2,
		vertLength, 2
	]


l = 0

print("All lengths mm.")

p1 = [float(input(    "Enter start x coordinate:  ")), float(input("Enter start y coordinate:  "))]
p2 = [float(input(  "\nEnter end x coordinate:    ")), float(input("Enter end y coordinate:    "))]
triangles = int(input("Input number of triangles: "))
print("NB: Scaling is about the origin (0,0) and NOT the truss start.")
reduction = int(input("Input scale-down factor:   "))
sigfigs =   int(input("Input nº of sig. fig.s:    "))

dx = p2[0] - p1[0]
dy = p2[1] - p1[1]

l = math.sqrt( dx**2 + dy**2 )
	print("\nDesign is valid. Evaluation:\n")
data = evaluateSubtruss(l, triangles, sigfigs)

if data[0]:
	# only if truss is valid.
	print("\nDesign is valid. Evaluation:\n")

	# calculate x and y steps per joint
	joint_dx = dx / triangles
	joint_dy = dy / triangles

	# calculate the incline
	angle = 90
	if dx != 0:
		# cannot divide by zero, but otherwise…
		angle = math.degrees(math.atan(dy/dx))

	a = math.radians(angle)

	# find the joints along the centreline
	for i in range(0, triangles + 1):

		# get the coordinates of the relevant centre point
		cp = [(joint_dx * i), (joint_dy * i)]

		print("Centre point: (", math.round(cp[0] / reduction, 1), ",", math.round(cp[1] / reduction, 1), ")")

		# check whether there are additional joints
		if i % 2 == 1:
			# there are

			# calc half of the tension member's length
			l = data[5] / 2

			# calculate the aditional joint locations
			up = [(-1 * l * math.sin(a)), (l * math.cos(a))]
			lp = [(l * math.sin(a)), (-1 * l * math.cos(a))]

			# print the coordinates
			print("Upper point:  (", math.round(up[0] / reduction, 1), ",", math.round(up[1] / reduction, 1), ")")
			print("Lower point:  (", math.round(lp[0] / reduction, 1), ",", math.round(lp[1] / reduction, 1), ")")
		


	print("\n* Geometry Stats *")
	print("Overall span: ", math.round(l, sigfigs), "mm.")
	print("Change in x:  ", math.roung(dx, sigfigs), "mm")
	print("Change in y:  ", math.round(dy, sigfigs), "mm")
	print("Incline angle:", math.round(angle, sigfigs), "degrees. (Note that this is not absolute.)")
	print("Length of compression members:", math.round(data[3], sigfigs), "mm")
	print("Length of tension members:    ", math.round(data[4], sigfigs), "mm")

	print("\n* Capacity Stats *")
	print("Maximum capacity by compression members:", math.round(data[1], sigfigs), "N")
	print("Maximum capacity by tension members:    ", math.round(data[2], sigfigs), "N")


	print("\nDone.")

else:
	# invalid truss calculation.
	print("ERROR: This subtruss is invalid. You've screwed something up. Terribly sorry.")

