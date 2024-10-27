# Input: data from GCS 
# Output: upload to GCS with sentiment scores
# import google.cloud.aiplatform as aip
from google.cloud import aiplatform as aip

from kfp import dsl
from kfp.v2 import compiler
from kfp.v2.dsl import component

from kfp.v2 import compiler  # noqa: F811

import os


# @component(packages_to_install=["google-cloud-storage"])
# def example(
#     text: str,
# ) -> NamedTuple(
#     "Outputs",
#     [
#         ("output_one", str),  # Return parameters
#         ("output_two", str),
#     ],
# ):
#     # the import is not actually used for this simple example, but the import
#     # is successful, as it was included in the `packages_to_install` list.
#     from google.cloud import storage  # noqa: F401

#     o1 = f"output one from text: {text}"
#     o2 = f"output two from text: {text}"
#     print("output one: {}; output_two: {}".format(o1, o2))
#     return (o1, o2)

PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION")
BUCKET_URI = os.getenv("BUCKET_URI")  # @param {type:"string"}
SERVICE_ACCOUNT = os.getenv("SERVICE_ACCOUNT")

# API service endpoint
API_ENDPOINT = "{}-aiplatform.googleapis.com".format(REGION)
PIPELINE_ROOT = "{}/pipeline_root/intro".format(BUCKET_URI)

# it's pandasql not pandassql 
@component(
    packages_to_install=["transformers==4.19.4","pandas==1.3.5", "pandasql"], #, "pandasql"],
    base_image="us-docker.pkg.dev/vertex-ai/training/pytorch-xla.1-11:latest" # "python:3.9",
)
def get_sentiment_2() -> None:
    print("hi")
    import logging
    import sys
    # set up logging
    logging.basicConfig(stream = sys.stdout)
    logger = logging.getLogger("get_sentiment")
    logger.setLevel("INFO")

    logging.info("Test to see if logging works")


    from transformers import pipeline
    logging.info("Loaded hf pipeline")
    import pandas as pd

    # from pandasql import sqldf
    import pandasql

    # set up pysqldf
    # pysqldf = lambda q: sqldf(q, globals())
    logging.info("Set up pysqldf")


    # Allocate a pipeline for sentiment-analysis
    classifier = pipeline('sentiment-analysis')
    logging.info("Getting sentiment analysis model")

    # read data
    input_comments_df = pd.read_csv("gs://gcf-sources-134756275535-us-central1/nfl_comments.csv")
    logging.info("Get input comments")

    # TODO: figure out how to retain types when transferring to and from GCP
    # cast to right types to make pandasql work
    input_comments_df["team_name"] = input_comments_df["team_name"].astype("str")
    input_comments_df["comment"] = input_comments_df["comment"].astype("str")
    input_comments_df["upload_date"] = input_comments_df["upload_date"].astype("datetime64[ns]")

    # classify sentiment
    input_comments_df["sentiment"] = input_comments_df.apply(lambda row: classifier(row.comment[:min(len(row.comment),512)]), axis = 1)
    input_comments_df["label"] = input_comments_df.apply(lambda row: row.sentiment[0]["label"], axis = 1)
    input_comments_df["score"] = input_comments_df.apply(lambda row: row.sentiment[0]["score"], axis = 1)
    logging.info("Classify sentiment")

    # drop unncessary column
    input_comments_df.drop("sentiment", axis = 1, inplace=True)

    # cast to right types to make pandasql work

    input_comments_df["label"] = input_comments_df["label"].astype("str")


    q = """
    WITH b AS (
        SELECT *,
        IIF(label = "POSITIVE",1,-1) AS sign
        FROM input_comments_df
    )
    SELECT team_name, AVG(score*sign) AS sentiment_summary
    FROM b
    GROUP BY team_name
    """

    final_stats = pandasql.sqldf(q, locals()) # pysqldf(q)
    logging.info("Get aggregated stats")

    # save comments with sentiment probabilities
    input_comments_df.to_csv("gs://gcf-sources-134756275535-us-central1/nfl_comments_w_sentiment.csv", index = False)
    # save aggregated stats for app
    final_stats.to_csv("gs://gcf-sources-134756275535-us-central1/nfl_comments_agg_stats.csv", index = False)

    return

@dsl.pipeline(
    name="nfl-subreddit-sentiment",
    description="Getting sentiment of nfl reddit comments",
    pipeline_root=PIPELINE_ROOT,
)
def pipeline():
    
    get_sentiment_task = (
        get_sentiment_2().
        set_cpu_limit('1').
        set_memory_limit('3G')
    )
    

    
if __name__=="__main__":


    aip.init(project=PROJECT_ID, staging_bucket=BUCKET_URI)

    compiler.Compiler().compile(pipeline_func=pipeline, package_path="intro_pipeline_2.json")

    DISPLAY_NAME = "intro_pipeline_job_unique"

    job = aip.PipelineJob(
        display_name=DISPLAY_NAME,
        template_path="intro_pipeline_2.json",
        pipeline_root=PIPELINE_ROOT,
        enable_caching=False
    )

    print(type(job))

    job.run()
