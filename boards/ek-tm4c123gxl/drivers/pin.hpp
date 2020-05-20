#ifndef DRIVER_PIN_HPP
#define DRIVER_PIN_HPP

#ifdef __cplusplus

#include "driverlib/sysctl.h"
#include "registers/registers_gpio.h"

#include <stdint.h>

using namespace RegistersGPIO;

namespace Pin
{
    enum Mode_e
    {
        INPUT = 0,
        OUTPUT = 1
    };

    enum State_e
    {
        LOW = 0,
        HIGH = 1
    };

    enum PullMode_e
    {
        NONE = 0,
        UP = 1,
        DOWN = 2
    };

    /**
     * @brief This is a Digital Pin template class.
     */
    template<Port_e gpio_port, uint32_t gpio_pin>
    class DigitalPin
    {
        public:

            static void init()
            {
                /*
                 * Enable the clock to the given peripheral.
                 *
                 * [340]
                 */
                SysCtlPeripheralEnable(sysctl_periph);

                /*
                 * Select the GPIO function for the given pin on the given port.
                 *
                 * [672, 10.5-R10]
                 */
                gpio_registers->AFSEL &= ~gpio_pin_mask;

                /*
                 * Select 2mA drive strength.
                 *
                 * [673, 10.5-R11]
                 */
                gpio_registers->DR2R |= gpio_pin_mask;

                /*
                 * Disable pull-ups and pull-downs.
                 *
                 * [677, 10.5-R15; 679, 10.5-R16]
                 */
                gpio_registers->PUR &= ~gpio_pin_mask;
                gpio_registers->PDR &= ~gpio_pin_mask;

                /*
                 * Disable slew rate control.
                 *
                 * [681, 10.5-R17]
                 */
                gpio_registers->SLR &= ~gpio_pin_mask;

                /*
                 * Enable the digital functions.
                 *
                 * [682, 10.5-R18]
                 */
                gpio_registers->DEN |= gpio_pin_mask;

                gpio_registers->PUR &= ~gpio_pin_mask;
                gpio_registers->PDR &= ~gpio_pin_mask;

                setMode(INPUT);
            }

            static void setMode(Mode_e mode)
            {
                switch(mode)
                {
                    case OUTPUT:
                        gpio_registers->DIR |= gpio_pin_mask;
                        break;

                    case INPUT:
                        gpio_registers->DIR &= ~gpio_pin_mask;
                        break;
                }
            }

            static Mode_e getMode()
            {
                if(gpio_registers->DIR & gpio_pin_mask)
                    return OUTPUT;

                return INPUT;
            }

            static void toggleState()
            {
                uint8_t oldval = gpio_registers->DATA[gpio_pin_mask << 2];
                gpio_registers->DATA[gpio_pin_mask << 2] = oldval ^ 0xFF;
            }

            static void setState(State_e state)
            {
                switch(state)
                {
                    case LOW:
                        gpio_registers->DATA[gpio_pin_mask << 2] = 0;
                        break;

                    case HIGH:
                        gpio_registers->DATA[gpio_pin_mask << 2] = 0xFF;
                        break;
                }
            }

            static State_e getState()
            {
                if(gpio_registers->DATA[gpio_pin_mask << 2])
                    return HIGH;

                return LOW;
            }

            static PullMode_e getPullMode()
            {
                if(gpio_registers->PUR & gpio_pin_mask)
                    return UP;
                if(gpio_registers->PDR & gpio_pin_mask)
                    return DOWN;
                return NONE;
            }

            static void setPullMode(PullMode_e pullmode)
            {
                switch(pullmode)
                {
                    case UP:
                        gpio_registers->PUR |= gpio_pin_mask;
                        break;

                    case DOWN:
                        gpio_registers->PDR |= gpio_pin_mask;
                        break;

                    default:
                        break;
                }
            }

        private:
            static constexpr uint32_t sysctl_periph =
                (gpio_port == Port_e::A) ? SYSCTL_PERIPH_GPIOA :
                (gpio_port == Port_e::B) ? SYSCTL_PERIPH_GPIOB :
                (gpio_port == Port_e::C) ? SYSCTL_PERIPH_GPIOC :
                (gpio_port == Port_e::D) ? SYSCTL_PERIPH_GPIOD :
                (gpio_port == Port_e::E) ? SYSCTL_PERIPH_GPIOE :
                                           SYSCTL_PERIPH_GPIOF;

            static constexpr uint32_t gpio_pin_mask = 1 << gpio_pin;

            static constexpr intptr_t gpio_registers_base =
                (gpio_port == Port_e::A) ? 0x40004000 :
                (gpio_port == Port_e::B) ? 0x40005000 :
                (gpio_port == Port_e::C) ? 0x40006000 :
                (gpio_port == Port_e::D) ? 0x40007000 :
                (gpio_port == Port_e::E) ? 0x40024000 :
                                           0x40025000;

            static constexpr Map* const gpio_registers =
                RegisterUtil::declareAt<Map, gpio_registers_base>();
    };

    template<Port_e gpio_port, uint32_t gpio_pin>
    class DigitalInputPin : public DigitalPin<gpio_port, gpio_pin>
    {
        public:
            static void init()
            {
                DigitalPin<gpio_port, gpio_pin>::init();
                DigitalPin<gpio_port, gpio_pin>::setMode(Mode_e::INPUT);
            }

    };

    template<Port_e gpio_port, uint32_t gpio_pin>
    class DigitalOutputPin : public DigitalPin<gpio_port, gpio_pin>
    {
        public:
            static void init()
            {
                DigitalPin<gpio_port, gpio_pin>::init();
                DigitalPin<gpio_port, gpio_pin>::setState(State_e::LOW);
                DigitalPin<gpio_port, gpio_pin>::setMode(Mode_e::OUTPUT);
            }

    };

    template<typename T>
    class AnalogPin
    {
        public:
            static T getValue() { return static_cast<T>(0); }
        private:
    };
}

#endif

#endif
