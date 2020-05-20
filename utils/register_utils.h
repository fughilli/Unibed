#ifndef REGISTER_UTILS_H
#define REGISTER_UTILS_H

#include <stdint.h>

#define REGMAP_EMPTY(__size__,__name__) uint8_t __name__[(__size__)]
#define FOLD(x) (__builtin_constant_p(x) ? (x) : (x))

namespace RegisterUtil
{
    template<typename T, intptr_t ptr>
    constexpr T* declareAt()
    {
        /* Thanks to gcc 4.9.x, there is now full enforcement of the constexpr
         * rules that disallow creation from a compile-time constant integer.
         * However, we can use a little compiler extension hack to get around
         * it.
         */
        return FOLD(reinterpret_cast<T*>(ptr));
    }

}

#endif
