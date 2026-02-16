+++
title = "An Exercise in Agentic Coding: AV1 Encoder from Scratch in Rust"
date = 2026-02-16
slug = "an-exercise-in-agentic-coding-av1-encoder-from-scratch-in-rust"

[taxonomies]
categories = ['multimedia', 'rust']
tags = ['agentic-coding', 'video', 'codecs', 'av1']

[extra.social_media_image]
path = "demo-web-ui.avif"
alt_text = "The wav1c demo page, realtime AV1 encoding in the browser with WASM"
+++

It's a contentious time to be a software engineer. Some of us really love agentic coding, others hate it with passion. Some say it makes them super-productive, for others it's just useless slop.
Little over a year ago, I thought agentic coding was just a fad, I was even annoyed by the AI auto-complete. That is, until I tried [Cline (VS Code plugin)](https://cline.bot/) in November 2024. It was then that I realized tools for writing software were changing and I needed to start paying closer attention. I'm an extremely curious person and anyone who has ever worked with me knows I can sometimes get obsessed with a new technology, with learning about it and experimenting with it.

Fast forward to 2025, I've been doing a lot of agentic coding using Claude Code but it was mostly basic usage that demanded a lot of steering. Oftentimes I would end up writing the code myself. However, I noticed a significant leap when Claude Opus 4.5 was released. I actually liked the code the model was producing and it made me want to push it further and come up with cool new ideas on what to build with it. 

I wanted to create something more impressive to me than, say, a React/Three.js single-page animation. What task would be so complex that it would normally take a year or more of my spare time? That would be a true challenge! Perhaps something that would resonate with my peers in the multimedia space…? That's when I thought about an AV1 encoder. Written in Rust, of course, with no dependencies, and no unsafe code. It was just a gamble, but even though I made an effort setting up the task, I had little confidence the model would succeed. I then ended up with a working version of it in less than 12 hours. 😳

<figure style="text-align: center;">
  <video controls playsinline width="320" height="240" style="display: block; margin: 0 auto;">
    <source src="wav1c-demo.mp4" type="video/mp4">
  </video>
  <figcaption style="font-size: 0.85em; opacity: 0.7; font-style: italic;">This is me encoded with wav1c (initial version)</figcaption>
</figure>

It's not the best AV1 encoder by any measure, nor the fastest. The point is: I was able to develop a usable AV1 encoder in less than a day. It is specification compliant and we can decode the resulting bitstream with [dav1d](https://code.videolan.org/videolan/dav1d), hardware decoder via macOS VideoToolbox API and, potentially, by any other AV1 decoder (I haven't tested all of them myself. If you do, let me know). To me, this was an astonishing exercise, as writing video encoders (even a bad one), is not a "less than a day" kind of task. Even more so, when we're talking about [a production video codec like AV1](https://netflixtechblog.com/av1-now-powering-30-of-netflix-streaming-02f592242d80).

I still need to reflect more on the implications of my exercise. Specification-based development seems to be a great fit for agentic coding with a self-verification loop, encode/decode. A lower bar for custom encoders/decoders could mean being able to create custom encoding profiles that go beyond just a change of parameters, e.g. having a custom transform or prediction logic baked into the encoder, as opposed to simply tweaking qp/rate-control knobs. Trimmed down encoders/decoders could also be used in embedded devices or embedded on a website. I created a [simple demo](https://rafaelcaricio.github.io/wav1c_demo/) to show how wav1c (Wondrous AV1 Coder) [compiled to WASM](https://github.com/rafaelcaricio/wav1c/tree/main/wav1c-wasm) can encode to AV1 in real time, no server-side processing needed. I added some stats so that we can take a closer look at what is going on. Do not expect high quality images, but it absolutely works. You can download the MP4 file and play it in VLC or QuickTime (if you have AV1 hardware support as of M3 or more recent MacBook). Even without any practical applications, this code base can also be used simply for learning and to spark creativity.

<figure style="text-align: center;">

[![Demo web UI](demo-web-ui.avif)](https://rafaelcaricio.github.io/wav1c_demo/)

  <figcaption style="font-size: 0.85em; opacity: 0.7; font-style: italic;">The wav1c demo page, realtime AV1 encoding in the browser with WASM.</figcaption>
</figure>

<details>
<summary title="Click me for a fun fact">🥚🐰 Click me for a fun fact</summary>

This screenshot is an AVIF file encoded with wav1c itself.

```bash
./ffmpeg -y -i Screenshot.png -c:v libwav1c -wav1c-q 1 demo-web-ui.avif
```

</details>

If you want to try locally, I also included [a patch file](https://github.com/rafaelcaricio/wav1c/blob/main/ffmpeg-libwav1c.patch) you can apply and use wav1c with FFmpeg.

```bash
# Build the wav1c static library
cargo build -p wav1c-ffi --release

# Clone and patch FFmpeg
git clone https://git.ffmpeg.org/ffmpeg.git
cd ffmpeg
git apply /path/to/wav1c/ffmpeg-libwav1c.patch

# Configure with libwav1c (adjust library path as needed)
./configure --enable-libwav1c \
  --extra-cflags="-I/path/to/wav1c/wav1c-ffi/include" \
  --extra-ldflags="-L/path/to/wav1c/target/release"

make -j$(nproc)

# Encode
./ffmpeg -i input.y4m -c:v libwav1c -wav1c-q 64 output.mp4
```

You can embbed wav1c in your Rust project, or embedded microcontroller firmware. The Rust API is very straight forward to use:

```rust
use wav1c::{Encoder, EncoderConfig, FrameType};
use wav1c::y4m::FramePixels;

let config = EncoderConfig {
    base_q_idx: 128,
    keyint: 25,
    target_bitrate: None,
    fps: 25.0,
};

let mut encoder = Encoder::new(320, 240, config).unwrap();
let frame = FramePixels::solid(320, 240, 128, 128, 128);

encoder.send_frame(&frame).unwrap();
let packet = encoder.receive_packet().unwrap();

assert_eq!(packet.frame_type, FrameType::Key);
// packet.data contains raw AV1 OBUs (TD + SequenceHeader + Frame)
```

It's a contentious but absolutely [fascinating time to be a software engineer](https://open.spotify.com/episode/2ilPuZvpudECHieL0sqnzT). A friend told me last week, the LLM model I'm using today is the worst model I will ever use. I reckon he's right and that doesn't faze me in any way, it urges me to keep on top of it. I want to learn more and know how to better take advantage of these *tools* in my work. Because these are tools, just like a code linter or `cargo clippy` are. They don't replace my creativity, they allow me to take on more ambitious and increasingly complex challenges. I'm accountable for what I create and I care deeply about the result of my work, whether or not it's developed using Turbo Pascal, Vim, NeoVim, IntelliJ, VS Code, or Claude Code.

