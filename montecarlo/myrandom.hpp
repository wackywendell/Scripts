/*Created so that the generator could be easily switched in and out.
 */
#include <boost/multi_array.hpp>
using namespace boost;

using namespace std;


typedef unsigned int uint;
typedef vector<int> vec;

namespace myrandom{
    float randfloat();
    uint randint(uint max=RAND_MAX);
    void randperm(vec v);
    bool initialize(); // check if its been seeded, and if not, seed it
};