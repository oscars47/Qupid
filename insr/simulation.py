from fbpic.main import Simulation
from fbpic.openpmd_diag import FieldDiagnostic, ParticleDiagnostic
from fbpic.lpa_utils.bunch import add_elec_bunch

# Define the simulation box
Nz = 200         # Number of gridpoints along z
zmax = 10.e-6    # Maximum z (meters)
zmin = 0         # Minimum z (meters)
Nr = 50          # Number of gridpoints along r
rmax = 25.e-6    # Maximum r (meters)
c = 299792458    # Speed of light (m.s^-1)
dt = zmax/Nz/c   # Timestep (s)

# Define the beam parameters
gamma_bunch = 400.
sig_r = 1.e-6    # Beam size in r (meters)
sig_z = 1.e-6    # Beam length (meters)
n_e = 4.e24      # Density (particles.m^-3)
Q = -10.e-12     # Charge (Coulombs)

# Initialize the simulation
sim = Simulation(Nz, zmax, Nr, rmax, dt, boundaries='open')

# Add a plasma
plasma_density = 1.e24  # Define the plasma density (particles.m^-3)
sim.add_plasma(density=plasma_density)

# Add an electron bunch
add_elec_bunch(sim, gamma0=gamma_bunch, sig_r=sig_r, sig_z=sig_z,
               n_emit=0., n_part=1.e5, Q=Q)

# Add diagnostics
sim.diags = [FieldDiagnostic(period=100, sim=sim),
             ParticleDiagnostic(period=100, sim=sim,
                                species=sim.ptcl[0])]

# Run the simulation
sim.step(1000)
