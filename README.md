# sports-bet-engine
a side-project in Machine Learning that tries to predict good bets on sports using real Vegas odds

## Setup
### Pre-requisites
- [virtualenv](https://gist.github.com/Geoyi/d9fab4f609e9f75941946be45000632b)
- [serverless](https://serverless.com/framework/docs/providers/aws/guide/installation/)
- [docker](https://docs.docker.com/install/) (for packaging python dependencies with serverless)

### Getting Started
psst, here is a little [cheat sheet](https://serverlesscode.com/post/python-3-on-serverless-framework/) for using python
3 with serverless.

    mkvirtualenv sports-bet -p ${path/to/python3}
    pip install -r requirements.txt

## Build & Deploy
Use serverless

    export AWS_PROFILE=personal-serverless
    serverless create --template aws-python3

## Betting Notes
Scoresandodds.com has some [helpful tips](http://www.scoresandodds.com/readinglines.php) on reading and understanding the published odds.
Some important defaults to keep in mind:
- MLB run line (aka, spread) is always 1.5 runs
- Most bets use a default of 20% fee between the favorite and underdog. For example, if it is a 50/50 toss up, then each
  team will cost $110 wager to win $100. If one team is favored at `-120` then the underdog would be `+100`

### Getting Odds Data
Scoresandodds.com has a roughly 24 hour history of the trends of the odds for a given matchup. You can find an example
at http://scoresandodds.com/linemovement/20180620/387097277
