''' A set of functions used to describe the initial parameters pf the rocket. '''

import numpy as np
import scipy.constants as const

class Earth:
	mass = 5.9722e24
	polr = 6356.7523e3
	equat = 6378.1370e3
	ecc_sqr = 1 - (polr/equat)**2
	sec_ecc_sqr = ecc_sqr / (1 - ecc_sqr)
	d = sec_ecc_sqr * polr

class Atmosphere:
	dens_sealvl = 1.225
	scale_height = 8500

class Falcon9FT:
	total_mass = 544.6e3
	dry_mass = 27.9e3
	diameter = 5.2633
	exhaust_velocity = 2.77e3

class FalconHeavy:
	total_mass = 1385.5e3
	dry_mass = 55.5e3
	diameter = 6.339 # Area is equal to main + 2 boosters
	exhaust_velocity = 2.77e3

def getVel(height):
	'''
	Calculates the orbital velocity at a given height from the Earth's surface (estimated lat = 90)
	Arguments:
		height: Height from the Earth's surface. (m)
	
	Returns:
		vel: Orbital velocity at given height. (m/s)
	'''

	vel = np.sqrt(const.G * Earth.mass / (Earth.polr + height))
	
	return vel

def getMass(payoload_mass, exhaust_velocity, height, k):
	'''
	Calculates the mass required to reach a given height. 
	Arguments:
		payload_mass: The desired payload mass. (kg)
		exhaust_velocity: Fuel exhaust velocity. (m/s)
		height: Height from the Earth's surface. (m)
		k: Ratio of the ? mass to the payload mass. (1)

	Returns:
		mass: Initial rocket mass (kg) 
	'''

	mass = np.exp(getVel(height)/exhaust_velocity) * payoload_mass * (k + 1)
	
	return mass

if __name__ == '__main__':

	print(Earth.mass, Earth.polr)
	print(Atmosphere.dens_sealvl)
	m = getMass(60e3, 2.77e3, 10e3, 3)
	print(m/1e6)