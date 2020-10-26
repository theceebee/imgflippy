# pyimgflip
An open source Python interface for the [imgflip RESTful API](https://api.imgflip.com) `pyimgflip` has been developed
to remain true to the original API while offering the conveniences that Python allows.

### Quickstart
`pyimgflip` has been written with the intention of allowing for meme generation from either a command line
interface *or* an interpreted environment.

####Command Line

#####get_memes
Print a table of the popular memes that may be captioned with this API:

From the imgflip API documentation:
> The size of this array and the order of memes may change at any time. When this description was written, it returned
> 100 memes ordered by how many times they were captioned in the last 30 days. Additional properties other than those
> listed below may be added in the future without warning, so do not assume the JSON structure of each meme will never
> have new properties.

```
$ python -m pyimgflip get_memes
Template ID |                      Name                      |               URL
------------+------------------------------------------------+---------------------------------
112126428   | Distracted Boyfriend                           | https://i.imgflip.com/1ur9b0.jpg
181913649   | Drake Hotline Bling                            | https://i.imgflip.com/30b1gx.jpg
87743020    | Two Buttons                                    | https://i.imgflip.com/1g8my4.jpg
...
```

#####add_caption

From the imgflip API documentation:
> Add a caption to an Imgflip meme template. Images created with this API will be publicly accessible by anyone through
> the url in the response - there is no "private" option. This does not mean these memes will be posted publicly though,
> one still needs to know the exact URL to find the image. If the image hangs around on Imgflip servers for a while and
> gets very few views (direct image views and image page views both count), it will be auto-deleted to save space.