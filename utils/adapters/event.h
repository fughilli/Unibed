#ifndef ADAPTERS_EVENT_H
#define ADAPTERS_EVENT_H

namespace Adapters
{
    struct EventAdapter
    {
        static void operator()();
    };

    struct NullEventAdapter : EventAdapter
    {
        static void operator()() {}
    };
}

#endif // ADAPTERS_EVENT_H
