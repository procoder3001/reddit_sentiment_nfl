# nfl_reddit_sentiment
What is the current sentiment across the different NFL team subreddits? Is there a clear relationship between team performance and fan sentiment? How has sentiment shifted recently? These are the key questions I aim to explore with this project.

The app is updated every other day.

https://nfl-pulse-3-134756275535.us-central1.run.app/

I used: 
- Cloud Scheduler & Cloud Functions
    - schedule job to get recent reddit comments
    - run sentiment classification pipeline
- Vertex AI Pipelines
    - run Kubeflow pipeline to conduct sentiment analysis and aggregate scores
- Hugging Face 
    - use default sentiment classification model (DistilBERT base uncased finetuned SST-2)
- GCS
    - store data and pipeline metadata
- DASH
    - frontend
- Cloud Run
    - deployment

TODO:
- improve responsiveness of frontend
- improve model used (classification of reddit comments not always correct)
- include some measure of recent change in sentiment ranking

![Screen Shot 2023-01-02 at 3 04 18 PM](https://user-images.githubusercontent.com/48736213/212568848-08530d12-714c-430b-897c-4dd5a7249d38.png)
