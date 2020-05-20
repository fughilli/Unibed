#include "board.hpp"
#include "utils/time.hpp"
#include "drivers/pin.hpp"

typedef Board::ClockConfig::Default ClockConfig;
typedef Board::BoardConfig::Base<ClockConfig> BoardConfig;
typedef Board::Leds::Default Led;
typedef Time::TimeUtil<ClockConfig> TimeUtil;

int main(void)
{
    BoardConfig::init();

    Led::init();

    while(1)
    {
        
        TimeUtil::sleepMilliseconds(1000);

        Led::toggleState();
    }

    return 0;
}
