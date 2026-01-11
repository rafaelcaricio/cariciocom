+++
title = "A brief introduction to GStreamer"
date = 2022-10-29
slug = "a-brief-introduction-to-gstreamer"

[taxonomies]
categories = ['gstreamer', 'programming', 'rust']
tags = ['gstreamer', 'multimedia', 'rust']
+++

A while ago, I started working with [GStreamer](https://gstreamer.freedesktop.org/). I wasn't familiar with the framework  
before, and took me a while to grasp how it works. I have recently created a mental model which has been helping me understand how to use GStreamer API and I thought sharing it here could also help others.

GStreamer is a multimedia framework. It is meant to be used to create applications that can manipulate multimedia content. We don't usually manipulate the multimedia content in GStreamer directly, we orchestrate elements that deal with the content. GStreamer provides us with an API for orchestrating those elements. There are various types of elements: from audio and video encoding, decoding, demuxing, muxing to closed captions, image compositions and all kinds of metadata. There are [over 90 elements](https://tw.homeservice.click/gstreamer/status/1584612782150135810) available in the official GStreamer distribution. It is likely that you'll find elements for most, if not all, the operations you might want to do.

## Element types

When working with GStreamer you start with building a pipeline and using some elements to process your content. Building a pipeline consists generally of creating and connecting elements you need in a meaningful way. For example, to play a file, we need to read its content then decode the content to raw audio and send the raw audio to an audio device.

In GStreamer there are a few general types of elements which can be categorized according to the way they connect with each other. Elements connect using a single or multiple pads which provide input and output streams of content. Input pads are called sink pads, and output pads are called source pads.

### Source elements

![](/wp-content/uploads/2022/10/Untitled-Source-Element_small.jpg)Source elements have a single source pad always available.

Read from external resources or produce content themselves. Source elements have one output stream or pad (source pad) available at all times (known as static pad). They do not accept any content as input (no sink pads).

### Destination elements

![](/wp-content/uploads/2022/10/Untitled-Source-Element-3.jpg)Sink elements have a single sink pad always available.

Destination elements, also known as sinks, are elements that receive a single stream of content. They don't produce any content out (no source pads). They usually have a single input (sink) pad available at all times (static pad).

### Demuxer elements

![](/wp-content/uploads/2022/10/Untitled-Source-Element-0.jpg)Demuxer elements have a single sink pad always available and possibly multiple source pads created later on demand.

Demuxer elements usually receive one stream of content and split the content into multiple output streams. They usually have a single input (sink) pad available at all times and will create new output (source) pads as soon as they figure out what types of content are available in the stream it's receiving.

### Muxer elements

![](/wp-content/uploads/2022/10/Untitled-Source-Element-2.jpg)Muxer elements have a single source pad always available and multiple sink pads created later on demand.

Muxer type elements receive multiple streams (sink pads) of content and mix them together into a single output stream (source pad). Muxers usually have an output (source) pad available at all times. Whenever we want a muxer to process some content, we need to request new input (sink) pads to be created.

### Filter elements

![](/wp-content/uploads/2022/10/Untitled-Source-Element-1.jpg)Filter elements have a sink and a source pad always available.

Filter elements generally have a single input (sink) pad and a single output (source) stream pad. The pads in a filter element are usually static (always available).

## Multimedia manipulation using pseudocode

You now know about elements and their most common types. How to put them together? In GStreamer, elements usually connect inside a container (or bin) called a pipeline. We put elements into it and use API calls to make the elements connect. Let's say we want to play music from a file. We need to read the file, decode the content to raw audio, then send this content to an audio device. Here's a pseudo pipeline with made-up elements:

![](/wp-content/uploads/2022/10/Example-Pipeline.jpg)

Inspired by Javascript and HTML manipulation, one could imagine pseudocode like this:
```rust
    // Create our pipeline container
    let pipeline = createElement("pipeline");
    
    // Create our elements
    let file_reader = createElement("filesource");
    file_reader.setAttribute("location", "/Users/rafaelcaricio/astronaut.wav");
    
    // Generic decoder which is similar
    // to a demuxer type of element
    let decoder = createElement("decoder");
    let audio_device = createElement("audiodevice");
    
    // Add all elements to the Pipeline container
    pipeline.appendChild(file_reader);
    pipeline.appendChild(decoder);
    pipeline.appendChild(audio_device);
    
    // Tell our elements how to connect
    file_reader.link(decoder);
    
    // The demuxer type of elements only create pads
    // after it is able to get some content, so we
    // add a event listener here to link later on
    // whenever the new stream pad is available
    let audio_device_pad = audio_device.getDestinationPad();
    decoder.addEventListener("streamFound", function (stream_source_pad) {
        stream_source_pad.link(audio_device_pad);
    })
    
    pipeline.dispatchEvent("playing");
    
    pipeline.waitUntilEnd();
    
    pipeline.dispatchEvent("stop");
```

In this pseudocode, we are creating elements and manipulating them to connect together inside a pipeline container. If you have ever worked with web development, this should look familiar. This is comparable with how you will be thinking when working with GStreamer.

## Using the GStreamer API

Let's translate this example to real GStreamer code to play a WAV file. We need to select our elements for every operation we want to do: read from a file, decode the content, send to an audio device. For those, we have `filesrc`, `decodebin`, `autoaudiosink` respectively.

  * `[filesrc](https://gstreamer.freedesktop.org/documentation/coreelements/filesrc.html?gi-language=c#filesrc-page)`: Reads content from a file and has one output pad.
  * `[decodebin](https://gstreamer.freedesktop.org/documentation/playback/decodebin.html?gi-language=c#decodebin-page)`: An abstract element that identifies the content received, and puts together other elements to decode the content and then create new pads with the types of content which are available.
  * `[autoaudiosink](https://gstreamer.freedesktop.org/documentation/autodetect/autoaudiosink.html?gi-language=c)`: Selects the first available audio output device and sends the received audio content to be played.



Using GStreamer API in [Rust](https://www.rust-lang.org/) it looks like this:

{% wide_container() %}
```rust
    fn main() {
        gst::init().unwrap();

        // Create our pipeline container
        let pipeline = gst::Pipeline::default();

        let file_reader = gst::ElementFactory::make("filesrc").build().unwrap();
        file_reader.set_property("location", "/Users/rafaelcaricio/astronaut.wav");

        let demuxer = gst::ElementFactory::make("decodebin").build().unwrap();
        let audio_device = gst::ElementFactory::make("autoaudiosink").build().unwrap();

        pipeline.add(&file_reader).unwrap();
        pipeline.add(&demuxer).unwrap();
        pipeline.add(&audio_device).unwrap();

        file_reader.link(&demuxer).unwrap();

        // Our event listener to connect pads later on
        let audio_device_pad = audio_device.static_pad("sink").unwrap();
        demuxer.connect_pad_added(move |_, pad| {
            pad.link(&audio_device_pad).unwrap();
        });

        pipeline.set_state(gst::State::Playing).unwrap();

        // Wait until end, handle errors, etc
        let bus = pipeline.bus().unwrap();
        for msg in bus.iter() {
            match msg.view() {
                MessageView::Eos(..) => break,
                MessageView::Error(err) => {
                    println!("Oh no.. something wrong happened: {:?}", err);
                    break
                }
                _ => continue,
            }
        }

        pipeline.set_state(gst::State::Null).unwrap();
    }
```
{% end %}

As you can see, the fake JavaScript API we created for manipulating elements (like they would be HTML elements) and the real GStreamer API are analogous. The GStreamer API is vast and provides many operations to manipulate elements inside pipelines or inside other elements (also called bins). There are elements for many different operations you might want to do, not only conversion of content types.

Here I generated a visualization of the GStreamer pipeline we wrote:

[![](/wp-content/uploads/2022/10/example-pipeline-diagram-1024x155.png)](/wp-content/uploads/2022/10/example-pipeline-diagram.png)

I like to think of elements as functionalities that we can piece together like LEGO blocks. If a source pad is of the same type as the sink pad, then they can connect. Pad types are called capabilities (or simply "caps") in GStreamer and are compatible when they have compatible fields. Caps [look very much like mime-types](https://gstreamer.freedesktop.org/documentation/plugin-development/advanced/media-types.html?gi-language=c#table-of-audio-types) that we see in the HTTP header `Content-Type`. An example of caps is `audio/x-wav` which means an audio content in WAV format or `video/x-raw,format=RGBA,width=480,height=320,framerate=30/1` which - you guessed it - is a decoded raw video content in RGBA format with the sizes and frame rate specified.

## Conclusion

I hope this brief introduction has given you a good high-level overview of basic concepts that might help you jump start writing your own GStreamer multimedia processing pipelines. I recommend checking out the GStreamer documentation and browsing a little through [some of the elements](https://gstreamer.freedesktop.org/documentation/plugins_doc.html?gi-language=c), something might catch your eye. There is [extensive documentation](https://gstreamer.freedesktop.org/documentation/application-development/index.html?gi-language=c) and [tutorials available in C](https://gstreamer.freedesktop.org/documentation/tutorials/basic/hello-world.html?gi-language=c) and [Rust](https://gitlab.freedesktop.org/gstreamer/gstreamer-rs/-/tree/main/tutorials/src/bin) that delve further into the concepts I introduced in this blog post. I've also created a basic GStreamer [project template](https://github.com/rafaelcaricio/gstreamer-rust-project-template) that you can use. The GStreamer community is very friendly and welcoming to newcomers. We usually hang around at the official GStreamer [IRC chat](irc://irc.oftc.net/gstreamer) which can be accessed using [the matrix.org bridge](https://matrix.to/#/#_oftc_#gstreamer:matrix.org). Feel free  
to say "hi". See you around!