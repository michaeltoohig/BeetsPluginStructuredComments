[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE.txt)

# Structured Comments (Beets Plugin)

This plugin is not yet built and not safe to use yet!

The *beets-structuredcomments* plugin lets you define a format that your media files' comments field will adhere to allowing you to ensure your media files will have the information you defined in beets available at a glance outside of beets.


## Basic Idea

I found when taking my beets library to DJ with software such as ReckordBox I want to know the information I defined such as `context` or `rating` but obviously those are not available. I believe I can override the comments field with more details and therefore have some of that information outside of beets itself.

I'm thinking the configuration of `structuredcomments` will have a formatted string such as `paths` configuration or `format_item` where I can define what information I want in my comments field.

An example configuration concept

```
structuredcomments:
  format_str: '[$rating]:$context $tags - $comments'
  fields:
    - rating:
      missing: '-'
    - context:
      case: 'upper'
      length: 3
      missing: 'UNK'
    - tags:
      append: '#'
```

This configuration will likely change but provides the following:
  - Individual fields can have additional configuration about how they are formatted
    - case: sets how the string is written
    - length: can limit the string length to keep consistent spacing between fields in the comments
    - missing: defines what to place when the media file does not have that information defined
    - append: Adds a string to the beginning of each item in the list (if $tags is a list). So when searching in DJ software I can search `#acid` to find songs I tagged with `acid` but not find any titles, artists, genres, etc that contain the string `acid` in the DJ software search.
  - The original media file comment can be added to the structured comments. This will cause some challenges during development.


## Installation

You can try cloning this repo yourself, but this repo is not yet safe to use on your library.


## Usage
Activate the plugin in your configuration file:

```yaml
pluginpath:
  - /path/to/BeetsPluginStructuredComments/beetsplug
  # [...]

plugins:
  - structuredcomments
  # [...]
```

Check if plugin is loaded with `beet version`. It should list 'structuredcomments' amongst the loaded plugins.

Your default configuration is:
```yaml
structuredcomments:
  pass
```


### Examples:
 

## Issues
If something is not working as expected please use the Issue tracker.
If the documentation is not clear please use the Issue tracker.
If you have a feature request please use the Issue tracker.
In any other situation please use the Issue tracker.


## Acknowledgements
Many thanks to the developer of the [beets-template](https://github.com/adamjakab/BeetsPluginTemplate) for the Beets Plugin skeleton.


## Final Remarks
This plugin is still in development and not yet safe for use!
