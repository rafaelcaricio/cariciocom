+++
title = "Readable Rust: Combinators vs. Match Clauses"
date = 2023-03-18
slug = "readable-rust-combinators-vs-match-clauses"

[taxonomies]
categories = ['programming', 'rust']
tags = ['opnion', 'rust']
+++

When writing code in any programming language, choosing the appropriate constructs is crucial for creating readable and maintainable code, and in Rust is no different. In this post, I will discuss a specific dilemma I find myself thinking often about: deciding between using combinators or match clauses.

Let's consider an example where in an application we need to retrieve the value of an environment variable, convert it to a map, and then serialize it to JSON. The first approach uses combinators and closures:
```rust
    std::env::var("SELECTOR")
        .ok()
        .and_then(|env_var| selector_field(env_var.as_str()).ok())
        .map(|sel_map| serde_json::to_value(sel_map).unwrap())
```

I ignore the declaration of the `fn selector_field(&str) -> Option<BTreeMap<String, String>>` function for simplification. This version is concise and elegant, but doesn't log any warnings if and for what reason the result turns out to be `None`. To add some context and make it easier for debugging, we can log some useful information. We can modify the code like this:
```rust
    std::env::var("SELECTOR")
        .map_err(|err| {
            log::warn!("Failed to find environment configuration for selector: {}", err);
        })
        .ok()
        .and_then(|env_var| {
            selector_field(env_var.as_str())
                .map_err(|err| {
                    log::warn!("Failed to parse selector: {}", err);
                })
                .ok()
        })
        .map(|sel_map| serde_json::to_value(sel_map).unwrap())
```

While functional, this version feels convoluted and harder to read due to the nested closures. In such cases, I tend to use a match clause, as I think it is a better option:
```rust
    let env_var = match std::env::var("SELECTOR") {
        Ok(env_var) => env_var,
        Err(err) => {
            log::warn!("Failed to find environment configuration for selector: {}", err);
            return None;
        }
    };
    let sel_map = match selector_field(env_var.as_str()) {
        Ok(sel_map) => sel_map,
        Err(err) => {
            log::warn!("Failed to parse selector: {}", err);
            return None;
        }
    };
    Some(serde_json::to_value(sel_map).unwrap())
```

This version is more readable and easier to understand. Thus, I think it's useful to consider the following guidelines when choosing between combinators and match clauses:

  1. If you need to add multiple lines of code inside the closures when using combinators, a match clause might be a better choice.
  2. When error handling is minimal or not needed (conversion to `Option` or use of `?` is possible) and simple closures can be used in combinators, combinators are a good choice.



Combinators in Rust are a powerful tool for writing concise and functional code, but sometimes a match clause is still the better choice for readability. When deciding between the two, consider the complexity of error handling and the need for multiple lines of code inside closures used in combinators. By striking the right balance, we can create more readable and maintainable Rust code.