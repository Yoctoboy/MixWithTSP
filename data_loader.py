from datetime import datetime

from helpers import tone_map
from tsp_manager import TSPManager


def get_tsp_manager(filename):
    data_loader = DataLoader(filename)
    return data_loader.load()


class DataLoader(object):
    def __init__(self, filename):

        """Constructor for Dataloader
        
        Arguments:
            filename {string} -- string of the file containing initial data
        """

        self.filename = filename
    
    def load(self):
        """
        Performs loading of the data
        
        Returns:
            TSPManager -- Manager that will perform TSP resolution
        """

        
        data = open(self.filename, "r").readlines()
        songs = []
        for line in data[1:]:
            song_dict = self.get_song_dict(line[:-1])
            songs.append(song_dict)

        manager = TSPManager(songs)
        
        return manager
    
    def get_song_dict(self, l):
        """
        Transforms a line of a file into a song dictionnary
        
        Arguments:
            l {list} -- string of one line of data
        
        Returns:
            dict -- song dictionary
        """

        result = {}
        song_list = self.get_actual_list(l)
        result["id"] = int(song_list[0])
        result["name"] = song_list[1]
        result["bpm"] = float(song_list[2].replace(',', '.'))
        result["track_length"] = self.get_track_length(song_list[3])
        result["key_tone"] = self.get_key_tone(song_list[4])
        return result

    def get_actual_list(self, l):
        """
        Returns the actual list correctly split
        
        Arguments:
            l {string} -- input string
        
        Returns:
            list -- raw data list of one song
        """

        return filter(lambda x: x!='', l.split("	"))

    def get_track_length(self, s):
        """
        Returns the track length of a song gevin the length string
        
        Arguments:
            s {string} -- length string
        
        Returns:
            int -- amount of seconds the track lasts
        """

        time_object = datetime.strptime(s, "%M:%S")
        return 60*time_object.minute + time_object.second

    def get_key_tone(self, s):
        """
        Returns the key tone of the song (given camelot format)
        
        Arguments:
            s {string} -- camelot format of the track
        
        Returns:
            list -- rekordbox format of the track
        """

        return tone_map[s]