#ifndef BOARD_HPP
#define BOARD_HPP

#include "driverlib/sysctl.h"
#include "drivers/pin.hpp"
#include "registers/registers_gpio.h"

namespace Board
{
    namespace Pins
    {
        typedef Pin::DigitalPin<RegistersGPIO::Port_e::F, 0> F0;
        typedef Pin::DigitalPin<RegistersGPIO::Port_e::F, 1> F1;
        typedef Pin::DigitalPin<RegistersGPIO::Port_e::F, 2> F2;
        typedef Pin::DigitalPin<RegistersGPIO::Port_e::F, 3> F3;
        typedef Pin::DigitalPin<RegistersGPIO::Port_e::F, 4> F4;
        typedef Pin::DigitalPin<RegistersGPIO::Port_e::F, 5> F5;
        typedef Pin::DigitalPin<RegistersGPIO::Port_e::F, 6> F6;
        typedef Pin::DigitalPin<RegistersGPIO::Port_e::F, 7> F7;
    }

    namespace Leds
    {
        typedef Pin::DigitalOutputPin<RegistersGPIO::Port_e::F, 1> Red;
        typedef Pin::DigitalOutputPin<RegistersGPIO::Port_e::F, 2> Blue;

        typedef Red Default;
    }

    namespace Buttons
    {
        typedef Pin::DigitalInputPin<RegistersGPIO::Port_e::F, 0> SW0;

        typedef SW0 Default;
    }

    namespace ClockConfig
    {
        template<uint32_t _extfreq, uint32_t _cpufreq>
        struct External
        {
            const static uint32_t cpufreq = _cpufreq;
            const static uint32_t extfreq = _extfreq;

            static void init()
            {
                uint32_t mask = 0;

                mask |= (cpufreq == 80000000) ? SYSCTL_SYSDIV_2_5 :
                        (cpufreq == 40000000) ? SYSCTL_SYSDIV_5 : 0;

                mask |= (extfreq == 16000000) ? SYSCTL_XTAL_16MHZ : 0;

                SysCtlClockSet(mask | SYSCTL_USE_PLL | SYSCTL_OSC_MAIN);
            }
        };

        typedef External<16000000ul, 80000000ul> Default;
    }

    namespace BoardConfig
    {
        template<class ClockConfig>
        struct Base
        {
            static void init()
            {
                ClockConfig::init();
            }
        };

        typedef Base<ClockConfig::Default> Default;
    }
}

#endif
