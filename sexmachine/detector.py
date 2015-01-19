"""Module for getting a gender based on name and optional country."""

import os.path

from codecs import open as copen
from six import viewkeys

from .mapping import map_name


class NoCountryError(Exception):

    """Raised when non-supported country is queried."""
    pass


class Detector:
    """Get gender by first name."""

    COUNTRIES = """great_britain ireland usa italy malta portugal spain france
                   belgium luxembourg the_netherlands east_frisia germany
                   austria swiss iceland denmark norway sweden finland estonia
                   latvia lithuania poland czech_republic slovakia hungary
                   romania bulgaria bosniaand croatia kosovo macedonia
                   montenegro serbia slovenia albania greece russia belarus
                   moldova ukraine armenia azerbaijan georgia the_stans turkey
                   arabia israel china india japan korea vietnam other_countries
                 """.split()

    def __init__(self,
                 case_sensitive=True,
                 unknown_value="andy"):

        """Creates a detector parsing given data file.

        Args:
            case_sensitive (''bool''): Whether it's case sensitive or not.
            unknown_value (''str''): The value returned when unknown (not m/f).
        """
        self.case_sensitive = case_sensitive
        self.unknown_value = unknown_value
        self._parse(os.path.join(os.path.dirname(__file__),
                                 "data/nam_dict.txt"
                                 )
                    )

    def _parse(self, filename):
        """Opens data file and for each line, calls _eat_name_line.

        Args:
            filename (''str''): Filename for the data file.
        """
        self.names = {}
        with copen(filename, encoding="iso8859-1") as f:
            for line in f:
                if any(map(lambda c: 128 < ord(c) < 160, line)):
                    line = line
                self._eat_name_line(line.strip())

    def _eat_name_line(self, line):
        """Parses one line of data file.

        Args:
            line (''str''): A line form the data file.
        """
        if line[0] not in "#=":
            parts = line.split()
            country_values = line[30:-1]
            name = map_name(parts[1])
            if not self.case_sensitive:
                name = name.lower()

            if parts[0] == "M":
                self._set(name, "male", country_values)
            elif parts[0] == "1M" or parts[0] == "?M":
                self._set(name, "mostly_male", country_values)
            elif parts[0] == "F":
                self._set(name, "female", country_values)
            elif parts[0] == "1F" or parts[0] == "?F":
                self._set(name, "mostly_female", country_values)
            elif parts[0] == "?":
                self._set(name, self.unknown_value, country_values)
            else:
                raise "Not sure what to do with a sex of %s" % parts[0]

    def _set(self, name, gender, country_values):
        """Set gender and country values for names dictionary of detector.

        Args:
            name (''str''): Name of the person.
            gender (''str''): The gender of the person
            country_values (''str''): The country.
        """
        if '+' in name:
            for replacement in ['', ' ', '-']:
                self._set(name.replace('+', replacement),
                          gender,
                          country_values
                          )
        else:
            if name not in self.names:
                self.names[name] = {}
            self.names[name][gender] = country_values

    def _most_popular_gender(self, name, counter):
        """Find the most popular gender for the given name by given counter

        Args:
            name (''str''): The Name.
            counter (''int''): The number given for popularity of the name
                based on the country. 1 (=rare) to 13 (=extremely common). See
                the link in readme about the data file for more information.
        Return:
            Best value for a name.
        """
        if name not in self.names:
            return self.unknown_value

        max_count, max_tie = (0, 0)
        best = [a for a in viewkeys(self.names[name])][0]
        for gender, country_values in self.names[name].items():
            count, tie = counter(country_values)
            if count > max_count or (count == max_count and tie > max_tie):
                max_count, max_tie, best = count, tie, gender

        return best if max_count > 0 else self.unknown_value

    def counter(self, country_values):
        """Find the value for the country values

        Args:
            country_values (''List of chars''):
        Return:
            tuple with length of the country values and a value
        """
        country_values = [ord(a) for a in country_values]
        return (len(country_values),
                sum(map(lambda c: c > 64 and c-55 or c-48, country_values)))

    def get_gender(self, name, country=None):
        """Returns best gender for the given name and country pair

        Args:
            name (''str''): The name to look up
            Country (''str''): Name of a country or None
        Return:
            The best gender for the given name and country pair
        """
        if not self.case_sensitive:
            name = name.lower()

        if name not in self.names:
            return self.unknown_value
        elif not country:

            return self._most_popular_gender(name, self.counter)
        elif country in self.__class__.COUNTRIES:
            index = self.__class__.COUNTRIES.index(country)
            counter = lambda e: (ord(e[index])-32, 0)
            return self._most_popular_gender(name, counter)
        else:
            raise NoCountryError("No such country: %s" % country)
