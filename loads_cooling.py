#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 21:27:06 2021

@author: cghiaus

# # Loads
#
# Estimate the values of building characteristic and auxiliary loads
#
# Total:
# - sensible: 45 kW
# - latent: 15 kW

# Rules of thumb, BSRIA 2003
# Solar gains over floor area 150-250 W/m2 of glass (Tab. 3/p 13)
# Heat loads 50 - 100 W/m2 floor area
# U-wall 0.4 W/m2K
# U-window 3.5 W/m2K
"""

import psychro as psy
# constants
c = 1e3         # J/kg K, air specific heat
l = 2496e3      # J/kg, latent heat
ρ = 1.2         # kg/m3, density

# Buildig dimensions
length = 20     # m
width = 30      # m
height = 3.5    # m
persons = 100   # m

sens_heat_person = 60       # W / person
latent_heat_person = 40     # W / person
load_m2 = 15        # W/m2
solar_m2 = 150      # W/m2 of window area
ACH = 1             # Air Cnhnages per Hour
U_wall = 0.4        # W/K, overall heat transfer coeff. walls
U_window = 3.5      # W/K, overall heat transfer coeff. windows

θo, φo = 32, 0.5    # outdoor temperature & relative humidity
θI, φI = 26, 0.5    # indoor temperature & relative humidity
wo = psy.w(θo, φo)
wI = psy.w(θI, φI)

floor_area = length * width
surface_floor = 2 * (length + width) * height + floor_area
surface_wall = 0.9 * surface_floor
surface_window = surface_floor - surface_wall

UA = U_wall * surface_wall + U_window * surface_window
mi = ACH * surface_floor * height / 3600 * ρ

solar_gains = solar_m2 * surface_window
electrical_load = load_m2 * surface_floor
Qsa = persons * sens_heat_person + solar_gains + electrical_load
Qla = persons * latent_heat_person

QsTZ = (UA + mi * c) * (θo - θI) + Qsa
QlTZ = mi * l * (wo - wI) + Qla

θS = θI - 15        # °C supply air temperature
m = QsTZ / c / ((θI - θS))

print(f'QsTZ = {QsTZ:.0f} W, QlTZ = {QlTZ:.0f} W')
print(f'UA = {UA:.0f} W/K, mi = {mi:.2f} kg/s,\
      Qsa = {Qsa:.0f} W, Qla = {Qla:.0f} W')
print(f'm = {m:.3f} kg/s')
