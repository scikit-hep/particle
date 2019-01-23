from ..shared_literals import common_particles
from .pdgid import PDGID

for item in common_particles:
    locals()[item] = PDGID(common_particles[item])
    
del PDGID, common_particles