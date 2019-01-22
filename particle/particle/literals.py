from ..shared_literals import common_particles
from .particle import Particle, ParticleNotFound

for item in common_particles:
    try:
        locals()[item] = Particle.from_pdgid(common_particles[item])
    except ParticleNotFound:
        pass
    
del Particle, ParticleNotFound, common_particles