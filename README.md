## What it does?
The idea came when my taskbar and my desktop started to feel "overfloated" with lost of apps, websites and games. So after that I tought "what if I could put them all on just one small (nice) box?" then the idea for the Sortcut Manager came to my mind! "An app where you can easily organize and customize how you open your apps." 

Below are some examples of how you can organize and use the app:
![image](https://github.com/CaioEmPessoa/ShortcutManager/assets/127911795/b315e252-6a43-4930-82fa-927c41b3b9a8)

## Installing...
You can just download the .exe in the "Releases" tab and extract it anywhere.
Or if you want this normal python version, just clone this repo and install the requirements. Carefull to not run the 'save reset.py', it deletes all your data and resets the app to the defaults.

## How it does?
### Adding a shortcut
First you need to decide if you want to add a shortcut to a local app, an website or a Steam game(not necessarly) after that you'll see one of theese windows:

___
### Adding a APP:
- The name of the shortcut, if you leave it empty it'll get the name before the extension of the app path.
- The path to the app you want to open
- Optionally: The icon that will show up on the app (if you don't choose anything it will show a default icon when icons are enabled)

___
#### Adding a SITE:
- The name of the shortcut, same thing as an app if leave empty
- The link to the website, with or without https://, www, etc... but requires ".com" or ".org" at the end
- Optionally: The browser you'll want the window to open (for firefox case check [below](#firefox-case))
- Optionally: The icon that will show up on the app

<details>
  <summary open>
    
  ## *Using Firefox*
  
  </summary>
  
  The "ssb.enable" firefox funcion was disabled some time ago, so in order to make a workaround for it you'll need to create a new profile with some custom css for it:
  
  1. Go to about:profiles on your firefox and create a new profile called "Apps" (case-sensitive)
  2. Launch this new profile and go to about:config
  3. Define `toolkit.legacyUserProfileCustomizations.stylesheets` as `true`
  4. Now go back to about:profiles and open the root directory of Apps
  5. In this directory create a new folder called "chrome", and inside chrome create a file called "userChrome.css"
  6. In this userChrome.css file paste the following code:

    TabsToolbar {
      visibility: collapse;
    }
    :root:not([customizing]) #navigator-toolbox:not(:hover):not(:focus-within) {
      max-height: 1px;
      min-height: calc(0px);
      overflow: hidden;
    }
    
    #navigator-toolbox::after {
      display: none !important;
    }
    
    #main-window[sizemode="maximized"] #content-deck {
      padding-top: 8px;
    }

  7. Now your the websites should run as the chromium-based ones, just remember to write 'firefox' when adding an website.
</details>

___
#### Adding a STEAM shortcut:
- If you selected the steam generated desktop icon it will fill all the informations for you, even the icon, so I recommend just selecting the path and call it a day. (YOU CAN DELETE THE DESKTOP SHORTCUT LATER)
- Name of shortcut
- Link to the game, its usually like this: "steam://rungameid/gameid", the way you get the game id is by creating a shortcut of it in your desktop, reading the properties of the url.
- Optionally: The icon that will show up on the app

note: Yes you can add any game other than steam, you'll just need to go to its original path and add it as an "app".

___
### Adding an Shortcut Folder
Just write the name of the folder you want. You can switch them by pressing the tabs on the top of the app or using a horizontal scroll.


## Conclusion
And thats it! now you can start your apps right from Shortcut Manager, and leave your desktop and taskbar to more important things!

*also put all of your games into one simple but customizable "launcher" XD
