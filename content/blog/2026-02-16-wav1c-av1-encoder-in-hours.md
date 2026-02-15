+++
title = "wav1c - Rust AV1 encoder implementation in less than 24 hours"
date = 2026-02-15
slug = "wav1c-rust-av1-encoder-implementation-in-less-than-24-hours"

[taxonomies]
categories = ['multimedia']
tags = ['agentic-coding', 'video', 'codecs', 'multimedia']
+++

It is a contentious time to be a software engineer, some people love agentic coding and some hate it. People say they are super-productive, others say it is just useless slop. Over a year ago I thought agentic coding was a fad, I was even annoyed by the AI auto-complete. Until I tried [Cline (VS Code plugin)](https://cline.bot/) in November 2024. Since then I realized that tools for writing software were changing and I needed to pay attention. I'm a curious person and love to learn new technologies. Whoever worked with me (or knows me well) is aware that I sometimes get obsessed about things and love to experiment.

Fast-forward, I tried a lot of agentic coding using Claude Code, but mostly it was quite basic usage or plus it demanded a lot of steering. Many times I would choose to write code myself. But since the release of Claude Opus 4.5, I noticed a leap, it required a lot less steering. I liked the code the model was producing and that made me want to push further on what to build with it.

I wanted something more impressive to me than a React/Three.js single-page animation. I asked myself what could be some complex task that I know it would take me a year or more of my hobby time. Something that could resonate with my peers in the multimedia space: AV1 encoder. In Rust (of course), no dependencies, no unsafe code. I was pretty confident the model would fail. Then I arrived at a working version in less than 12 hours. 😳

[Video Player HLS.js?]

It is not the best AV1 encoder by any measurement, nor it is the fastest, and many other flaws. The point here is that I could develop a usable AV1 encoder in less than a day. It is specification compliant and we can decode the resulting bitstream with [dav1d](https://code.videolan.org/videolan/dav1d), hardware decoder via macOS VideoToolbox API, and potentially by any other AV1 decoder (I haven't tried all of them myself, so I will let you exercise this and let me know). This is fascinating to me as writing video encoders, even a bad one, is not a "less than a day" task, especially when we are talking about [a production video codec like AV1](https://netflixtechblog.com/av1-now-powering-30-of-netflix-streaming-02f592242d80).

I still need to reflect more about what the implications of this are. Specification based development seems to be a great fit for agentic coding with a self-verification loop, encode/decode. A lower bar for custom encoders/decoders could mean custom encoding profiles that go beyond a change of parameters. Like custom transform or prediction logic baked into the encoder, as opposed to just tweaking qp/rate-control knobs. Also trimmed down encoders/decoders could be used in embedded devices or embedded on a website. I have also created a [simple demo](https://rafaelcaricio.github.io/wav1c_demo/) to show how wav1c (Wondrous AV1 Coder) [compiled to WASM](https://github.com/rafaelcaricio/wav1c/tree/main/wav1c-wasm) and doing encoding to AV1 in realtime. I cared to show some stats so we can look a little deeper on what is going on. Do not expect high quality images, but it absolutely works. You can download the fMP4 file and play in VLC or QuickTime (if you have AV1 hardware support as of M3 or more recent MacBook). Even without practical production uses, this is a very small codebase that can also be used for learning and to spark creativity.

![](Demo web UI)

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

You can embbed wav1c in your Rust project, or embedded microcontroller firmare. The Rust API is very straight forward to use:
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

I think this is [a fascinating time to be a software engineer](https://open.spotify.com/episode/2ilPuZvpudECHieL0sqnzT). As a friend told me after talking about this experiment, this is the worst LLM model I will use for the rest of my life. He is right and that does not scare me in any way. But it urges me to keep on top of it. I want to learn more and know how to better take advantage of those tools in my work. Those are tools that I can use like I use a code linter or `cargo clippy`. It doesn't replace my creativity, it pushes me to take on more complex challenges. I'm accountable for what I produce and I care about the result of my work whether it is developed using Turbo Pascal, Vim, NeoVim, IntelliJ, VS Code, or Claude Code.