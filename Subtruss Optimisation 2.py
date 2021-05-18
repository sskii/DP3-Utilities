import math

# parameters
k = (200) * ((60) ** 2)					# compression constant
phi = 0.8								# reduction factor

# evaluate a given subtruss
def evaluateSubtruss(length, triangles, precision):

	thetaStep = math.radians(10 ** (-1 * precision))				# because python works in radians
	RHS = (115 * (length ** 2)) / (k * (triangles ** 2))

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
			stMaxCompLoad = (2 * k * phi * (math.cos(theta) ** 3) * (triangles ** 2)) / (length ** 2)
			stMaxTensLoad = (230 * phi) / (math.tan(theta))

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


testTrusses = [2, 4, 6, 8]

for i in testTrusses:
	print(evaluateSubtruss(191.169, i, 2))