#!/usr/bin/python
import os,re,sys,show_info

def find_new_filename(filename,series,episodes): 

  regex = '.*[sS](\d+)[eE](\d+).*'
  #fail safe regex if format isn't s01e01
  regex2 = '.*(\d\d)(\d\d).*'
  regex3 = '.*(\d)x*(\d\d).*'
  
  season,episode = 0,0
  regs = [regex,regex2,regex3]
  ep = ""
  for reg in regs: 
    match = re.search(reg,filename)
    if match: 
      season,episode = int(match.group(1)),int(match.group(2))
      break
  
  if season <= 0: 
    print 'Unable to parse', filename
    return


  episode_name = episodes[episode].replace(' ','.')
  
  ep = 'S{:02d}E{:02d}.{}'.format(season,episode,episode_name) 
    
  series = series.replace(' ','.')
  new_filename = series + '.' + ep + os.path.splitext(filename)[-1]
  
  if not os.path.exists(new_filename):     
    return (filename,new_filename)
    #os.rename(filename,new_filename)
  #  os.rename(filename,"__TEMP"+new_filename)
  #  os.rename("__TEMP"+new_filename,new_filename)
  
def order_tuple(t): 
  _,b = t
  return b
  
def confirm_delete(remappings):

  remappings = sorted(remappings,key=order_tuple)

  txt = []  
  for old,new in remappings: 
    txt.append('{:>50} -> {}'.format(old,new))

  ans = ""
  while ans.lower() not in ['y','n']: 
    ans = raw_input('\n'.join(txt)+'\nConfirm the file moves y/n\n')
  if ans.lower() == 'n': 
    print "Abort rename."
    return 
  else: 
    print "Renaming files..."
    for old,new in remappings: 
      if not os.path.exists(new):     
        os.rename(old,new)
      else: 
        print "Unable to rename", old, "to", new

def main(): 

  if not len(sys.argv) == 3: 
    sys.exit('Only '+str(len(sys.argv))+' argument')
    
  show = sys.argv[1]
  season = sys.argv[2]

  # expected episodes to be organised like os
  # 'E:\Downloads\Sorted\[Show Name]\Season x'
  root = 'E:\Downloads\Sorted'
  path = os.path.join(root,show,'Season '+season)

  os.chdir(path)
  p = os.path.abspath('.')
  path_head, path_tail = os.path.split(p)
  if "Season" in path_tail: 
    _,series = os.path.split(path_head)
  else: 
    series = path_tail
  
  
  episodes = show_info.find_episodes_in_series(series,season)
  
  remappings = []
  for filename in os.listdir('.'):
    remapping = find_new_filename(filename,series,episodes)
    if not remapping == None: 
      remappings.append(remapping)
  if len(remappings) > 0:     
    confirm_delete(remappings)
  else: 
    print 'No files to rename in', path
  

if __name__ == '__main__':
  main()
