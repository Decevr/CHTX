# CHTX

CHTX is a catalog of character portraits and a short character line for each one. It is a prompting guide for ComfyUI and Forge.

Pick a character, copy the line, and paste it into your own prompt. The line names the character and the series, so the picture uses that character. Your prompt sets the scene. A second copy button has the Danbooru character tags. Gelbooru uses the same character tags.

The catalog has 823 portraits. Categories are Anime, Marvel, DC, Disney, Pixar, Pokemon, Video Games, and Cartoons. Search finds a character by name or series. Browse shows the portraits, and Categories opens one group at a time. Style shows the same kind of portrait in each look. Copy adds only that style line to your own prompt.

The banner shows the CHTX wordmark over character portraits. DecervCo is the small name at the bottom right of the banner.

CHTX stores the catalog in the app. Browsing and copying work without an account.

## Install on Windows

1. Download [CHTX-Setup-1.6.2.exe](https://github.com/Decevr/CHTX/releases/download/v1.6.2/CHTX-Setup-1.6.2.exe).
2. Open the file and choose Install.
3. If Windows says the publisher is unknown, choose More info, then Run anyway.
4. Open CHTX from the desktop shortcut or the Start menu.

The installer does not need an administrator login. It puts CHTX in your user folder and adds the shortcuts. To remove it, open Start, go to CHTX, and choose Uninstall CHTX.

## Install on Android

1. Download [chtx-1.6.2.apk](https://github.com/Decevr/CHTX/releases/download/v1.6.2/chtx-1.6.2.apk).
2. Open the file. If Android asks, allow install from the browser.
3. Install, then open CHTX.

The app is sideloaded from this release. It is not on the Play Store. A newer install replaces the older one.

## What you copy

Open a character to see the portrait, the name, and the series.

- Character line: `Usagi Tsukino from Sailor Moon`
- Danbooru tags: `tsukino_usagi, bishoujo_senshi_sailor_moon`

Paste the character line with your own prompt in ComfyUI or Forge. Copy the tags when the model takes Danbooru or Gelbooru tags.

## Build from source

The Android project needs JDK 17 and Android SDK 35. Put your SDK path in `local.properties`:

```
sdk.dir=C:/path/to/Android/sdk
```

Then run:

```
gradle assembleDebug
```

The installable file is `app/build/outputs/apk/debug/app-debug.apk`.

The Windows installer is built on Windows:

```
powershell -ExecutionPolicy Bypass -File windows\build-setup.ps1
```

That writes `dist/CHTX-Setup-1.6.2.exe`. The `dist` folder stays on the machine that built it.
