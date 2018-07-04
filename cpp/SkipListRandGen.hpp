#ifndef SKIP_LIST_RAND_GEN_H
#define SKIP_LIST_RAND_GEN_H

#include <cstdlib>
#include <time.h>

class RandomHeight {
  public:
    RandomHeight(int max_level, float prob);
    ~RandomHeight() {}
    int new_level();
 
  private:
    int max_level_;
    float prob_;
};

RandomHeight::RandomHeight(int max_level, float prob) : max_level_(max_level), prob_(prob) {
  srand(time(NULL));
}

int RandomHeight::new_level() {
  float p;

  int level = 1;

  while (1) {
    p = static_cast<float>(std::rand()) / static_cast<float>(RAND_MAX);

    if (p >= prob_ || level >= max_level_) {
      break;
    }

    level += 1;
  }

  return level;
}

#endif
