#ifndef ADAPTER_ACTION_H
#define ADAPTER_ACTION_H

namespace Utils
{
    namespace Adapters
    {
        struct ActionAdapter
        {
            enum class Result_t : uint32_t
            {
                SUCCESS,
                FAIL
            };

            static Result_t operator()();
        };

        struct NullActionAdapter : ActionAdapter
        {
            static Result_t operator()() { return SUCCESS; }
        };
    }
}

#endif // ADAPTER_ACTION_H
