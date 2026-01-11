+++
title = "Install GStreamer SRT plugin on macOS"
date = 2022-06-27
slug = "install-gstreamer-srt-plugin-on-macos"

[taxonomies]
categories = ['gstreamer']
tags = ['gstreamer', 'howto', 'multimedia']
+++

Today I was working on a project that uses [GStreamer](https://gstreamer.freedesktop.org/) and reads content using the [SRT protocol](https://www.srtalliance.org/) on my macOS. The [SRT elements](https://gstreamer.freedesktop.org/documentation/srt/index.html?gi-language=c) could not be found in my system after installing GStreamer using [Homebrew](https://brew.sh/). I’ve installed all the GStreamer sub-packages from Homebrew.
```
    $ brew install gstreamer gst-plugins-base \
        gst-plugins-good gst-plugins-bad \
        gst-plugins-ugly gst-libav \
        gst-rtsp-server gst-editing-services
```

Still, I could not find the `strsrc` element, for example.
```text
    $ gst-launch-1.0 -v srtsrc uri="srt://127.0.0.1:7001" ! fakesink
    WARNING: erroneous pipeline: no element "srtsrc"
```

For some reason, not clear to me at the time, I did not have the plugin installed. This triggered me to look at the source code of GStreamer to find how the element is enabled. I know that GStreamer contains many plugins that depend on different third-party libraries. The SRT set of elements, resides in the [`gst-plugins-bad`](https://gitlab.freedesktop.org/gstreamer/gstreamer/-/tree/main/subprojects/gst-plugins-bad) bundle. Then it was clear to me that the SRT elements are only compiled if the [libsrt](https://github.com/hwangsaeul/libsrt) is available in the host system at compilation time.

![](/wp-content/uploads/2022/10/20220627-meson-if-gst-plugins-bad-1024x443.png)GStreamer meson file showing that it only enables the SRT element if the dependency is found.

Ok, now I know what might be causing the SRT plugin to not be available on my GStreamer’s brew installation. In order to confirm that, I checked the Homebrew formula for its dependencies.

[![](/wp-content/uploads/2022/10/20220627-missing-srt-as-dependecy-1024x521.png)](https://github.com/Homebrew/homebrew-core/blob/08c288c9042fd6d8b71c3104c24224473753fa5d/Formula/gst-plugins-bad.rb#L23-L38)

As I was guessing, libsrt is not a dependency of that formula. This means that the meson configuration we saw earlier is not letting the SRT plugin in the compilation process.

## The fix

We need to modify the `gst-plugins-bad` formula locally and then install from source.

First, we uninstall the `gst-plugins-bad` formula.
```
    $ brew rm gst-plugins-bad
```

Then we can edit our local formula to add the `libsrt` dependency. This is not strictly required, as we could just install libsrt manually and then recompile from source. But we will add here anyway, so we make sure we will not override this next time the package update. The following command will open your default editor as defined in the `EDITOR` environment variable.
```
    $ brew edit gst-plugins-bad
```

Add the line below to the dependency list:
```
    depends_on "srt"
```

We now install the package from source.
```
    $ brew reinstall --build-from-source gst-plugins-bad
```

That's it. Now you should have the SRT plugin installed and all its elements will be available in your system. We can double-check that by inspecting the one element, like the `srtsrc`.
```
    $ gst-inspect-1.0 srtsrc
```

You should see something like:

![](/wp-content/uploads/2022/10/20220627-inspect-srtsrc-element-1024x614.png)

Yay! That is it. Now I can continue my work and have all the SRT elements available on my macOS GStreamer installation from Homebrew.

![](/wp-content/uploads/2022/10/20220627-pipelineworking.png)