
from pysat.solvers import Glucose3


def coordinate_to_num(a):
  return a[1]*6+a[0]+1
def num_to_coordinate(a):
  a = a-1
  x = a%6
  y = a//6
  return [x,y]
def is_safe(world,x):
  a = num_to_coordinate(x)
  a[1] = 5-a[1]
  a[0] = a[0]
  world[a[1]][a[0]]=1
def printf(a):
  for i in range(len(a)-1):
    print(a[i],"->",end=" ")
  print(a[-1])

def percieved(curr,g,percept,unvisited):
  x = coordinate_to_num(curr)
  g.add_clause([x])
  if x in unvisited:
    unvisited.remove(x)
  else: 
    return
  neighbours = [[1,0],[0,1],[-1,0],[0,-1]]
  valid_neighbours = []
  for i in neighbours:
    temp = [curr[0] + i[0],curr[1]+i[1]]
    valid_neighbours.append(temp)  
  a = [coordinate_to_num(i) for i in valid_neighbours]
  if percept=="=0":
    g.add_clause([a[0]])
    g.add_clause([a[1]])
    g.add_clause([a[2]])
    g.add_clause([a[3]])
  if percept=="=1":
    g.add_clause([a[0],a[1],a[2],a[3]])
    g.add_clause([-a[0],-a[1],-a[2],-a[3]])
    for i in range(4):
      for j in range(4):
        b = [i for i in a]
        b[i] = -1*a[i]
        b[j] = -1*a[j]
        g.add_clause([b[0],b[1],b[2],b[3]])
  if percept==">1":
    b = [-i for i in a]
    g.add_clause([-b[0],b[1],b[2],b[3]])
    g.add_clause([b[0],-b[1],b[2],b[3]])
    g.add_clause([b[0],b[1],-b[2],b[3]])
    g.add_clause([b[0],b[1],b[2],-b[3]])
    g.add_clause([b[0],b[1],b[2],b[3]])

def get_safe_rooms(g,unvisited,world):
  safe_rooms = []
  for i in unvisited:
    if g.solve(assumptions = [-i])== False:
      safe_rooms.append(i)
  for i in safe_rooms:
    is_safe(world,i)
  return safe_rooms

def get_neighbours(x,world,visited):
  curr = num_to_coordinate(x)
  neighbours = [[1,0],[0,1],[-1,0],[0,-1]]
  valid_neighbours = []
  for i in neighbours:
    temp = [curr[0] + i[0],curr[1]+i[1]]
    if temp[0]!=0 and temp[0]!=5 and temp[1]!=0 and temp[1]!=5 and world[5-temp[1]][temp[0]]==1 and visited[coordinate_to_num(temp)]==0:
      valid_neighbours.append(temp)
  a = [coordinate_to_num(i) for i in valid_neighbours]
  return a
def dir(a,b):
  u = num_to_coordinate(a);v = num_to_coordinate(b)
  x = v[0]-u[0];y=v[1]-u[1]
  if x==1:
    return 'Right'
  if x==-1:
    return 'Left'
  if y==1:
    return 'Up'
  if y==-1:
    return 'Down'

def move(ag,u,v,world,final_path,g,unvisited):
  parent = [i for i in range(40)]
  visited = [0 for i in range(40)]
  visited[u] = 1
  q = []
  q.append(u)
  while len(q)>0:
    x = q.pop(0)
    neighbours = get_neighbours(x,world,visited)
    for i in neighbours:
      visited[i] = 1
      parent[i] = x
      q.append(i)
    if visited[v]==1:
      break
  path = []
  if visited[v]==0:
    return False
  while not v==u:
    path.append(v)
    v = parent[v]  
  path.append(u)
  path.reverse()
  path_dir = []
  for i in range(len(path)-1):
    path_dir.append(dir(path[i],path[i+1]))
    final_path.append(num_to_coordinate(path[i+1]))
  for i in path_dir:
    ag.TakeAction(i)
    f = ag.FindCurrentLocation()
    if f!=[4,4]:
      p = ag.PerceiveCurrentLocation()
      percieved(f,g,p,unvisited)
  return True

def dist(x):
  v = num_to_coordinate(x)
  return abs(4-v[0]) + abs(4-v[1])

def initialize():
  g = Glucose3()
  final_path=[[1,1]]
  g.add_clause([coordinate_to_num([4,4])])
  g.add_clause([coordinate_to_num([3,4]),coordinate_to_num([4,3])])
  for i in range(6):
    g.add_clause([coordinate_to_num([0,i])])
    g.add_clause([coordinate_to_num([5,i])])
    g.add_clause([coordinate_to_num([i,0])])
    g.add_clause([coordinate_to_num([i,5])])
  world = [[0 for j in range(6)] for i in range(6)]
  safe_rooms = [8]
  is_safe(world,8)
  unvisited = []
  for i in range(1,5):
    for j in range(1,5):
      unvisited.append(coordinate_to_num([i,j]))
  return (g,final_path,world,safe_rooms,unvisited)

ag = Agent()
g,final_path,world,safe_rooms,unvisited=initialize()
while True:
  p = ag.PerceiveCurrentLocation()
  curr = ag.FindCurrentLocation()
  percieved(curr,g,p,unvisited)
  safe_rooms = get_safe_rooms(g,unvisited,world)
  safe_rooms.sort(key=dist)
  for i in safe_rooms:
    if move(ag,coordinate_to_num(curr),i,world,final_path,g,unvisited)== True:
      break
  if ag.FindCurrentLocation()==[4,4]:
    break
printf(final_path)
print(len(final_path))

import nltk
nltk.download('punkt')

sent = "Hello how are you"
words = nltk.word_tokenize(sent)
words

def color(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    if val>=0.7:
      color = "green"
    elif val<=0.5:
      color = "red"
    else:
      color = "black"
    return 'color: %s' % color

def dis():
  df = pd.DataFrame(np.random.rand(4,3))
  df.style.applymap(color)

import numpy as np
import pandas as pd
from IPython.display import display
df = pd.DataFrame(np.random.rand(4,3))
display(df.style.applymap(color))
c=20

