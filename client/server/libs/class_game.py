from datetime import datetime
class Game():
    def __init__(self, player = None):
        self.player = player
        self.__reset()
    
    def __reset(self):
        self.type = 0 # 0 local 1 remote
        self.status = None
        self.id = None
        self.time_start = None
        self.num_players = None
        self.distance = None
        self.players_data = {}        
        self._serialize_reponse = {}
    
    def set_status(self, status):
        self.status = status
    
    def get_status(self):
        return self.status
    
    def set_id(self, id):
        self.id = id
    
    def get_id(self):
        return self.id
    
    def set_num_players(self, num_players):
        self.num_players = int(num_players)
    
    def get_num_players(self):
        return self.num_players
        
    def set_distance(self, distance):
        self.distance = float(distance)
    
    def get_distance(self):
        return self.distance
    
    
    def get_players_data(self):
        return self.players_data
    
    def get_serializate_data(self):
        return self._serialize_reponse     
    
    def create(self, data):
        self.__reset()
        self.player.set_master()
        self.set_num_players(data['game_num_players'])
        self.set_distance(data['game_distance'])  
        if(self.get_num_players() == 1):
            #Return local game id 0
            self.set_id(0)
            self._serialize_reponse = {'game_id': self.get_id()}
            return True
        elif(self.get_num_players() > 1):
            #Call http request to server
            self.type = 1
            self._serialize_reponse = {}
            pass
        return False    
    
    def join_player(self, game_id):
        if(self.type):
            #http request
            #self.set_num_players(data['game_num_players'])
            #self.set_distance
            pass
        else:
            self.set_status(2)           
            return {'game_num_players': self.get_num_players(), 'game_distance': self.get_distance()}
    
    def get_status_game(self):
        response = {'game_id': self.get_id(), 'game_status': self.get_status(), 'game_players': {}}        
        if(self.type):
            #http request
            pass
        #Append data local user
        response['game_players']['0'] = self.player.get_data()
        if(self.time_start):
            response['game_time'] = str(datetime.now() - self.time_start)
        return response
    
    def start(self):
        if(self.type):
            #http request
            pass
        else:
            self.set_status(4)
            return True
    
    def start_player(self):
        if(self.type):
            #http request
            pass
        else:
            self.set_status(5)
            self.time_start = datetime.now()
        self.player.run()
        return True
    
    def end_player(self):
        if(self.type):
            #http request
            pass
        else:
            self.set_status(6)
        self.player.stop()
        return True

        
            