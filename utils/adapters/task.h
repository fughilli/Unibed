#ifndef ADAPTER_TASK_H
#define ADAPTER_TASK_H

namespace Utils
{
    namespace Adapters
    {
        struct TaskAdapter
        {
            enum class RunState_t : uint32_t
            {
                CONTINUE,
                DONE
            };

            static RunState_t : operator()();
        };

        struct NullTaskAdapter : TaskAdapter
        {
            static RunState_t operator()() { return DONE; }
        };
    }
}

#endif // ADAPTER_TASK_H
