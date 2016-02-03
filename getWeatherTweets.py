from dbco import *

##THIS PROGRAM FINDS THE WEATHER DURING A TIME PERIOD BY READING TWEETS!

##_id
##author
##text
##hashtags
##place
##words
##timestamp
##mentions
##guid

##blue
##blizzard
##chilly
##cloud
##cloudy
##freezing
##cold
##cool
##dark
##drizzle
##duststorm
##fog
##gray
##heat
##hot
##hurricane
##ice
##lightening
##moisture
##rain
##rainbow
##sandstorm
##sky
##smog
##smoke
##snow
##storm
##sunset
##sunrise
##thunder
##tornado
##typhoon
##warm
##weather
##wind

##rainy, cloudy, sunny
##cold, warm
##windy

def guessWeather(startTimestamp, endTimestamp):
    basicKeywordList = ["weather"]
    coldKeywordList = ["chilly", "freezing", "cold"]
    warmKeywordList = ["heat", "hot", "warm"]
    rainyKeywordList = ["drizzle", "rain", "rains", "rainy", "raining"]
    cloudyKeywordList = ["cloud", "clouds", "cloudy"]
    sunnyKeywordList = ["sunny", "rainbow"]
    windyKeywordList = ["blizzard", "hurricane", "storm", "wind", "windy"]

    overallKeywordList = basicKeywordList + coldKeywordList + warmKeywordList + rainyKeywordList + cloudyKeywordList + sunnyKeywordList + windyKeywordList
    overallWordList = []
    coldCount = 0
    warmCount = 0
    rainyCount = 0
    cloudyCount = 0
    sunnyCount = 0
    windyCount = 0
    
    tweetPool = list(db.tweet.find({'timestamp' : {'$gte' : startTimestamp, '$lt' : endTimestamp}, 'words' : {'$in' : overallKeywordList}}))
    for tweet in tweetPool:
        for word in tweet['words']:
            if word in overallKeywordList:
                overallWordList.append(word)
    for word in overallWordList:
        if word in coldKeywordList:
            coldCount += 1
        elif word in warmKeywordList:
            warmCount += 1
        elif word in rainyKeywordList:
            rainyCount += 1
        elif word in cloudyKeywordList:
            cloudyCount += 1
        elif word in sunnyKeywordList:
            sunnyCount += 1
        elif word in windyKeywordList:
            windyCount += 1

    coldPercentage = "unavailable"
    warmPercentage = "unavailable"
    rainyPercentage = "unavailable"
    cloudyPercentage = "unavailable"
    sunnyPercentage = "unavailable"

    if (coldCount + warmCount > 0):
        coldPercentage = int(coldCount * 100 / float(coldCount + warmCount))
        warmPercentage = int(warmCount * 100 / float(coldCount + warmCount))
    if (rainyCount + cloudyCount + windyCount > 0):
        rainyPercentage = int(rainyCount * 100 / float(rainyCount + cloudyCount + sunnyCount))
        cloudyPercentage = int(cloudyCount * 100 / float(rainyCount + cloudyCount + sunnyCount))
        sunnyPercentage = int(sunnyCount * 100 / float(rainyCount + cloudyCount + sunnyCount))

    print str(coldPercentage) + "% of people claim it was cold during the time period"
    print str(warmPercentage) + "% of people claim it was warm during the time period"
    print
    print str(rainyPercentage) + "% of people claim it was rainy during the time period"
    print str(cloudyPercentage) + "% of people claim it was cloudy during the time period"
    print str(sunnyPercentage) + "% of people claim it was sunny during the time period"

guessWeather(1440300000, 1440355000)
