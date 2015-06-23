import os.path
import codecs
from .mapping import map_name


class NoCountryError(Exception):
    """Raised when non-supported country is queried"""
    pass


class Detector:
    """Get gender by first name"""

    COUNTRIES = u"""great_britain ireland usa italy malta portugal spain france
                   belgium luxembourg the_netherlands east_frisia germany austria
                   swiss iceland denmark norway sweden finland estonia latvia
                   lithuania poland czech_republic slovakia hungary romania
                   bulgaria bosniaand croatia kosovo macedonia montenegro serbia
                   slovenia albania greece russia belarus moldova ukraine armenia
                   azerbaijan georgia the_stans turkey arabia israel china india
                   japan korea vietnam other_countries
                 """.split()

    def __init__(self,
                 case_sensitive=True,
                 unknown_value=u"andy"):

        """Creates a detector parsing given data file"""
        self.case_sensitive = case_sensitive
        self.unknown_value = unknown_value
        self._parse(os.path.join(os.path.dirname(__file__), "data/nam_dict.txt"))

    def _parse(self, filename):
        """Opens data file and for each line, calls _eat_name_line"""
        self.names = {}
        with codecs.open(filename, encoding="iso8859-1") as f:
            for line in f:
                if any(map(lambda c: 128 < ord(c) < 160, line)):
                    line = line.encode("iso8859-1").decode("windows-1252")
                self._eat_name_line(line.strip())

    def _eat_name_line(self, line):
        """Parses one line of data file"""
        if line[0] not in "#=":
            parts = line.split()
            country_values = line[30:-1]
            name = map_name(parts[1])
            if not self.case_sensitive:
                name = name.lower()

            if parts[0] == "M":
                self._set(name, u"male", country_values)
            elif parts[0] == "1M" or parts[0] == "?M":
                self._set(name, u"mostly_male", country_values)
            elif parts[0] == "F":
                self._set(name, u"female", country_values)
            elif parts[0] == "1F" or parts[0] == "?F":
                self._set(name, u"mostly_female", country_values)
            elif parts[0] == "?":
                self._set(name, self.unknown_value, country_values)
            else:
                raise "Not sure what to do with a sex of %s" % parts[0]

    def _set(self, name, gender, country_values):
        """Sets gender and relevant country values for names dictionary of detector"""
        if '+' in name:
            for replacement in ['', ' ', '-']:
                self._set(name.replace('+', replacement), gender, country_values)
        else:
            if name not in self.names:
                self.names[name] = {}
            self.names[name][gender] = country_values

    def _most_popular_gender(self, name, counter):
        """Finds the most popular gender for the given name counting by given counter"""
        if name not in self.names:
            return self.unknown_value

        max_count, max_tie = (0, 0)
        best = next(iter(self.names[name].keys()))
        for gender, country_values in self.names[name].items():
            count, tie = counter(country_values)
            if count > max_count or (count == max_count and tie > max_tie):
                max_count, max_tie, best = count, tie, gender

        return best if max_count > 0 else self.unknown_value

    def get_gender(self, name, country=None):
        """Returns best gender for the given name and country pair"""
        if not self.case_sensitive:
            name = name.lower()

        if name not in self.names:
            return self.unknown_value
        elif not country:
            def counter(country_values):
                country_values = map(ord, country_values.replace(" ", ""))
                return (len(list(country_values)),
                        sum(map(lambda c: c > 64 and c-55 or c-48, country_values)))
            return self._most_popular_gender(name, counter)
        elif country in self.__class__.COUNTRIES:
            index = self.__class__.COUNTRIES.index(country)
            counter = lambda e: (ord(e[index])-32, 0)
            return self._most_popular_gender(name, counter)
        else:
            raise NoCountryError("No such country: %s" % country)
