#ifndef TASK_SCHEDULER_H
#define TASK_SCHEDULER_H

#include "common.h"

namespace Utils
{
    namespace Task
    {
        template<class... Tasks>
        struct StaticScheduler
        {
            const static Adapters::TaskAdapter::Result_t(*run_methods)() [] =
                { Tasks::operator() ... };
            static constexpr uint32_t num_methods = ARR_LEN(run_methods);

            static Adapters::TaskAdapter::Result_t run_next();
        };

        template<class... Tasks>
        struct StaticSchedulerRoundRobin : StaticScheduler<Tasks...>
        {
            static uint32_t run_index = 0;

            static Adapters::TaskAdapter::Result_t run_next()
            {
                return run_methods[run_index++]();

                if(run_index == num_methods)
                    run_index = 0;
            }
        };
    }
}

#endif // TASK_SCHEDULER_H
