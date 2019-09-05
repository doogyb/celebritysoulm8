# celebritysoulm8

celebritysoulm8 is a twitter plot which aims to match you with your closest
celebrity, based on the linguistic content of your tweets. The linguistic
comparative evaluation uses [LWIC](http://liwc.wpengine.com/)'s online twitter
analysis tool [Analyze Words](https://analyzewords.com/) to create a vector
representation of your language on Twitter. It then compares this vector
to other users using cosine similarity evaluation. You can also compare anyone
you might like, as described in the examples below.

## How to use

The bot is interacted with on Twitter, using the hashtag #matchme (case insensitive).
So long as you tweet at the bot with this hashtag, it will reply with your celebrity
match:
<html>
<blockquote class="twitter-tweet"><p lang="en" dir="ltr"><a href="https://twitter.com/celebritysoulm8?ref_src=twsrc%5Etfw">@celebritysoulm8</a> <a href="https://twitter.com/hashtag/matchme?src=hash&amp;ref_src=twsrc%5Etfw">#matchme</a> here&#39;s hoping...</p>&mdash; S Doogy (@celebritysoulm8) <a href="https://twitter.com/celebritysoulm8/status/1169626725216600065?ref_src=twsrc%5Etfw">September 5, 2019</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
</html>


## Built With

* [Analyze Words](https://analyzewords.com/) - The sentiment analysis engine.
* [python-twitter](https://github.com/bear/python-twitter) - The python Twitter API.
## Acknowledgments

I'd like to thank my supervisor Tony Veale for the inspiration for this work.
His website can be found [here](http://afflatus.ucd.ie/), and his book, which
covers the idea of vectorising people's twitter language usage can be bought
[here](https://www.amazon.co.uk/Exploding-Creativity-Myth-Computational-Foundations/dp/1441181725/ref=sr_1_1?keywords=tony+veale&qid=1567622637&s=gateway&sr=8-1).
