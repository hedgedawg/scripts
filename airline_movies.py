#!/usr/bin/python
import urllib2, re, json, string, sys

_debug = 0

def movies_virgin():
  #Returns a list of movies for the particular airline
  
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
  
def movies_ba():
  #Returns a list of movies for the particular airline
  
  base_url = 'http://www.britishairways.com/en-gb/information/entertainment/in-flight-entertainment?to&livesite_country=gb&month=this&class=all&from&flightno&livesite_language=en&page={}'
  urls = [base_url.format(i) for i in range(1,10)]
  pattern = '<li class="post-movie.+?post_type=movie.+?title="(.+?)"'
  end_pattern = 'There is no media matching your query'  
  movies = []
  for url in urls: 
    f = urllib2.urlopen(url)
    html = f.read()
    if end_pattern in html: 
      break
    matches = re.findall(pattern,html)
    if matches: 
      movies += matches
      
  return movies
  
def imdb_query(search,type='t'): 
  template_url = "http://www.omdbapi.com/?{}={}&r=json"
  url = template_url.format(type,search)
  url = urllib2.quote(url, safe="%/:=&?~#+!$,;'@()*[]")
  f = urllib2.urlopen(url)
  json_str = f.read()
  return json.loads(json_str)
  
def error_msg(title,msg): 
  if (_debug): 
    print "Unable to parse", title
    print "Most recent json", msg
  return 0

def imdb_rating(title): 

  movie_json = imdb_query(title)
  
  if "Error" in movie_json: 
    search_json = imdb_query(title,type='s')
    if 'Search' not in search_json: 
      seach_json = imdb_query(title.translate(None, string.punctuation),type='s')
      if 'Search' not in search_json: 
        return error_msg(title, search_json)
    imdb_id = search_json['Search'][0]['imdbID']
    movie_json = imdb_query(imdb_id,type='i')
  
  if "Error" not in movie_json:   
    if movie_json['imdbRating'] != "N/A": 
      return float(movie_json['imdbRating'])
    else: 
      return error_msg(title, movie_json)
  else: 
    return error_msg(title, movie_json)
  return 0
  
def rate_movies(titles):
  return [(title,imdb_rating(title)) for title in titles]
  
def viewable(rated_movies, tolerance=7): 
  #expects a list of (title,rating) tuples
  return ["{:>26} - {}".format(title,rating) for title,rating in rated_movies if rating >=tolerance]

def main(): 
  airline = "virgin" #default to virgin
  
  if len(sys.argv) > 1: 
    airline = sys.argv[1].lower()
  fn_name = 'movies_'+airline
  if hasattr(globals(),fn_name): 
    movies = globals()[fn_name]()
  else:
    sys.exit('Unable to parse movies for airline %s' % airline)
  rated_movies = rate_movies(movies)  
  
  last_elem = lambda x: x[-1]
  ordered_rated_movies = sorted(rated_movies,key=last_elem,reverse=True)
  
  print "\n".join(viewable(ordered_rated_movies))


if __name__ == '__main__':
  main()
