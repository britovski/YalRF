import time
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

import setup
from yalrf import YalRF, Netlist
from yalrf.Analyses import HarmonicBalance, MultiToneHarmonicBalance

y = Netlist('Oscillator')

# circuit parameters
vcc = 3
vee = -3
rb = 100
re = 2.2e3
l = 5e-6
c1 = 200e-12
c2 = 50e-12
freq = 0

# VCC
y.add_idc('I1', 'nx1', 'gnd', dc=vcc)
y.add_gyrator('G1', 'nx1', 'nvcc', 'gnd', 'gnd', 1)

# VEE
y.add_idc('I2', 'nx2', 'gnd', dc=vee)
y.add_gyrator('G2', 'nx2', 'nvee', 'gnd', 'gnd', 1)

# passives
#y.add_resistor('Rb', 'nb', 'gnd', rb)
y.add_resistor('Re', 'ne', 'nvee', re)
y.add_resistor('Rx', 'nvccx', 'nvcc', 10)
y.add_inductor('L1', 'nvccx', 'nc', l)
y.add_capacitor('C1', 'ne', 'nc', c1)
y.add_capacitor('C2', 'nvcc', 'ne', c2)

# bjts
q1 = y.add_bjt('Q1', 'gnd', 'nc', 'ne')

q1.options['Is'] = 10.2e-15
q1.options['Bf'] = 301
q1.options['Br'] = 4
q1.options['Ne'] = 2
q1.options['Nc'] = 2
q1.options['Ise'] = 5.82e-12
q1.options['Vaf'] = 121
q1.options['Var'] = 24
q1.options['Ikf'] = 60.7e-3
q1.options['Ikr'] = 0.15

q1.options['Cje'] = 26.8e-12
q1.options['Vje'] = 1.1
q1.options['Mje'] = 0.5
q1.options['Cjc'] = 8.67e-12
q1.options['Vjc'] = 0.3
q1.options['Mjc'] = 0.3
q1.options['Xcjc'] = 1
q1.options['Cjs'] = 0
q1.options['Vjs'] = 0.75
q1.options['Mjs'] = 0
q1.options['Fc'] = 0.5
q1.options['Tf'] = 427e-12
q1.options['Tr'] = 50.3e-9

numharmonics = 10
freq = 9e6
V0 = 1

hb = MultiToneHarmonicBalance('HB1')
hb.options['maxiter'] = 100

converged, freqs, Vf, _, _ = hb.run_oscillator(y, freq, numharmonics, V0, 'nc')

hb.print_v('nc')
hb.plot_v('nc')
plt.show()


