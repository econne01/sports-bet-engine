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
