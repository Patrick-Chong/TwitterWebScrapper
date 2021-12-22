from logging import debug
from flask import Flask, render_template
from flask.helpers import url_for
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from werkzeug.utils import redirect
from numerize import numerize 

# creating the APP
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Secret'

# Make the blueprint for the twitter authorization page. (replace the api_key and api_secret)
twitter_blueprint = make_twitter_blueprint(api_key='8krksO8AtMgrdCRsO1u6S5TiC', api_secret='DsEbq922hRWPy15yetoGbWvZJsyqXnHgINBtA9ZMPApQOVyG4f') 

#initiate the twitter auth process to get the user token for twitter API
app.register_blueprint(twitter_blueprint, url_prefix='/twitter_login') 

@app.route('/twitter')
def twitter_login():
    
    # If not logged in, proceed and login
    if not twitter.authorized: 
        return redirect(url_for('twitter.login')) 
    
    # Make a get call to 
    account_timeline_json = twitter.get('statuses/home_timeline.json',params={'tweet_mode':'extended'})  
    
    #initiate the lists for the required data (for easy access of the data)
    tweet_texts = []
    tweet_dates = []
    tweet_likes = []
    tweeter_name = []
    tweet_rts = []
    tweeter_followers = []
    
    print(account_timeline_json)
    if account_timeline_json.ok:
        
        if account_timeline_json:
        # iterate through all the 20 tweets' data
            for i in range(20):
                
                # fetch the tweet like from the above API get and append it to the list
                tweet_like = numerize.numerize(account_timeline_json.json()[i]['favorite_count'])
                tweet_likes.append(tweet_like)
                
                # fetch the tweet text from the above API get and append it to the list
                tweet_text = account_timeline_json.json()[i]['full_text']
                tweet_texts.append(tweet_text)   
                
                # fetch the tweet date from the above API get and append it to the list
                tweet_date = account_timeline_json.json()[i]['created_at']
                tweet_dates.append(tweet_date)
                
                # fetch the tweet rt_count from the above API get and append it to the list
                tweet_rt = numerize.numerize(account_timeline_json.json()[i]['retweet_count'])
                tweet_rts.append(tweet_rt)
                
                # fetch the tweet follower count from the above API get and append it to the list
                tweet_follower_count = numerize.numerize(account_timeline_json.json()[i]['user']['followers_count'])
                tweeter_followers.append(tweet_follower_count)
                
                # fetch the tweeter id like from the above API get and append it to the list
                tweeter_name_id = account_timeline_json.json()[i]['user']['screen_name']
                tweeter_name.append(tweeter_name_id)

        # pass the collected lists containing the variables required to the HTML file to display it
            return render_template('index.html', tweet_rts=tweet_rts, tweet_texts=tweet_texts, tweet_likes=tweet_likes, tweet_dates = tweet_dates, tweeter_followers=tweeter_followers, tweeter_name=tweeter_name)
    
    return '<h1>Error</h1>'

#by default, the app opens at the '/' endpoint. 
@app.route('/')
def home_redirect():
    
    # to avoid the error, redirect to the above function
    return redirect(url_for('twitter_login'))
    
# reun the app
if __name__ == '__main__':
    app.run(debug=False)
