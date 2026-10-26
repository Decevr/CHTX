# CHTX

A phone catalog of character portraits and a short character line for each one. Paste that line with your own prompt in ComfyUI or Forge so the picture uses that character.

The menu has Browse and Categories. A search bar on the main screen finds a character by name or series. Open a character to see the portrait, the name, the series, and the character line. Copy the sentence or the Danbooru tags.

## Install on a phone

1. Open the [v1.5.0 release](https://github.com/Decevr/chtx/releases/tag/v1.5.0) on the phone while signed in to this GitHub account.
2. Download `chtx-1.5.0.apk`.
3. Open the file. If Android asks, allow install from the browser.
4. Install, then open CHTX.

This repository is private. The release download requires the Decevr GitHub login.

## What is in the catalog

744 portraits from the lookbook. Categories are Anime, Marvel, DC, Disney, Pixar, Pokemon, Video Games, and Cartoons. The sentence is the character name and series. The tags are the Danbooru character tags, which Gelbooru uses too.

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

## Desktop

The CHTX shortcut opens `app/src/main/assets/www/index.html` from this repo. That page is the desktop copy, so it matches the phone catalog. The banner shows the chrome CHTX wordmark over the character portraits, with DecervCo in small type at the bottom right.
