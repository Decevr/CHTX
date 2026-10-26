# Prompt Assist

A phone catalog of the clothed character portraits and the prompt for each one. Paste a prompt into the Anima text-to-image workflow, or use the Danbooru / Gelbooru tags on Illustrious, Pony, NoobAI, and other tag models.

The menu has Browse and Categories. A search bar on the main screen finds a character by name or series. Open a character to see the portrait, name, series, sentence prompt, and tag prompt. Copy any of them to the clipboard.

## Install on a phone

1. Open the [v1.2.0 release](https://github.com/Decevr/prompt-assist/releases/tag/v1.2.0) on the phone while signed in to this GitHub account.
2. Download `prompt-assist-1.2.0.apk`.
3. Open the file. If Android asks, allow install from the browser.
4. Install, then open Prompt Assist.

This repository is private. The release download requires the Decevr GitHub login.

## What is in the catalog

744 portraits from the lookbook. Categories are Anime, Marvel, DC, Disney, Pixar, Pokemon, Video Games, and Cartoons. The sentence prompts match those clothed busts. The tag prompts use Danbooru character tags, which Gelbooru uses too. Younger characters keep their series look and do not get an adult age line.

Portrait settings: Pearly Sapphire v10, Qwen CLIP, HDR VAE, 768×1024, 20 steps, CFG 5, er_sde / simple. The Anima text-to-image graph defaults to 1024 square, 40 steps, and euler ancestral. Match the portrait settings when you want the same framing.

## Build

Requires JDK 17 and Android SDK 35.

```
sdk.dir=C:/Users/Danie/Android/sdk
```

Put that in `local.properties`, then:

```
gradle assembleDebug
```

The installable file is `app/build/outputs/apk/debug/app-debug.apk`.
