[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE.txt)

# Structured Comments (Beets Plugin)

This plugin is working for me but it could be improved yet.

The *beets-structuredcomments* plugin lets you define a format that your media files' comments field will adhere to allowing you to ensure your media files will have the information you defined in beets available at a glance outside of beets.


## Basic Idea

I found when taking my beets library to DJ with software such as ReckordBox I want to know the information I defined such as `context` or `rating` but obviously those are not available in music tags. I believe I can override the comments field with more details and therefore have some of that information outside of beets itself.

### Use with Rekordbox

Be sure after re-importing your music into record box to select everything then right-click and choose "Reload Tags" before the changes you've made will appear in Rekordbox.

## Installation

You can try cloning this repo yourself, but this repo may not yet safe to use on your library as it is under devloplment. So only use if you have a backup and understand what you are doing, which if you are installing this from the repo you probably are fine.

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

Then define your comments template, use the `inline` plugin to define special cases. I'll look into using the `usertag` plugin with structured comments next.

My idea is to have a unix directory like list when looking at all of my files in a table so I may see something like the following:

```
|| Title    || Genre      || Year || Comments                                 ||
| Blah blah | UK Garage   | 2008  | [3]:v-:--- ::: Vocal, Rising Energy, Deep |
| Blah Blah | Techno      | 2019  | [4]:--:HIG ::: Raw, Dark                  |
| Blah Blah | Drum & Bass | 2017  | [2]:vm:CHI ::: Liquid, Jazz, Vocal Male   |
```

Your config file will require the following for the above example structured comments:

```yaml
import:
  write: yes
  # [...]

plugins:
  - inline
  # [...]

structuredcomments:
  auto: yes
  template: '[$ifdef{rating,$rating,-}]:$vocal$vocal_gender:%ifdef{context,%left{%upper{$context}, 3},---}'
  delimiter: ':::'

# inline plugin config
item_fields:
  vocal: u'v' if 'vocal' in comments.lower() else u'-'
  vocal_gender: u'm' if 'male' in comments.lower() else u'f' if 'female' in comments.lower() else u'-'
```

The `deliminter` is the string that separates your actual comments field from the structured portion defined in the `template`. By default it is `:::`; however you can set it to whatever you want as long as it is an unique string that does not appear elsewhere in the comments field. For example a `delimiter` of `---` would not work since our `template` already defines `---` for songs with a missing `$context` field.  

The `-d` flag can be used to show you the changes structuredcomments will make before actually writing anything.

The `-f` flag can be used to force the plugin to overwrite the existing comments field even if the field is the same.

## Future Development

1. I would like to remove the requirement of a delimiter or be smart enough not to mess anything up if two delimiters were present.
2. Clean up the code and make it DRY.
3. Look for a way to define a look up table so instead of `$context` being the left first 3 characters; we could search a table to determine what we want in its place. For example a table that defines the context `Chill` would be `CHL` or `Comedown` would be `CDW`.
4. Try the `usertag` plugin and add a section in the `template` for something like `%tags{3}` to select the first three tags and write them into the structured comments field like: `#Vocal, #Deep, #Classic`
5. Testing


### Potential Generic Field Templating

On the forums for `beets` there are often questions about how to force titles to be titlecase or other formatting options for metadata and not just path templates. I believe this plugin can be adapted to handle the structure of any arbitrary field if I re-work the config to have a template string for any given attribute.

An example of a hypothetical `StructuredFields` plugin.

```yaml
structured_fields:
  comments: '[%ifdef{rating,$rating,-}] %tags{3} :: $comments'
  title: '%title{$title}'
  artist: '%upper{$artist}'
```


## Issues
If something is not working as expected please use the Issue tracker.
If the documentation is not clear please use the Issue tracker.
If you have a feature request please use the Issue tracker.
In any other situation please use the Issue tracker.


## Final Remarks
This plugin is use as-is and be sure to have a backup of your library before using yourself.


## Changelog

2020 Oct 31
  - Added flag for `force` to overwrite a field even if current comments field is identical. This improves performance since we don't have to write to every file when we update structured comments.
  - Fixed flag for `dry_run` so it actually prints the dry run.
  - Added more logging to terminal so you can see what it's doing and see the current progress.