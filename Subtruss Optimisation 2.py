import math

# environment parameters #
kComp = (200) * ((60) ** 2)				# compression constant
kTens = 230								# tension constant
phi = 0.8								# reduction factor

# evaluate a given subtruss
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


# test code #
triangles = [2, 4, 6, 8]	# possible numbers of triangles
							# trusses to test
subtrusses = [191.169, 261.600, 111.111]

for i in subtrusses:
	print("\nSolutions for", i, "mm subtruss:\nTriangles:  Half of enclosed angle:  Capacity (diags, verts)^  Length (diags, verts)")
	for n in triangles:
		data = evaluateSubtruss(i, n, 3)
		
		if data[0]:
			print(
				n, "         ", data[1],
				"                    (", data[2], ",", data[3],
				")      (", data[4], ",", data[5], ")"
			)
		
		else:
			# unsuccessful run
			print(n, "          No solutions found.")