#!/usr/bin/python
import urllib2, re, json

def movies_now():

  page1 = "http://virginatlantic.mymovies.net/?s=2"
  page2 = "http://virginatlantic.mymovies.net/?s=2&p=2"
  urls = [page1,page2]
  pattern = '<div class="itemtitle">(.*?)</div>'
  movies = []
  for url in urls: 
    f = urllib2.urlopen(url)
    html = f.read()
    matches = re.findall(pattern,html)
    if matches: 
      movies += matches
      
  return movies

def imdb_rating(title): 

  url = "http://www.omdbapi.com/?t={}&r=json".format(title)
  url = urllib2.quote(url, safe="%/:=&?~#+!$,;'@()*[]")

  f = urllib2.urlopen(url)
  json_str = f.read()
  movie_json = json.loads(json_str)
  
  if "Error" not in movie_json:   
    if movie_json['imdbRating'] != "N/A": 
      return float(movie_json['imdbRating'])
    else: 
      "Unable to rate", title
  else: 
    print "Unable to find movie", title
  return 0
  
def rate_movies(titles):
  return [(title,imdb_rating(title)) for title in titles]
  
def viewable(rated_movies): 
  #expects a list of (title,rating) tuples
  return ["{:>26} - {}".format(title,rating) for title,rating in rated_movies if rating >=7]

def main(): 
  movies = movies_now()
  rated_movies = rate_movies(movies)  
  
  last_elem = lambda x: x[-1]
  ordered_rated_movies = sorted(rated_movies,key=last_elem,reverse=True)
  
  print "\n".join(viewable(ordered_rated_movies))


if __name__ == '__main__':
  main()
