import importlib

class Encoder():
  def name(self):
    raise NotImplementedError()
  
  def encode(self, game_state):
    raise NotImplementedError()
  
  def encode_point(self, point): 
    raise NotImplementedError()

  def decode_point_index(self, index): 
    raise NotImplementedError()

  def num_points(self): 
    raise NotImplementedError()
    
  def shape(self): 
    raise NotImplementedError()
  

def get_encoder_by_name(name):
  board_size = (9, 7)
  module = importlib.import_module('dljungle.encoders.' + name)
  constructor = getattr(module, 'create')
  return constructor()