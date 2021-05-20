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
		round(math.degrees(theta), precision),
		round(stMaxCompLoad, 2),
		round(stMaxTensLoad, 2),
		round(diagLength, 2),
		round(vertLength, 2)
	]


l = 0

p1 = [float(input(    "Enter start x coordinate:  ")), float(input("Enter start y coordinate: "))]
p2 = [float(input(  "\nEnter end x coordinate:    ")), float(input("Enter end y coordinate:   "))]
triangles = int(input("Input number of triangles: "))
reduction = int(input("Input scale-down factor:   "))

dx = p2[0] - p1[0]
dy = p2[1] - p1[1]

l = math.sqrt( dx**2 + dy**2 )
data = evaluateSubtruss(l, triangles, 3)

if data[0]:
	# only if truss is valid.

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

		print("Centre point: (", cp[0] / reduction, ",", cp[1] / reduction, ")")

		# check whether there are additional joints
		if i % 2 == 1:
			# there are

			# calc half of the tension member's length
			l = data[5] / 2

			# calculate the aditional joint locations
			up = [(-1 * l * math.sin(a)), (l * math.cos(a))]
			lp = [(l * math.sin(a)), (-1 * l * math.cos(a))]

			# print the coordinates
			print("Upper point:  (", up[0] / reduction, ",", up[1] / reduction, ")")
			print("Lower point:  (", lp[0] / reduction, ",", lp[1] / reduction, ")")
		


	print("\n* Geometry Stats *")
	print("Change in x:  ", dx, "mm")
	print("Change in y:  ", dy, "mm")
	print("Incline angle:", angle, "degrees. (Note that this is not absolute.)")
	print("Length of compression members:", data[3], "mm")
	print("Length of tension members:    ", data[4], "mm")

	print("\n* Capacity Stats *")
	print("Maximum capacity by compression members:", data[1], "N")
	print("Maximum capacity by tension members:    ", data[2], "N")


	print("\nDone.")

else:
	# invalid truss calculation.
	print("ERROR: This subtruss is invalid. You've screwed something up. Terribly sorry.")

print("\nSubtruss measures ", l, "mm.")

