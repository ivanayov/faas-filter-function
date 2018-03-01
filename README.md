# slack-filter-function
This is a Serverless function for OpenFaaS that filters messages and sends them to separate slack channels based on a sentiment analysis.


## Create Docker ID

If you don't have a Docker ID, you can register for it [here](https://docs.docker.com/docker-id/).


## Create a Docker host

You can provision an instance using [play-with-docker](https://labs.play-with-docker.com) by signing in with your Docker ID and starting a new session.

By clicking **ADD NEW INSTANCE** you will create a single Docker host.

Then you can install OpenFaaS on your instance with:

```
# docker swarm init --advertise-addr eth0 && \
  git clone https://github.com/openfaas/faas && \
  cd faas && \
  git checkout 0.7.0 && \
  ./deploy_stack.sh && \
  docker service ls
```

Update `gateway` in `filter.yml` with the link to OpenFaaS UI (The `8080` port link from the Docker host UI, e.g. `http://ip172-18-0-27-babuu59lukr000as9tcg-8080.direct.labs.play-with-docker.com`). 


## Deploy Sentiment Analysis function

In order to use this filter function, you will need to deploy the Sentiment Analysis function first.
This is a python function that provides a rating on sentiment positive/negative (polarity -1.0-1.0) and subjectivity provided to each of the sentences sent in via the TextBlob project.

Download the function with 

```
curl https://codeload.github.com/openfaas/faas/tar.gz/master | \
> tar -xz --strip=2 faas-master/sample-functions/SentimentAnalysis & cd SentimentAnalysis/
```

Instead of \<URL> use the same URL you use for the filter function (The `gateway` value from `filter.yml`).

Deploy with: 

```
curl -s <URL>/system/functions --data-binary \
'{ 
   "service": "sentimentanalysis",
   "image": "functions/sentimentanalysis",
   "envProcess": "python ./handler.py",
   "network": "func_functions"
   }'
```

and test

```
# curl <URL>/function/sentimentanalysis -d "I am really excited to participate in the OpenFaaS workshop."
Polarity: 0.375 Subjectivity: 0.75

# curl <URL>/function/sentimentanalysis -d "The hotel was clean, but the area was terrible"; echo
Polarity: -0.316666666667 Subjectivity: 0.85
```


## Update image with your Docker ID

You need to update `image` value in `filter.yml` and replace `docwareiy` with your Docker ID. 
You can check your images in [Docker Hub](https://hub.docker.com).


## Create Slack account

If you have never used Slack before, download it from [this link](https://slack.com/downloads)
and create Slack account.

Then you should create two separate slack chanels for positive and negative statements.

In order to get the Slack channel tokens, you need to add the **Incoming WebHooks App** to each of the channels.
Copy the contents of `slack.examples.yml` to a `slack.yml` file and update `slack_hook_positive` and `slack_hook_negative` with the channels tokens.


## Create an Applet

Visit [If This Then That](https://ifttt.com/) and create a new Applet.
Choose **Tweeter** and **New tweet from search**.

In the **Search for** field you should enter the query you'd like to search for.

For URL you should use the gateway value from `filter.yml`, followed by `/function/filter`.

Select `POST` for a **Method** as we would like to submit the data to our filter function.
As a **Content Type** select `application/json` and a **Body** in json format:

```
{ "text": "<<<{{Text}}>>>", "username": "<<<{{UserName}}>>>", "link": "<<<{{LinkToTweet}}>>>" }
```

Then save your Applet and it is ready for use from the `filter` function.


## Build and Deploy:

Use the CLI to build and deploy the function:

```
faas build -f filter.yml & faas push -f filter.yml & faas deploy -f filter.yml
```

View the logs by executing `docker service logs -f filter` on the Docker instance.

The filter function is ready to go. You can check you Slack channels for inputs.

