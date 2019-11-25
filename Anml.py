'''
	This serves as the ANML class file in Python with cellular automata
	support.
'''
from enum import Enum


class AnmlDefs(Enum):
    ALL_INPUT = 1
    NO_START = 2

class Logic(object):
	"""A class that represents a logic element in an automaton network"""

	def __init__(self, *args, **kwargs):

		self.neighbors_ = []
		self.id_ = str(kwargs['logicId'])

		assert type(self.id_) == str, "Logic ID is not valid!"

	def add_edge(self, ste):
		""" This function connects self to an STE state"""
		""" QUESTION: Do we want to be able to connect multiple logics?"""
		assert isinstance(ste, Ste), "ste is not a valid STE, it is a {}".format(type(ste))
		self.neighbors_.append(ste)

	def add_edges(self, stes):
		"""A function that connects self to several states."""
        for ste in stes:
            self.add_edge(ste)

    def __str__(self):
		"""A function that prints out the ANML-formatted logic representation"""
        string = "<logic-element id=\"" + self.id_ + "\""
		string += "\t\t</logic-element>\n"
		return string


class Ste(object):
    """ A class that represents an automaton state"""

    # anmlId, character_class, defs, match=False, reportCode=None):
    def __init__(self, *args, **kwargs):

        self.neighbors_ = []

        self.character_class_ = args[0]
        self.defs_ = args[1]
        self.starting_ = False
        self.reportCode_ = None
        self.matching_ = False

        self.id_ = str(kwargs['anmlId'])

        assert type(self.id_) == str, "STE ID is not valid!"

        if 'reportCode' in kwargs:
            self.reportCode_ = str(kwargs['reportCode'])

        if 'match' in kwargs:
            self.matching_ = kwargs['match']

        if self.defs_ == AnmlDefs.ALL_INPUT:
            self.starting_ = True
            self.start_type_ = 'all-input'

    def add_edge(self, ste2):
        """A function that connects self to another state."""
        assert isinstance(ste2, Ste), "ste2 is not a valid STE, it is a {}".format(type(ste2))
        self.neighbors_.append(ste2)

    def add_edges(self, stes):
        """A function that connects self to several other states."""
        for ste in stes:
            self.add_edge(ste)

    def __str__(self):

        string = "<state-transition-element id=\"" + self.id_ + \
            "\" symbol-set=\"" + ''.join(self.character_class_) + "\""
        if self.starting_:
            string += " start=\"" + self.start_type_ + "\">\n"
        else:
            string += ">\n"
        if self.reportCode_ is not None:
            string += "\t\t\t<report-on-match reportcode=\"" +\
                self.reportCode_ + "\"/>\n"
        for neighbor in self.neighbors_:
            string += "\t\t\t<activate-on-match element=\"" + \
                neighbor.id_ + "\"/>\n"
        string += "\t\t</state-transition-element>\n"
        return string


class Anml(object):
    """A class that represents an automaton graph."""

    def __init__(self, aId="an1"):
        self.stes_ = []
        self.id_ = aId

    def __str__(self):
        """String representation of the ANML network generates the ANML file"""

        string = "<anml version=\"1.0\"  xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n"
        string += "\t<automata-network id=\"" + self.id_ + "\">\n"
        for ste in self.stes_:
            string += '\t\t' + str(ste)
        string += '\t</automata-network>\n'
        string += '</anml>\n'
        return string

    def AddSTE(self, *args, **kargs):
        """Add one state to the network"""

        ste = Ste(*args, **kargs)

        self.stes_.append(ste)
        return ste

    def AddAnmlEdge(self, ste1, ste2):
        """Add an edge between ste1 and ste2"""

        ste1.add_edge(ste2)

    def AddAnmlEdges(self, ste1, stes, stuff):
        """Add an edge between ste1 and all stes in stes"""

        ste1.add_edges(stes)

    def ExportAnml(self, filename):
        """Write out the automaton network to a file"""

        with open(filename, 'w') as f:
            f.write(str(self))
        return 0


if __name__ == "__main__":

    anml = Anml()

    stes = []

    report_symbol = r"\x%02X" % 255

    for i in range(10):
        if i == 0:
            start_ste = anml.AddSTE(report_symbol, AnmlDefs.ALL_INPUT,
                                    anmlId=i, match=False)
            stes.append(start_ste)
        else:
            character_class = r"\x%02X" % i
            ste = anml.AddSTE(character_class, AnmlDefs.NO_START,
                              anmlId=i, match=False)
            anml.AddAnmlEdge(stes[-1], ste, 0)
            stes.append(ste)

    ste = anml.AddSTE(report_symbol, AnmlDefs.NO_START,
                      anmlId=10, reportCode=10)
    anml.AddAnmlEdge(stes[-1], ste, 0)
    anml.ExportAnml("test_anml.anml")
