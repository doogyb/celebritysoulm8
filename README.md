# celebritysoulm8

celebritysoulm8 is a twitter plot which aims to match you with your closest
celebrity, based on the linguistic content of your tweets. The linguistic
comparative evaluation uses [LWIC](http://liwc.wpengine.com/)'s online twitter
analysis tool [Analyze Words](https://analyzewords.com/) to create a vector
representation of your language on Twitter. It then compares this vector
to other users using cosine similarity evaluation. You can also compare anyone
you might like, as described in the examples below.

The bot's handle is @celebritysoulm8 and here is where you can find its
[Twitter Profile](https://twitter.com/celebritysoulm8).

## How to use

The bot is interacted with on Twitter, using the hashtag #matchme (case insensitive).
So long as you tweet at the bot with this hashtag, it will reply with your celebrity
match:

https://twitter.com/celebritysoulm8/status/1169626725216600065?s=20

This bot matched with Pink... Go figure.

You can also ask the bot to rate the similarity of your twitter language usage
with anyone else (regardless of celebrity status) using the tweet #rateus and
the person you which to compare yourself to:

https://twitter.com/celebritysoulm8/status/1169632588258058240?s=20

## Built With

* [Analyze Words](https://analyzewords.com/) - The sentiment analysis engine.
* [python-twitter](https://github.com/bear/python-twitter) - The python Twitter API.

## Acknowledgements

I'd like to thank my supervisor Tony Veale for the inspiration for this work.
His website can be found [here](http://afflatus.ucd.ie/), and his book, which
covers the idea of vectorising people's twitter language usage can be bought
[here](https://www.amazon.co.uk/Exploding-Creativity-Myth-Computational-Foundations/dp/1441181725/ref=sr_1_1?keywords=tony+veale&qid=1567622637&s=gateway&sr=8-1).
