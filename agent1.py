from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions, features, units
from absl import app
import random

#obs is the object that contains all the observactions we need it
state = 2
boostm = True
queenslimit = True
moveallow = True
cont = 0
state = 2
game_state = 1

class ZergAgent(base_agent.BaseAgent):

  def __init__(self):
    """initialize a variable"""
    super(ZergAgent, self).__init__()
    self.attack_coordinates = None
    self.safe_coordinates = None



  def unit_type_is_selected(self, obs, unit_type):

    """utility fuction to simply sintax of unit type
    selected check"""
    if (len(obs.observation.single_select) > 0 and
            obs.observation.single_select[0].unit_type == unit_type):
        return True

    if (len(obs.observation.multi_select) > 0 and
            obs.observation.multi_select[0].unit_type == unit_type):
        return True

    return False

  def get_units_by_type(self, obs, unit_type):

    """utility fuction to simply sintax of unit
    selection by type"""
    return [unit for unit in obs.observation.feature_units
            if unit.unit_type == unit_type]

  def can_do(self, obs, action):

    """utility fuction to simply sintax of
    available actions check"""
    return action in obs.observation.available_actions

  def my_attack1(self, obs):
    #if enough zerglings,send attack
    zerglings = self.get_units_by_type(obs, units.Zerg.Zergling)
    hydras = self.get_units_by_type(obs, units.Zerg.Hydralisk)
    x = self.safe_coordinates[0]
    y = self.safe_coordinates[1]
    if x < 32:
        self.safe_coordinates[0] = 20
        self.safe_coordinates[1] = 20
        x = 44
        y = 20
    else:
        self.safe_coordinates[0] = 42
        self.safe_coordinates[1] = 48
        x = 18
        y = 48
    if len(hydras) >= 6:
        #send attack at attack locations
        if self.unit_type_is_selected(obs, units.Zerg.Hydralisk):
            if self.can_do(obs, actions.FUNCTIONS.Attack_minimap.id):
                global game_state
                game_state = 3
                global cont
                cont = 0
                return actions.FUNCTIONS.Attack_minimap("now",(x,y))

        #select zerglings
        if self.can_do(obs, actions.FUNCTIONS.select_army.id):
            return actions.FUNCTIONS.select_army("select")

  def my_attack2(self, obs):
    #if enough zerglings,send attack
    zerglings = self.get_units_by_type(obs, units.Zerg.Zergling)
    hydras = self.get_units_by_type(obs, units.Zerg.Hydralisk)
    if (len(hydras) >= 30):
        #send attack at attack locations
        if self.unit_type_is_selected(obs, units.Zerg.Hidralisk):
            if self.can_do(obs, actions.FUNCTIONS.Attack_minimap.id):
                return actions.FUNCTIONS.Attack_minimap("now",
                                                        self.attack_coordinates)

        #select zerglings
        if self.can_do(obs, actions.FUNCTIONS.select_army.id):
            return actions.FUNCTIONS.select_army("select")

  def my_spawning_pool(self, obs, qty):
    #if there is no barraks (spawning pool) build one
    spawning_pools = self.get_units_by_type(obs, units.Zerg.SpawningPool)
    if len (spawning_pools) < qty :
        # if drone is selected build spawning pool
        if self.unit_type_is_selected(obs, units.Zerg.Drone):
            if self.can_do(obs,actions.FUNCTIONS.Build_SpawningPool_screen.id):
                x = random.randint(0,63)
                y = random.randint(0,63)

                return actions.FUNCTIONS.Build_SpawningPool_screen("now", (x,y))

        # select some random drone for the next choice
        drones = self.get_units_by_type(obs, units.Zerg.Drone)
        if len(drones) > 0 :
            drone = random.choice(drones)

            return actions.FUNCTIONS.select_point("select_all_type",(drone.x,
                                                                  drone.y))

  def my_metabolic_boost(self, obs):
    #if there is no barraks (spawning pool) build one
    spawning_pools = self.get_units_by_type(obs, units.Zerg.SpawningPool)
    if len (spawning_pools) > 0 :
        if self.unit_type_is_selected(obs, units.Zerg.SpawningPool):
            if self.can_do(obs,actions.FUNCTIONS.Research_ZerglingMetabolicBoost_quick.id):
                print("metabolic Boost")
                global boostm
                boostm = False
                return actions.FUNCTIONS.Research_ZerglingMetabolicBoost_quick("now")


        spawning_pools = random.choice(spawning_pools)
        return actions.FUNCTIONS.select_point("select",(spawning_pools.x,spawning_pools.y))


  def my_den(self, obs):
    den = self.get_units_by_type(obs, units.Zerg.HydraliskDen)
    if len (den) == 0 :
        if self.unit_type_is_selected(obs, units.Zerg.Drone):
            if self.can_do(obs,actions.FUNCTIONS.Build_HydraliskDen_screen.id):
                x = random.randint(0,63)
                y = random.randint(0,63)
                print("den")
                return actions.FUNCTIONS.Build_HydraliskDen_screen("now", (x,y))

        # select some random drone for the next choice
        drones = self.get_units_by_type(obs, units.Zerg.Drone)
        if len(drones) > 0 :
            drone = random.choice(drones)

            return actions.FUNCTIONS.select_point("select_all_type",(drone.x,
                                                                  drone.y))

  def my_hatchery(self, obs, qty):
    #to build another hatchery to inprove performance
    hatch = self.get_units_by_type(obs, units.Zerg.Hatchery)
    lair = self.get_units_by_type(obs, units.Zerg.Lair)
    hive = self.get_units_by_type(obs, units.Zerg.Hive)
    total = len(hatch)+len(lair)+len(hive)
    if total < qty :
        # if drone is selected build spawning pool
        if self.unit_type_is_selected(obs, units.Zerg.Drone):
            if self.can_do(obs,actions.FUNCTIONS.Build_Hatchery_screen.id):
                x = random.randint(0,63)
                y = random.randint(0,63)
                return actions.FUNCTIONS.Build_Hatchery_screen("now", (x,y))
        # select some random drone for the next choice
        drones = self.get_units_by_type(obs, units.Zerg.Drone)
        if len(drones) > 0 :
            drone = random.choice(drones)

            return actions.FUNCTIONS.select_point("select_all_type",(drone.x, drone.y))

  def my_lair(self, obs):
    #if there is no barraks (spawning pool) build one
    lair = self.get_units_by_type(obs, units.Zerg.Lair)
    if len (lair) == 0 :
        # if drone is selected build spawning pool
        if self.unit_type_is_selected(obs, units.Zerg.Hatchery):
            if self.can_do(obs,actions.FUNCTIONS.Morph_Lair_quick.id):
                return actions.FUNCTIONS.Morph_Lair_quick("now")

        # select some random drone for the next choice
        hatchery = self.get_units_by_type(obs, units.Zerg.Hatchery)
        if len(hatchery) > 0 :
            hatchery = random.choice(hatchery)

            return actions.FUNCTIONS.select_point("select_all_type",(hatchery.x,
                                                                  hatchery.y))

  def my_extractor(self, obs, qty):
    #if there is no barraks (spawning pool) build one
    extractor = self.get_units_by_type(obs, units.Zerg.Extractor)
    if len (extractor) < qty :
        # if drone is selected build spawning pool
        if self.unit_type_is_selected(obs, units.Zerg.Drone):
            if self.can_do(obs,actions.FUNCTIONS.Build_Extractor_screen.id):
                geysers = self.get_units_by_type(obs, units.Neutral.VespeneGeyser)
                if len(geysers) > 0 :
                    geyser = random.choice(geysers)
                    #VespeneGeyser
                    return actions.FUNCTIONS.Build_Extractor_screen("now", (geyser.x,geyser.y))

        # select some random drone for the next choice
        drones = self.get_units_by_type(obs, units.Zerg.Drone)
        if len(drones) > 0 :
            drone = random.choice(drones)

            return actions.FUNCTIONS.select_point("select_all_type",(drone.x,drone.y))



  def my_harvest_gas(self,obs):
        extractor = self.get_units_by_type(obs, units.Zerg.Extractor)
        if len(extractor) > 0:
            extractor = random.choice(extractor)
            if extractor['assigned_harvesters'] < 3:
                if self.unit_type_is_selected(obs, units.Zerg.Drone):
                    if len(obs.observation.single_select) < 2 and len(obs.observation.multi_select) < 2 :
                        if self.can_do(obs,actions.FUNCTIONS.Harvest_Gather_screen.id):
                            return actions.FUNCTIONS.Harvest_Gather_screen("now",(extractor.x, extractor.y))


                drones = self.get_units_by_type(obs, units.Zerg.Drone)
                if len(drones) > 0 :
                    drone = random.choice(drones)
                    return actions.FUNCTIONS.select_point("select",(drone.x,drone.y))

  def my_harvest_minerals(self,obs):
      mineral = self.get_units_by_type(obs, units.Neutral.MineralField)
      if len(mineral) > 0:
          mineral = random.choice(mineral)
          if mineral['assigned_harvesters'] < 2:
              if self.unit_type_is_selected(obs, units.Zerg.Drone):
                  if len(obs.observation.single_select) < 2 and len(obs.observation.multi_select) < 2:
                      if self.can_do(obs,actions.FUNCTIONS.Harvest_Gather_screen.id):
                          print("harvesting minerals")
                          return actions.FUNCTIONS.Harvest_Gather_screen("now",(mineral.x, mineral.y))

              drones = self.get_units_by_type(obs, units.Zerg.Drone)
              if len(drones) > 0 :
                  drone = random.choice(drones)
                  if self.can_do(obs,actions.FUNCTIONS.select_point.id):
                      print("selecting drones minerals")
                      return actions.FUNCTIONS.select_point("select",(drone.x,drone.y))

  def make_queen(self, obs):

      if self.unit_type_is_selected(obs, units.Zerg.Hatchery) or self.unit_type_is_selected(obs, units.Zerg.Lair) or self.unit_type_is_selected(obs, units.Zerg.Hive):
          if self.can_do(obs,actions.FUNCTIONS.Train_Queen_quick.id):
              print("queen")
              global queenslimit
              queenslimit = False
              return actions.FUNCTIONS.Train_Queen_quick("now")

      hatch = self.get_units_by_type(obs, units.Zerg.Hatchery)
      if len(hatch) > 0:
          hatch = random.choice(hatch)
          return actions.FUNCTIONS.select_point("select",(hatch.x,hatch.y))

      hatch = self.get_units_by_type(obs, units.Zerg.Lair)
      if len(hatch) > 0:
          hatch = random.choice(hatch)
          return actions.FUNCTIONS.select_point("select",(hatch.x,hatch.y))

      hatch = self.get_units_by_type(obs, units.Zerg.Hive)
      if len(hatch) > 0:
          hatch = random.choice(hatch)
          return actions.FUNCTIONS.select_point("select",(hatch.x,hatch.y))



  def move_overlord(self, obs):
    #if there is no barraks (spawning pool) build one
    overlords = self.get_units_by_type(obs, units.Zerg.Overlord)
    print("muevete")
    if len (overlords) > 0 :
        if self.unit_type_is_selected(obs, units.Zerg.Overlord):
            if self.can_do(obs, actions.FUNCTIONS.Attack_minimap.id):
                return actions.FUNCTIONS.Attack_minimap("now",(random.randint(1,63),random.randint(1,63)))

  def my_move(self, obs):
    #if there is no barraks (spawning pool) build one
    #self.attack_coordinates = [49,49]
    #self.safe_coordinates = [12,16]
    x = self.safe_coordinates[0]
    y = self.safe_coordinates[1]
    if self.unit_type_is_selected(obs, units.Zerg.Drone):
        print("move mineral resource")
        global moveallow
        moveallow = False
        global cont
        cont = 0
        global game_state
        game_state = 3
        if x < 32:
            self.safe_coordinates[0] = 20
            self.safe_coordinates[1] = 20
            return actions.FUNCTIONS.move_camera((44,20))
        else:
            self.safe_coordinates[0] = 42
            self.safe_coordinates[1] = 48
            return actions.FUNCTIONS.move_camera((18,48))
    drones = self.get_units_by_type(obs, units.Zerg.Drone)
    if len(drones) > 0 :
        drone = random.choice(drones)
        return actions.FUNCTIONS.select_point("select",(drone.x,drone.y))
    # select some random drone for the next choice

  def my_go_back(self, obs):
    #if there is no barraks (spawning pool) build one
    #self.attack_coordinates = [49,49]
    #self.safe_coordinates = [12,16]
    x = self.safe_coordinates[0]
    y = self.safe_coordinates[1]
    print("move mineral resource")
    global moveallow
    moveallow = True
    global cont
    cont = 0
    return actions.FUNCTIONS.move_camera((x,y))

  def my_more_units(self, obs, type):
    #make units
    if self.unit_type_is_selected(obs, units.Zerg.Larva):
        free_supply = (obs.observation.player.food_cap - obs.observation.player.food_used)

        # if there are no more houses (overlords) build more
        if free_supply < 2 :
            if self.can_do(obs, actions.FUNCTIONS.Train_Overlord_quick.id):
                return actions.FUNCTIONS.Train_Overlord_quick("now")

        if type == "zergling":
            # if it is possible build troops
            if self.can_do(obs, actions.FUNCTIONS.Train_Zergling_quick.id):
                print("zergling")
                return actions.FUNCTIONS.Train_Zergling_quick("now")

        if type == "drone":
            if self.can_do(obs, actions.FUNCTIONS.Train_Drone_quick.id):
                print("drone")
                return actions.FUNCTIONS.Train_Drone_quick("now")

        if type == "hydralisk":
            if self.can_do(obs, actions.FUNCTIONS.Train_Hydralisk_quick.id):
                print("hidralisk")
                return actions.FUNCTIONS.Train_Hydralisk_quick("now")


    larvae = self.get_units_by_type(obs, units.Zerg.Larva)
    if len(larvae) > 0 :
        larva = random.choice(larvae)
        return actions.FUNCTIONS.select_point("select_all_type", (larva.x,
                                                                   larva.y))

  def step(self, obs):
    super(ZergAgent, self).step(obs)


    #select/guess the location of the enemies
    if obs.first():
        player_y, player_x = (obs.observation.feature_minimap.player_relative ==
                               features.PlayerRelative.SELF).nonzero()

        xmean = player_x.mean()
        ymean = player_y.mean()

        if xmean <= 31 and ymean <= 31:
            #set pair of coordintates
            self.attack_coordinates = [49,49]
            self.safe_coordinates = [12,16]
        else:
            #set pair of coordintates
            self.attack_coordinates = [12,16]
            self.safe_coordinates = [49,49]



    #python always includes by default "self" as a parameter in the call

    global game_state
    global moveallow
    global state
    global cont
    global boostm
    global queenslimit
    cont = cont + 1

    if game_state == 1:
        #attack
        zergling_hydra_attack = self.my_attack1(obs)
        if zergling_hydra_attack:
            return zergling_hydra_attack

        if self.unit_type_is_selected(obs, units.Zerg.Overlord):
            moverlord = self.move_overlord(obs)
            global state
            if moverlord and (state == 2) :
                state = 1
                return moverlord
            make_units = self.my_more_units(obs,"zergling")
            if make_units:
                state = 2
                return make_units

        #build hatchery
        hatcheries = self.my_hatchery(obs,1)
        if hatcheries:
            return hatcheries

        #make more drones
        if len(self.get_units_by_type(obs, units.Zerg.Drone)) <= 12:
            make_units = self.my_more_units(obs,"drone")
            if make_units:
                return make_units

        #build extractor
        extractor = self.my_extractor(obs, 1)
        if extractor:
            return extractor

        #build spawning pool
        spawning_pool = self.my_spawning_pool(obs, 1)
        if spawning_pool:
            return spawning_pool

        #harvest gas
        gas = self.my_harvest_gas(obs)
        if gas:
            return gas

        #my_metabolic_boost
        mboost = self.my_metabolic_boost(obs)
        global boostm
        if mboost and boostm:
            return mboost

        #make queen
        queens =  self.get_units_by_type(obs, units.Zerg.Queen)
        global queenslimit
        if (len(queens) < 1) and queenslimit:
            make_queen = self.make_queen(obs)
            if make_queen:
                return make_queen

        #make more zerglings
        zerglings =  self.get_units_by_type(obs, units.Zerg.Zergling)
        if len(zerglings) <= 10:
            make_units = self.my_more_units(obs,"zergling")
            if make_units:
                return make_units

        #build Lair
        lair = self.my_lair(obs)
        if lair:
            return lair

        #build Den
        den = self.my_den(obs)
        if den:
            return den

        #make more hydras
        hydras =  self.get_units_by_type(obs, units.Zerg.Hydralisk)
        if len(hydras) <= 16:
            make_units = self.my_more_units(obs,"hydralisk")
            if make_units:
                return make_units

    if game_state == 2:
        #attack
        zergling_hydra_attack = self.my_attack2(obs)
        if zergling_hydra_attack:
            return zergling_hydra_attack

        if self.unit_type_is_selected(obs, units.Zerg.Overlord):
            moverlord = self.move_overlord(obs)
            if moverlord and (state == 2) :
                state = 1
                return moverlord
            make_units = self.my_more_units(obs,"zergling")
            if make_units:
                state = 2
                return make_units

        #build hatchery
        hatcheries = self.my_hatchery(obs,1)
        if hatcheries:
            return hatcheries

        #make more drones
        if len(self.get_units_by_type(obs, units.Zerg.Drone)) <= 6:
            make_units = self.my_more_units(obs,"drone")
            if make_units:
                return make_units

        #build extractor
        extractor = self.my_extractor(obs, 2)
        if extractor:
            return extractor

        #build spawning pool
        spawning_pool = self.my_spawning_pool(obs, 1)
        if spawning_pool:
            return spawning_pool

        #harvest gas
        gas = self.my_harvest_gas(obs)
        if gas:
            return gas

        #harvest mineral
        #mineral = self.my_harvest_minerals(obs)
        #if mineral:
        #    return mineral

        #my_metabolic_boost
        mboost = self.my_metabolic_boost(obs)
        if mboost and boostm:
            return mboost

        #make queen
        queens =  self.get_units_by_type(obs, units.Zerg.Queen)
        if (len(queens) < 1) and queenslimit:
            make_queen = self.make_queen(obs)
            if make_queen:
                return make_queen

        #make more zerglings
        zerglings =  self.get_units_by_type(obs, units.Zerg.Zergling)
        if len(zerglings) <= 10:
            make_units = self.my_more_units(obs,"zergling")
            if make_units:
                return make_units

        #build Lair
        lair = self.my_lair(obs)
        if lair:
            return lair

        #build Den
        den = self.my_den(obs)
        if den:
            return den

        #make more hydras
        hydras =  self.get_units_by_type(obs, units.Zerg.Hydralisk)
        if len(hydras) <= 15:
            make_units = self.my_more_units(obs,"hydralisk")
            if make_units:
                return make_units
        elif cont > 400:
            if moveallow:
                move = self.my_move(obs)
                if move :
                    return move
            else:
                move = self.my_go_back(obs)
                if move :
                    return move

    if game_state == 3:
        #attack
        zergling_hydra_attack = self.my_attack2(obs)
        if zergling_hydra_attack:
            return zergling_hydra_attack

        if self.unit_type_is_selected(obs, units.Zerg.Overlord):
            moverlord = self.move_overlord(obs)
            if moverlord and (state == 2) :
                state = 1
                return moverlord
            make_units = self.my_more_units(obs,"zergling")
            if make_units:
                state = 2
                return make_units

        if cont > 400:
            if moveallow:
                move = self.my_move(obs)
                if move :
                    return move
            else:
                move = self.my_go_back(obs)
                if move :
                    return move

        #build hatchery
        hatcheries = self.my_hatchery(obs,1)
        if hatcheries:
            return hatcheries

        #make more drones
        if len(self.get_units_by_type(obs, units.Zerg.Drone)) <= 3:
            make_units = self.my_more_units(obs,"drone")
            if make_units:
                return make_units

        #build extractor
        extractor = self.my_extractor(obs, 2)
        if extractor:
            return extractor


        #harvest gas
        gas = self.my_harvest_gas(obs)
        if gas:
            return gas

        #my_metabolic_boost
        mboost = self.my_metabolic_boost(obs)
        if mboost and boostm:
            return mboost

        #make queen
        queens =  self.get_units_by_type(obs, units.Zerg.Queen)
        if (len(queens) < 1) and queenslimit:
            make_queen = self.make_queen(obs)
            if make_queen:
                return make_queen

        #make more zerglings
        zerglings =  self.get_units_by_type(obs, units.Zerg.Zergling)
        if len(zerglings) <= 10:
            make_units = self.my_more_units(obs,"zergling")
            if make_units:
                return make_units

        #build Lair
        lair = self.my_lair(obs)
        if lair:
            return lair



        #make more hydras
        hydras =  self.get_units_by_type(obs, units.Zerg.Hydralisk)
        if len(hydras) <= 100:
            make_units = self.my_more_units(obs,"hydralisk")
            if make_units:
                return make_units

        #harvest mineral
        mineral = self.my_harvest_minerals(obs)
        if mineral:
            return mineral
    return actions.FUNCTIONS.no_op()  #do not do anything if there were no matches

def main(unused_argv):
  agent = ZergAgent()
  try:
    while True:
      with sc2_env.SC2Env(
          map_name="Simple64",
          players=[sc2_env.Agent(sc2_env.Race.zerg),
                   sc2_env.Bot(sc2_env.Race.random,
                               sc2_env.Difficulty.easy)],
          agent_interface_format=features.AgentInterfaceFormat(
              feature_dimensions=features.Dimensions(screen=84, minimap=64),
              use_feature_units=True),
          step_mul=6,
          game_steps_per_episode=0,
          visualize=True) as env:

        agent.setup(env.observation_spec(), env.action_spec())

        timesteps = env.reset()
        agent.reset()

        while True:
          step_actions = [agent.step(timesteps[0])]
          if timesteps[0].last():
            break
          timesteps = env.step(step_actions)

  except KeyboardInterrupt:
    pass

if __name__ == "__main__":
    app.run(main)
