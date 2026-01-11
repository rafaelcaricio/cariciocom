+++
title = "My Late-Night Hack with iOS Shortcuts and AI"
date = 2025-01-11
slug = "building-a-cultural-bridge-my-late-night-hack-with-ios-shortcuts-and-ai"

[taxonomies]
categories = ['ai', 'automation-tool', 'programming', 'prompt-engineering']
tags = ['ai', 'ios', 'late-night', 'prompt-engineering', 'shortcuts']
+++

You know those moments right before falling asleep when your mind wanders and suddenly you get an idea you just have to try out? That's exactly what happened to me last night. Living in Amsterdam as a non-Dutch speaker, I've struggled to keep up with local news and understand the cultural context behind the stories. Sure, I could use Google Translate, but I wanted something more… comprehensive.

## The problem

As an immigrant in The Netherlands, I face two main challenges:

  1. The language barrier (I am still studying Dutch, but nowhere near being proficient enough to read a whole article)
  2. Understanding the cultural context behind news stories



## The spark

I remembered that iOS has this feature called Shortcuts that lets you create automations by connecting different app actions together. What caught my attention was that both Claude and ChatGPT have APIs that can be accessed through Shortcuts. This got me thinking – what if I could create a simple tool to help me better understand Dutch news articles?

## The Solution: A 10-Minute Hack

Building upon an existing shortcut I had for removing ads from web pages, I put together a multi-step workflow that does the following:

  1. Takes a Safari webpage as input
  2. Cleans up the content (removes ads, navigation, footers)
  3. Translates the article from Dutch to English
  4. Provides additional context like:
     * Cultural references explained for foreigners
     * Sentiment analysis
     * How a native Dutch person might react to the topic
     * A concise summary of the main points



The best part? It took only about 10 minutes to put together, all done on my phone!

## The Technical Bits

What makes this interesting from an engineering perspective is the multi-step prompt technique I used. The workflow is split into two main steps:

  1. First prompt: Clean up and extract only the relevant article content
     * Removes all the noise (text from overlays, menus, footers, etc)
     * Extracts just the article title and body
     * Outputs clean content
  2. Second prompt: Process and enhance the content
     * Translates the clean content to English
     * Adds cultural context
     * Provides additional insights



The result gets saved directly to the Notes app for easy access and historical view.

![](/wp-content/uploads/2025/01/notesappview-medium.jpeg)

## Why Multi-Step Prompting?

You might wonder why I split this into multiple steps instead of doing everything in one go. The answer lies in the "garbage in, garbage out" principle. By first cleaning up the input text, we ensure that the AI model only works with relevant content, leading to better quality outputs.

## Why This Matters

Now, this isn't about becoming a "prompt engineer" – that's not the point. As software engineers, we're constantly looking for tools that can increase our productivity. Just like we use linters to catch known issues in our code, or how we rely on helpful compiler messages from Rust or Python to guide us through error resolution, I see this as just yet another tool.

The real value here isn't in the prompts themselves, but in identifying opportunities where AI can help solve real-world problems we face. In my case, it was about breaking down the language barrier and cultural gap I experience living in the Netherlands.

## Try It Yourself

I've recorded a quick demo of the tool in action. You can install the shortcut and try it yourself by using the [Claude version of the Shortcut](https://www.icloud.com/shortcuts/6170ae3f58dc4e42b075307ad152a135) or the [ChatGPT version](https://www.icloud.com/shortcuts/fe65676260904e5e9990af0e898ff78c). Feel free to modify the prompts for your own needs with different languages and countries.

https://youtube.com/shorts/Qdv4fHdBfOw?si=io3TeGQurtY0IYyE

{{ alert(type="note", icon="info", title="Prerequisites", text="You'll need to have either Claude or ChatGPT installed on your iOS device to use this tool.") }}

Sometimes the best solutions come from scratching your own itch, even if it's right before bedtime. This is not my first time, and I don't expect it to be the last. 😴

Have you built any interesting shortcuts or tools to help with in your everyday life and leveraged LLMs for it? I'd love to hear about them, you can find me on [BlueSky](https://rafaelcaricio.eu), [the Fediverse](https://nullpointer.social/@rafaelcaricio), [LinkedIn](https://www.linkedin.com/in/rafaelcaricio/) or [GitHub](https://github.com/rafaelcaricio).