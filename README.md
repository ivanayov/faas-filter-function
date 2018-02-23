# slack-filter-function
This is a Serverless function for OpenFaaS that filters messages and sends them to separate slack channels based on a sentiment analysis.


In order to use this filter function, you will need to deploy the [Sentiment Analysis](https://github.com/openfaas/faas/tree/master/sample-functions/SentimentAnalysis) function first.  
You can find more details in the [README](https://github.com/openfaas/faas/tree/master/sample-functions/SentimentAnalysis#sentimentanalysis).  
Instead of `localhost:8080` you should use the same url you use for the filter function.  


You can provision an instance using [play-with-docker](https://labs.play-with-docker.com) by signing in with your Docker ID and starting a new session.
By clicking "ADD NEW INSTANCE" you will create a single Docker host.

Then you need to install OpenFaaS:

```# docker swarm init --advertise-addr eth0 && \
  git clone https://github.com/openfaas/faas && \
  cd faas && \
  git checkout 0.7.0 && \
  ./deploy_stack.sh && \
  docker service ls
```

For more details please refer to [TestDrive](https://github.com/openfaas/faas/blob/master/TestDrive.md) documentation.

Then you need to update the `gateway` in `filter.yml` with the link to OpenFaaS UI (The `8080` port link from the Docker host UI).

You also need to update the `image` and replace `docwareiy` with your Docker Hub name.

In order to get the Slack channel tokens, you need to add the Incoming WebHooks App to the channel.
Then create a `slack.yml` file, copying the content from `slack.examples.yml` and update it with your Slack tokens.

Then all you need is to build, push and deploy your function.

