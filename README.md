# Particle Gravity Simulator

Using pygame to render 'particles' which when generated, will bounce around while their mass and relative distance determines the force acting on all other particles. 

Currently implemented:
  Basic gravity calculations based on mass, and a O(n^2) method for updating gravity on particles.
    
  Particles spawn continuously during mouse clicks, and their velocities will be randomized.
  
  Collisions are simple and attempt to preserve inertia betwen objects.

Plan to implement:
   Use KNN clusters to calculate gravity of distant objects to reduce calculations.

   Spawn rate and parameters of particles set by a UI.

   modify collisions to be more accurate.

Would like to implement:
  Add 'elements' to particles.
  Have elements interact with eachother, sort of like little alchemy, but behaves more like a falling sand game.
    *A large mass of helium particles should turn into a star, and should be colored red*

  A primative 'lighting system' so stars / suns illuminate the solar system and can *shine* (could help rendering too, less objects to draw)
