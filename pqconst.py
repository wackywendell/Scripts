# coding: UTF-8
import quantities as pq
import quantities.constants as cst

from quantities import m,km,s,J,g,kg
from quantities.constants import h,hbar,G

m_Earth=pq.UnitConstant('Earth_mass', 5.9742e+24 * pq.kg, 'M⊕')
r_Earth=pq.UnitConstant('Earth_radius', 6371 * pq.km, 'R⊕')
r_Earth_pole=pq.UnitConstant('Earth_radius_at_poles', 6356.7523 * pq.km, 'r_Earth_pole')
r_Earth_eq=pq.UnitConstant('Earth_radius_at_equator', 6378.1370 * pq.km, 'r_Earth_Eq')
m_Sun=pq.UnitConstant('Solar_mass', 1.98892e+30 * kg, 'M☉')
