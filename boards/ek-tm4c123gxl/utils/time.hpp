#ifndef TIME_HPP
#define TIME_HPP

#include "driverlib/sysctl.h"

namespace Time
{
    template<class BoardConfig>
    struct TimeUtil
    {
        static void sleepMilliseconds(uint32_t millis)
        {
            SysCtlDelay(BoardConfig::cpufreq * 3 * millis / 1000);
        }
    };
}

#endif
