'''
	This serves as the ANML class file in Python with support for 
    counters, logic gates and cellular automata.
    Author: Tom Tracy II (tjt7a@virginia.edu)
'''
from enum import Enum


class AnmlDefs(Enum):
    """ Enums for valid start states"""
    ALL_INPUT = 1
    NO_START = 2



class Element(Object):
    """ Parent class for ANML elements"""
    pass

class Counter(object):
    """"A class that represents a counter element in an automaton network"""

    def __init__(self, *args, **kwargs):

        self.neighbors_ = []
        self.target = str(args[0])
        self.id_ = str(kwargs['anmlId'])

        assert type(self.id_) == str, "Counter ID is not valid"
    
    def add_edge(self, ste):
        """ This function connects self to an STE state"""
        assert isinstance(ste, Ste), "ste is not a valid STE, it is a {}".format(type(ste))
        self.neighbors_.append(ste)
    
    def add_edges(self, stes):
        """A function that connects self to several states."""
        for ste in stes:
            self.add_edge(ste)
        
    def __str__(self):
        """A function that prints out the ANML-formatted counter representation"""
        string = "\t\t<counter " + "at-target=\"" + self.at_target + "\"  " + "id=\"" + self.id_ + \
            "\" target=\"" + self.target + "\">\n"
        for neighbor in self.neighbors:
            string += "\t\t\t<activate-on-target element=\"" + \
                neighbor.id_ + "\"/>\n"
        string += "\t\t</counter>\n"
        return string



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
        self.elements_ = []
        self.id_ = aId

    def __str__(self):
        """String representation of the ANML network generates the ANML file"""

        string = "<anml version=\"1.0\"  xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n"
        string += "\t<automata-network id=\"" + self.id_ + "\">\n"
        for element in self.elements_:
            string += '\t\t' + str(ste)
        string += '\t</automata-network>\n'
        string += '</anml>\n'
        return string

    def AddSTE(self, *args, **kargs):
        """Add one state to the network"""

        ste = Ste(*args, **kargs)

        self.elements_.append(ste)
        return ste
    
    def AddCounter(self, *args, **kargs):
        """Add one counter to the network"""

        counter = Counter(*args, **kargs)

        self.elements_.append(counter)
        return counter

    def AddAnmlEdge(self, element1, element2):
        """Add an edge between element1 and element2"""

        element1.add_edge(element2)

    def AddAnmlEdges(self, element1, elements, stuff):
        """Add an edge between element1 and all elements in elements"""

        element1.add_edges(elements)

    def ExportAnml(self, filename):
        """Write out the automaton network to a file"""

        with open(filename, 'w') as f:
            f.write(str(self))
        return 0

class Macro(Anml):
    """ A class that represents a Macro definition inherits from Anml"""

    def __init__(self, *args, **kwargs):

        self.id_ = str(kwargs['anmlId'])
    
    def __str__(self):
        """Override ANML's __str__ method for Macros"""

        string = "<macro-definition id=\"" + self.id_ + "\" + name=\"" + self.name_ + "\">\n"
        string += "\t<header>\n"
        string += "\t\t<interface-declarations>\n"
        #for interface_declaration in interface_declarations: **For now not implemented**
        string += "\t\t</interface-declarations\n"

        string += "\t\t<parameter-declarations>\n"
        for parameter in self.parameters:
            string += "\t\t\t<parameter parameter-name=\"" + parameter.name_ + \
                "\""
            if parameter.default_value_:
                string += " default-value=\"" + parameter.default_value + "\"/>\n"
        string += "\t\t</parameter-declarations>\n"
        string += "\t</header>\n"

        string += "\t<body>\n"
        string += "\t\t<port-definitions>\n"
        # for port_definition in port_definitions: **For now not implemented**
        string += "\t\t</port-definitions>\n"

        for element in self.elements_:
            string += '\t\t\t' + str(ste)

        string += "\t</body>"
        string += '</macro-definition>\n'
        return string


if __name__ == "__main__":
    """ Test the class definitions"""

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
