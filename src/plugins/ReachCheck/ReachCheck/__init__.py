"""
This is where the implementation of the plugin code goes.
The ReachCheck-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from turtle import end_fill
from webgme_bindings import PluginBase
import json

# Setup a logger
logger = logging.getLogger('ReachCheck')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class ReachCheck(PluginBase):
  def main(self):

    import json
    active_node = self.active_node
    core = self.core
    logger = self.logger
    self.namespace = None
    META = self.META
    logger.debug('path: {0}'.format(core.get_path(active_node)))
    logger.info('name: {0}'.format(core.get_attribute(active_node, 'name')))
    logger.warn('pos : {0}'.format(core.get_registry(active_node, 'position')))
    logger.error('guid: {0}'.format(core.get_guid(active_node)))
    nodes = core.load_own_sub_tree(active_node)
    
    def getOutputmatrix():
      path2node = {}
      for node in nodes:
        # for every object, add to dict where key,val = path,node
        path2node[core.get_path(node)] = node
      # this is essentially an adjacency matrix
      output_graph = {}
      input_graph = {}

      for node in nodes:
        if core.is_instance_of(node, META['Place']) or core.is_instance_of(node, META['Transition']):
          station_id = core.get_path(node)
          #logger.info(station_id)
          item_type = core.get_attribute(node,'name') 
          tot_str = station_id  #item_type + ' - ' + 
          logger.debug(tot_str)
          output_station = []
          input_station = []

          for arc in nodes:
            if core.is_instance_of(arc, META['Arc']):
              # ---- LOGIC FOR DETERMINING OUTPUT ----
              # path2node[core.get_pointer_path(track, 'src')] gets the track 'node'
              src_station = core.get_path(path2node[core.get_pointer_path(arc, 'src')])
              dst_station = core.get_path(path2node[core.get_pointer_path(arc, 'dst')])
              name = core.get_attribute(path2node[core.get_pointer_path(arc, 'dst')], 'name')# + '-' + dst_station
              tot_str2 = dst_station 
              if src_station == station_id:
                output_station.append(tot_str2)
                #station[tot_str2] = 'connected'
                
              # ---- LOGIC FOR DETERMINING INPUT ----
              input_tot_str2 = src_station 
              if dst_station == station_id:
                input_station.append(input_tot_str2)
          
          # station_id is 'H/g' path
          output_graph[tot_str] = output_station
          input_graph[tot_str] = input_station

      
      logger.info(json.dumps(output_graph, indent = 4))
      logger.info(json.dumps(input_graph, indent = 4))
      return output_graph, input_graph 
    
    
    def getNetType():
      net_type = []
      if isMarkedGraph():
        net_type.append('Marked Graph')
      if isStateMachine():
        net_type.append('State Machine')
      if isWorkflow():
        net_type.append('Workflow') 
      if isFreeChoice():
        net_type.append('Free Choice') 
      if net_type:
        return net_type 
      else:
        return '' 
    
    ##--- MarkedGraph if every place has 1 input and 1 output
    def isMarkedGraph():
      count = 0 
      for node in nodes:
        if core.is_instance_of(node, META['Place']):
          place_id = core.get_path(node) 
          possible_inputs = inputs[place_id] 
          possible_outputs = outputs[place_id] 
          if len(possible_inputs) != 1 or len(possible_outputs) != 1:
            return False 
          count = 1 
      if count:
        return True 
      return False 
        
    ##--- statemachine if every transition has 1 input and 1 output
    def isStateMachine():
      count = 0 
      for node in nodes:
        if core.is_instance_of(node, META['Transition']):
          transition_id = core.get_path(node) 
          possible_inputs = inputs[transition_id] 
          possible_outputs = outputs[transition_id] 
          if len(possible_inputs) != 1 or len(possible_outputs) != 1:
            return False 
          count = 1 
      if count:
        return True 
      return False 
    
    ##--- free choice if every transition has a unique set of inplaces
    def isFreeChoice():
      count = 0 
      for node in nodes:  
        if core.is_instance_of(node, META['Transition']):
          transition_id = core.get_path(node) 
          #possible_inputs = [] 
          possible_inputs = inputs[transition_id] 
          logger.debug(possible_inputs) 
          for node in nodes:
            if core.is_instance_of(node, META['Transition']):
              t_id = core.get_path(node) 
              if t_id != transition_id:
                t2_inputs = inputs[t_id] 
                logger.debug(t2_inputs)
                if t2_inputs == possible_inputs:
                  return False 
          # if there is at least one transition, return true      
          count = 1 
      if count:
        return True 
      # otherwise return false
      return False 


    def bfs(visited, graph, node): #function for BFS
      visited.append(node)
      queue.append(node)
      while queue:          # Creating loop to visit each node
        m = queue.pop(0) 
        for neighbour in outputs[m]:
          if neighbour not in visited:
            visited.append(neighbour)
            queue.append(neighbour)
      return visited 

    
    ##--- Workflow if one start and one end sink, and all nodes
    ## exist along a path from start to end
    def isWorkflow():
      count = 0 
      possible_start = []
      possible_end = []
      for node in nodes:
        if core.is_instance_of(node, META['Place']):
          # check for a place with only one output and only
          # one input 
          place_id = core.get_path(node) 
          if len(inputs[place_id]) == 0 and len(outputs[place_id]) != 0:
            possible_start.append(place_id) 
          if len(outputs[place_id]) == 0 and len(inputs[place_id]) != 0:
            possible_end.append(place_id) 
            
      # if theres more than one start or end sink, return false
      logger.info(possible_start)
      if len(possible_start) != 1 or len(possible_end) != 1:
        return False 

      # check the path to ensure all nodes are on it
      # and it ends at the sink. Should only be one place
      # in possible_start
      path = bfs(visited,queue,possible_start[0]) 

      #ends with the sink
      if (path[-1] != possible_end[0]):
        return False 
      # has every node on it
      path.sort() 
      keys = list(outputs.keys())
      keys.sort()
      if(path == keys):
        return True     
      return False 
    


    ## EXECUTED CODE BEGINS HERE ##
    outputs, inputs = getOutputmatrix()
    # --- Arrays needed for workflow check
    visited = [] # List for visited nodes
    queue = []     #Initialize a queue 
    # --- Get the type of petrinet 
    ans = getNetType() 
    ans_str = ''
    if ans:
        ans_str = 'Petrinet is a {}'.format(ans.pop())
        while (len(ans) > 0):
            if len(ans) is 1:
                ans_str += " and {}.".format(ans.pop()) 
            else:
                ans_str += ", {}".format(ans.pop())
    else:
        ans_str = 'Petrinet is not any recognizable type.'
   
    self.send_notification(ans_str)
    logger.info(ans_str)
