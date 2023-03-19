#include <vector>
class System {
public:
  System(float infectionRate);
  void create(int x, int y);
  void annihilate(int x);
  // getters and setters for vars
  void setInfectionRate(float infectionRate);
  float getInfectionRate();
  void setDensity(float density);
  float getDensity();
  void setCreationProbability(float creationProbability);
  float getCreationProbability();
  void setLatticeSize(int latticeSize);
  int getLatticeSize();
  void setLattice(std::vector<int> lattice);
  std::vector<int> getLattice();

private:
  void calculateDensity();
  int latticeSize;
  float infectionRate;
  float density;
  float creationProbability;
  std::vector<int> lattice;
  int particleCount;
};