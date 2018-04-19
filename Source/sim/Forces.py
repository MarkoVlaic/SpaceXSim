''' A set of functions used for calculating the forces exerted on the rocket. '''

import numpy as np 
import scipy.constants as const

import CoordinateConversions as conv
import LinearAlgebra as linalg
import InitialParameters as init

def gravity(position, rocket_mass):
	''' Calculates the gravitational force on the rocket at any point. 

	Arguments:
		position: [tuple of floats] A tuple of (X, Y, Z) Cartesian coordinates of the object.
		rocket mass: [float] The rocket's mass (in kg).

	Returns:
		F: [tuple of floats] The force of gravity, split into components.
	'''

	# Unpack values from position tuple
	x = position[0]
	y = position[1]
	z = position[2]

	# Calculate distance from the center of the Earth at any time
	r = np.sqrt(x**2 + y**2 + z**2)

	# Calculate x, y, z components of the force of gravity
	Fx = (const.G * init.Earth.mass * rocket_mass) / r**3 * x
	Fy = (const.G * init.Earth.mass * rocket_mass) / r**3 * y
	Fz = (const.G * init.Earth.mass * rocket_mass) / r**3 * z

	F = (-Fx, -Fy, -Fz)

	return F


def atm_density(position):
	''' Calculates the air density at a given position (height). 
		
		Arguments:
			position: [tuple of floats] A tuple of (X, Y, Z) Cartesian coordinates of the object.

		Returns:
			dens_pos: [float] The atmospheric density at a given position (kgm-3).
	'''
	
	# Unpack values from tuple
	x, y, z = position

	# Calculate atmosphere density at a given height (exponentially decreasing)
	dens_pos = init.Atmosphere.dens_sealvl * np.exp(-conv.getHeight(x, y, z)/init.Atmosphere.scale_height) 

	return dens_pos


def drag_abs(velocity_3d, drag_coeff, position, area):
	''' Calculates the absolute drag force on an object. 

		Arguments:
			velocity_3d: [tuple or array of floats] The object's 3d velocity vector (ms-1).
			drag_coeff: [float] The drag coefficient of the object, (dimensionless quantity). 
			position: [tuple of floats] A tuple of (X, Y, Z) Cartesian coordinates of the object.
			area: [float] The cross-section area of the object (m2). 

		Returns:
			drag: [float] The absolute value of the drag force exerted on the object (N).
	'''

	# Unpack velocity vectors
	vel_x = velocity_3d[0]
	vel_y = velocity_3d[1]
	vel_z = velocity_3d[2]

	# Calculate the absolute value of the velocity vector
	vel_abs = linalg.originDist(vel_x, vel_y, vel_z)

	# Calculate the drag force
	drag = 0.5 * drag_coeff * vel_abs**2 * atm_density(position) * area

	return drag


def thrust_abs(exhaust_velocity, dm, dt):
    ''' Calculates the absolute thrust force on an object. 

        Arguments:
            exhaust_velocity: [float] The exhaust gas velocity of a given rocket (ms-1).
            dm: Change in mass (kg).
            dt: Change in time (s).

        Return:
            thrust: [float] The absolute value of the thrust force exerted on the object (N).
    '''

    # Calculate the thrust force
    thrust = exhaust_velocity * dm / dt 
    
    return thrust