def get_sentiment_2() -> None:
    print("hi")
    import logging
    import sys
    # set up logging
    logging.basicConfig(stream = sys.stdout)
    logger = logging.getLogger("get_sentiment")
    logger.setLevel("INFO")

    logging.info("Test to see if logging works")
    print("hi 2")

    # from transformers import pipeline
    logging.info("Loaded hf pipeline")
    import pandas as pd

    # from pandasql import sqldf
    import pandasql

    # set up pysqldf
    # pysqldf = lambda q: sqldf(q, globals())
    logging.info("Set up pysqldf")
    print("hi 3")

    # Allocate a pipeline for sentiment-analysis
    # classifier = pipeline('sentiment-analysis')
    # logging.info("Getting sentiment analysis model")

    # read data
    input_comments_df = pd.read_csv("gs://gcf-sources-134756275535-us-central1/nfl_comments.csv")
    logging.info("Get input comments")

    # TODO: figure out how to retain types when transferring to and from GCP
    # cast to right types to make pandasql work
    input_comments_df["team_name"] = input_comments_df["team_name"].astype("str")
    input_comments_df["comment"] = input_comments_df["comment"].astype("str")
    input_comments_df["upload_date"] = input_comments_df["upload_date"].astype("datetime64[ns]")

    # classify sentiment
    # input_comments_df["sentiment"] = input_comments_df.apply(lambda row: classifier(row.comment), axis = 1)
    # input_comments_df["label"] = input_comments_df.apply(lambda row: row.sentiment[0]["label"], axis = 1)
    # input_comments_df["score"] = input_comments_df.apply(lambda row: row.sentiment[0]["score"], axis = 1)
    # logging.info("Classify sentiment")

    # drop unncessary column
    # input_comments_df.drop("sentiment", axis = 1, inplace=True)

    # cast to right types to make pandasql work

    # input_comments_df["label"] = input_comments_df["label"].astype("str")


    q = """
 
        SELECT *
        FROM input_comments_df

    """

    final_stats = pandasql.sqldf(q, locals())
    logging.info("Get aggregated stats")

    # save comments with sentiment probabilities
    # input_comments_df.to_csv("gs://gcf-sources-134756275535-us-central1/nfl_comments_w_sentiment.csv", index = False)
    # save aggregated stats for app
    # final_stats.to_csv("gs://gcf-sources-134756275535-us-central1/nfl_comments_agg_stats.csv", index = False)

    print("done")

    return

if __name__=="__main__":
    get_sentiment_2()