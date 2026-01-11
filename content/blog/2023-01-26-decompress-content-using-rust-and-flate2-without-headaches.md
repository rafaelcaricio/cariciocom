+++
title = "Decompress content using Rust and flate2 without headaches"
date = 2023-01-26
slug = "decompress-content-using-rust-and-flate2-without-headaches"

[taxonomies]
categories = ['rust']
+++

A few days ago I had to deflate some compressed content using Rust. I quickly found the [flate2](https://crates.io/crates/flate2) crate, it is well maintained and has a very high usage. I decided it would be a great fit for my little project, a CLI tool to download, decompress, and store in a local SQLite3 some content from AWS S3.

I wrote my small CLI tool, and it seemed to work perfectly on the first run. It was all nice until some time later. I have noticed that some lines of my compressed file were missing. The code was running fine and didn't provide any warnings. After a few hours of debugging, I was sure there was a bug in my code somewhere. I went on and wrote a bunch more test to try to isolate in a reproducible way, where the problem was present, without any luck. All tests passing and no indication of problems anywhere.

At some point, I decided to use a sample from the original compressed files, and that is how I managed to reproduce the bug. The sample code in the README of the flate2 crate was what I used in my code:
[code] 
    use std::io::prelude::*;
    use flate2::read::GzDecoder;
    
    fn main() {
        let mut d = GzDecoder::new("...".as_bytes());
        let mut s = String::new();
        d.read_to_string(&mut s).unwrap();
        println!("{}", s);
    }
[/code]

Unfortunately, the `GzDecoder` cannot successfully decompress my files. I went then to the official library repository and found [this issue](https://github.com/rust-lang/flate2-rs/issues/301) which describes exactly my problem. I had to use the `MultiGzDecoder` instead, it all worked as expected after this change and I could decompress successfully my files. The example in the README of flate2 should probably be this:
[code] 
    use std::io::prelude::*;
    use flate2::read::GzDecoder;
    
    fn main() {
        let mut d = MultiGzDecoder::new("...".as_bytes());
        let mut s = String::new();
        d.read_to_string(&mut s).unwrap();
        println!("{}", s);
    }
[/code]

Finally, I still don't know why the `MultiGzDecoder` works when the `GzDecoder` don't. If you know, I will update this blog with your answer.