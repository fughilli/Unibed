# Unibed

Unibed is #uni#fied em#bed#ded software platform. It is designed to provide \
better platform uniformity, performance, and configurability than Arduino et. \
al.

To build an app for a particular target:

```
./configure.py <board> <app> [<output dir>]
<board>      : the board to build the target for. Must match the name of a
               directory under 'boards/'.
<app>        : the app to build. Must match the name of a directory under
               'apps/'.
<output dir> : the output directory for the build.ninja file. Defaults to '.'.
```

After running ```./configure.py```, run ```ninja``` in the output directory. To
program the target, use ```program```. To debug the application on the target,
use ```debug```.
