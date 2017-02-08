# SassSolution
Sublime plugin to autocomplete all SASS vars and mixins in files you set in the setting file  

![](https://raw.githubusercontent.com/ahmedam55/SassSolution/master/sass-solution-gif.gif)

# Easy installation
You can install **SassSolution** through the [Package Control](https://packagecontrol.io/installation).

1. Press <kbd>cmd/ctrl</kbd> + <kbd>shift</kbd> + <kbd>p</kbd> to open the command palette.
2. Type *"install package"* and press enter. Then search for *"Sass Solution"*

# Manual installation

1. Download the [latest release](https://codeload.github.com/ahmedam55/SassSolution/zip/master), extract and rename the directory to **"SassSolution"**.
2. Move the directory inside your sublime `Packages` directory. **(Preferences > Browse packages...)**

# Configuration
To use the autocompletion you have to define path(s) in the plugin settings so the plugin knows what to parse.
The easiest way is right clicking a folder or file in the sidebar and choose `SassSolution` > `Add to AutoComplete`.
This will add the appropriate path to your user settings of Sass Solution:
```
{
    "files": [],
    "folders": ["/Users/sassninja/Development/testProject"]
}
```

Apart from that you must choose **SCSS syntax** in the editor when you want to use the autocompletion. You can use the plugin [SCSS](https://packagecontrol.io/packages/SCSS) if you can't choose it yet. SASS syntax doesn't work because Sass Solution currently only supports SCSS.