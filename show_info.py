#!/usr/bin/python
import sys,urllib2
import xml.etree.ElementTree as ET

def find_show(show_name):
  ''' 
  find the show id for a show name
  returns the show id for the most relevant show name'''
  url = 'http://services.tvrage.com/feeds/search.php?show={}'
  f = urllib2.urlopen(url.format(show_name))
  root = ET.fromstring(f.read())
  shows = root.findall('show')
  print len(shows), "shows matching", show_name
  for show in shows: 
    id = show.findtext('showid')
    name = show.findtext('name')
    if name == show_name: 
      started = show.findtext('started')
      print "Choosing", name, started, id
      return id

def find_episodes(id, season): 
  ''' 
  for a particular season for a show 
  returns a dictionary of episode numbers to titles'''
  url = 'http://services.tvrage.com/feeds/episode_list.php?sid={}'
  f = urllib2.urlopen(url.format(id))
  root = ET.fromstring(f.read())
  xpath = "./Episodelist/Season/[@no='{}']".format(season)
  episodes = root.find(xpath).findall('./episode')
  episodes_map = {}  
  for e in episodes:
    num = e.findtext('seasonnum')
    title = e.findtext('title')
    episodes_map[int(num)] = title
    
  return episodes_map
  
def find_episodes_in_series(show,season):
  id = find_show(show)
  return find_episodes(id, season)

def main():
  show_name = 'Community'
  season = 3
  episodes = find_episodes_in_series(show_name,season)
  episode = 11
  print "{}-S{}E{}-{}".format(show_name, season, episode, episodes[episode].replace(' ','.'))

    
if __name__ == '__main__':
  main()
