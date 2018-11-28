from datetime import datetime
import io

from helpers import tone_map
from tsp_manager import TSPManager


def get_tsp_manager(filename, shifts_allowed, result_file):
    data_loader = DataLoader(filename, shifts_allowed, result_file)
    return data_loader.load()


class DataLoader(object):
    def __init__(self, filename, shifts_allowed, result_file):

        """Constructor for Dataloader
        
        Arguments:
            filename {string} -- string of the file containing initial data
            shifts_allowed {int} -- amount of shifts we allow before applying TSP
        """

        self.filename = filename
        self.shifts_allowed = shifts_allowed
        self.result_file = result_file
    
    def load(self):
        """
        Performs loading of the data
        
        Returns:
            TSPManager -- Manager that will perform TSP resolution
        """

        
        data = io.open(self.filename, "r", encoding='utf-16-le').readlines()
        songs = []
        for line in data[1:]:
            song_dict = self.get_song_dict(line[:-1])
            songs.append(song_dict)

        manager = TSPManager(songs, self.shifts_allowed, self.result_file)
        
        return manager
    
    def get_song_dict(self, l):
        """
        Transforms a line of a file into a song dictionnary
        
        Arguments:
            l {string} -- string of one line of data
        
        Returns:
            dict -- song dictionary
        """

        result = {}
        song_list = l.split("	")
        result["id"] = int(song_list[0])
        result["name"] = song_list[2]
        result["bpm"] = float(song_list[6].replace(',', '.'))
        result["track_length"] = self.get_track_length(song_list[7])
        result["key_tone"] = self.get_key_tone(song_list[8])
        return result

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