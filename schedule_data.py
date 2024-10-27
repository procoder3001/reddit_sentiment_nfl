
import praw
import pandas as pd
import os

import time
from datetime import datetime
from pytz import timezone

from dotenv import load_dotenv

load_dotenv()

def get_reddit_comments(reddit, nfl_team_subreddit_name):
    """
    Description: 
        Gets 5 top comments from 5 hottest posts (so max 25 comments)
    Args: 
        reddit: praw.Reddit (object with access to reddit)
        nfl_team_subreddit_name: name of nfl team subreddit
    Returns: 
        List of reddit comments
    """
    subreddit = reddit.subreddit(nfl_team_subreddit_name)
    subs = []

    # get top 5 hottest posts
    hot = subreddit.hot(limit=5)
    for submission in hot:
        subs.append(submission)
    
    res = []
    for submission in subs:
        print("-----------------")
        print("reddit.config.reddit_url" + f"{submission.permalink}")
        submission.comments.replace_more(limit=0)
        submission.comment_limit = 5
        i = 0
        for top_level_comment in submission.comments:
            if i < 5:
                comment = top_level_comment.body
                # strip all whitespace characters
                comment = " ".join(comment.split())
                res.append(comment)
            else:
                break
            i += 1
        print("-----------------")
    
    return res
        


def main():
    # set up reddit access
    reddit = praw.Reddit(
        client_id = os.getenv("REDDIT_CLIENT_ID"),
        client_secret = os.getenv("REDDIT_SECRET_KEY"),
        user_agent='ABot/0.0.1'
    )

    # define nfl team subreddits
    nfl_team_subreddits = {
        "NFC": {
            "north": ["ravens","bengals", "browns", "steelers"],
            "south": ["texans","colts","jaguars","tennesseetitans"],
            "east": ["buffalobills","miamidolphins","patriots","nyjets"],
            "west": ["denverbroncos","kansascitychiefs","raiders", "chargers"]
        },
        "AFC": {
            "north": ["chibears","detroitlions","greenbaypackers","minnesotavikings"],
            "south": ["falcons","panthers","saints","buccaneers"],
            "east": ["cowboys","nygiants","eagles","commanders"],
            "west": ["azcardinals","losangelesrams","49ers","seahawks"]
        }
    }


    # initialize dataframe
    final_df = pd.DataFrame({'team_name': pd.Series(dtype='str'),
                   'upload_date': pd.Series(dtype='datetime64[ns]'),
                   'comment': pd.Series(dtype='str')})

    # times from eastern time zone
    tz = timezone('EST')

    # iterates through all 32 teams
    for conference in ["NFC", "AFC"]:
        for division in ["north","south", "east", "west"]:
            # 4 teams in a division
            for i in range(4):
                nfl_team_subreddit_name = nfl_team_subreddits[conference][division][i]
                print(nfl_team_subreddit_name)

                comments = get_reddit_comments(reddit = reddit, nfl_team_subreddit_name = nfl_team_subreddit_name)
                upload_date = [datetime.now(tz).replace(hour=5, minute=0)]*len(comments)
                team_name = [nfl_team_subreddit_name]*len(comments)

                concat_this = {"team_name": team_name,"upload_date": upload_date,"comment": comments}

                final_df = pd.concat([final_df, pd.DataFrame(concat_this)], ignore_index=True)

                print(f"Done loading comments for r/{nfl_team_subreddit_name}!...")
                # to help with api rate limit
                time.sleep(3)
    
    final_df.to_csv("gs://gcf-sources-134756275535-us-central1/nfl_comments.csv", index = False)

    print("done")

if __name__=="__main__":

    # print(os.getenv("REDDIT_CLIENT_ID"), os.getenv("REDDIT_SECRET_KEY"))

    # reddit = praw.Reddit(
    #     client_id = os.getenv("REDDIT_CLIENT_ID"),
    #     client_secret = os.getenv("REDDIT_SECRET_KEY"),
    #     user_agent='ABot/0.0.1'
    # )

    main()