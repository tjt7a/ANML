'''
    This serves as the ANML class file in Python with support for
    counters, logic gates and [under construction] cellular automata.
    Author: Tom Tracy II (tjt7a@virginia.edu)
    
    ** WARNING: Macros and non-STEs have not been tested yet **
'''
from enum import Enum
from networkx import drawing
import re
import xml.etree.cElementTree as ET


class AnmlDefs(Enum):
    """ Enums for valid start states"""
    ALL_INPUT = 1
    NO_START = 2
    START_OF_DATA = 3


class Element(object):
    """ Parent class for ANML elements including:
        STE, counter, logic
    """

    def __init__(self, *args, **kwargs):

        # A list of elements that this element is connected to
        self.neighbors_ = []

        # The unique id of this element
        self.id_ = str(kwargs['anmlId'])

        # The type of this element
        self.type_ = self.__class__.__name__

        # Verifying that the id is a string
        assert type(self.id_) == str, "{} ID {} is not valid".format(
            self.type_, self.id_)

    def add_edge(self, element):
        """This function connects self to another element"""
        
        assert isinstance(
            element, Element), "{} is not a valid Element type".format(element)

        # Adding the element to the list of neighbors
        self.neighbors_.append(element)

    def add_edges(self, elements):
        """This function connects self to several elements"""

        # Add each element as a new neighbor
        for element in elements:
            self.add_edge(element)


class Counter(Element):
    """A class that represents a counter element in an automata network"""

    def __init__(self, *args, **kwargs):
        
        # Call the parent class's init method first, then add element-specific code
        super().__init__(*args, **kwargs)

        # Set the count target for the counter
        self.at_target_ = str(args[0])

    def __str__(self):
        """A function that prints out the ANML-formatted counter representation"""
        
        string = "\t\t<counter " + \
            "at-target=\"" + self.at_target + "\" " + \
            "id=\"" + self.id_ + "\">\n"

        # Iterate through each neighbor and add edge
        for neighbor in self.neighbors_:
            string += "\t\t\t<activate-on-target " + \
                "element=\"" + neighbor.id_ + "\"/>\n"

        string += "\t\t</counter>\n"
        return string
    
    
class Logic(Element):
    """ A class that represents a logic element in an automaton network
        *** INCOMPLETE ***
        TODO: We need to figure out a good way to represent logic
        A good way to represent each cell's input would be a 9x1 vector such as In = [C N NE E SE S SW W NW]
    """
    
    def __init__(self, *args, **kwargs):
        
        # Call the parent class's init method first, then add element-specific code
        super().__init__(*args, **kwargs)
        
        # Set the logic expression for this logic element
        self.logic_ = str(args[0])
        print("WARNING: Logic Elements are INCOMPLETE and do NOT function")

    def __str__(self):
        """A function that prints out the ANML-formatted logic representation"""
     
        string = "\t\t<logic-element " + "logic=\"" + self.logic_ + "\" " + "id=\"" + self.id_# + "\""
        
        # Iterate through each neighbor and add edge
        for neighbor in self.neighbors_:
            string += "\t\t\t<activate-on-true " + \
                "element=\"" + neighbor.id_ + "\"/>\n"

        string += "\t\t</logic-element>\n"
        return string


class Ste(Element):
    """ A class that represents an automaton state"""

    # anmlId, character_class, defs, match=False, reportCode=None):
    def __init__(self, *args, **kwargs):

        # Call the parent class's init method first, then add element-specific code
        super().__init__(*args, **kwargs)

        # Load character class and defs
        self.character_class_ = args[0]
        self.defs_ = args[1]

        if 'reportCode' in kwargs:
            self.reportCode_ = str(kwargs['reportCode'])
        else:
            self.reportCode_ = None

        if 'match' in kwargs:
            self.matching_ = kwargs['match']
        else:
            self.matching_ = False

        if self.defs_ == AnmlDefs.ALL_INPUT:
            self.starting_ = True
            self.start_type_ = 'all-input'
        elif self.defs_ == AnmlDefs.START_OF_DATA:
            self.starting_ = True
            self.start_type_ = 'start-of-data'
        else:
            self.starting_ = False
            self.start_type = 'no-start'

    def __str__(self):

        symbol_set = ''.join(self.character_class_)

        # Replace the escape character with the hex for the symbol
        if symbol_set == '\\':
            print("FOUND A backslash that needs replacing with hex")
            symbol_set = "\\x5C"
            print("Symbol_set: ", symbol_set)
            print("ID: ", self.id_)
            #exit()

        string = "\t\t<state-transition-element id=\"" + self.id_ + "\" " + \
            "symbol-set=\"" + symbol_set + "\" "
        if self.starting_:
            string += "start=\"" + self.start_type_ + "\">\n"
        else:
            string += ">\n"
        if self.matching_:
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
            string += str(element)
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

    def AddAnmlEdge(self, element1, element2, *other):
        """Add an edge between element1 and element2"""

        element1.add_edge(element2)

    def AddAnmlEdges(self, element1, elements, *other):
        """Add an edge between element1 and all elements in elements"""

        element1.add_edges(elements)

    def ExportAnml(self, filename):
        """Write out the automaton network to a file"""

        with open(filename, 'w') as f:
            f.write(str(self))
        
        return 0
    
    def CreateMacroDef(self, **kwargs):
        """Creates a macro definition"""
        
        macro = Macro(**kwargs)
        
        return macro

    def parseHDOT(self, dotfile):
        """ Parse homogeneous DOT file and extract data"""

        graph = drawing.nx_pydot.read_dot(dotfile)

        start = []
        accept = []
        nodes = {}
        edges = {}

        # Iterate through al the nodes
        for node_id, node_info in graph.nodes.items():

            shape = None

            if node_id == 'START':
                start.append(node_id)
                value = '*'
                nodes[node_id] = value
                continue

            if 'label' not in node_info:
                continue
            if 'shape' in node_info:
                shape = node_info['shape']

            # This is where stuff is broken
            label = node_info['label']
            print("LABEL: ", label)
            first_newline = label.index("\\n")
            first_double_newline  = label.index("\\n\\n", first_newline + 1)
            index = label[1:first_newline]
            rest = label[first_newline + 2: first_double_newline]
            print("What we use: ", rest)

            assert node_id == index, "Indexes don't match"

            value = rest
            # Ignore
            if value == 'START-DS' or value == 'ACCEPT-EOD':
                continue
            if value == 'START':
                start.append(node_id)
                value = '*'
            if value == 'ACCEPT':
                accept.append(node_id)
                value = '*'
            if shape == 'doublecircle':
                print("ACCEPTING: ", node_id)
                assert node_id not in accept
                accept.append(node_id)
            
            # Set nodes[name] to character set of the node
            nodes[node_id] = value
    
        for edge, _ in graph.edges.items():
            src = edge[0]
            dst = edge[1]

            print(src, dst)

            if src in edges:
                edges[src].append(dst)
            else:
                edges[src] = [dst]
        
        return start, accept, nodes, edges

    @staticmethod
    def sanitize_symbol_set(ss):
        """ This method was ported from VASim's ste.cpp
            Because VAsim's XML parser sometimes chokes on 
            special characters
        """

        ss = re.sub('(?<!\\\)]]', "]\\]", ss)
        ss = ss.replace("\\[", "\\x5B")
        ss = ss.replace("\\]", "\\x5D")
        ss = ss.replace("&", "\\x26")
        ss = ss.replace("<", "\\x3C")
        ss = ss.replace(">", "\\x3E")
        ss = ss.replace("\"", "\\x22")
        ss = ss.replace("\'", "\\x27")

        return ss

    def FromDOT(self, dotfile):
        """Generates an ANML object from a DOT file"""

        start, accept, nodes, edges = self.parseHDOT(dotfile)

        # print("HDOT Results:")
        # print("Start: ", start)
        # print("Accept: ", accept)
        # print("Nodes: ", nodes)
        # print("Edges: ", edges)

        #anml = Anml()
        stes = {}

        # Our start nodes are virtual, so let's make their neighbors start nodes
        real_start_nodes = list()

        # Grab the real start nodes
        for node in start:
            if node in edges.keys():
                for dst in edges[node]:
                    real_start_nodes.append(dst)


        for node, character_set in nodes.items():

            if node in start:
                continue

            start_type = AnmlDefs.NO_START
            match = False
            report_code = None

            # Because VASim's xml parser sometimes can't handle special characters,
            # we're going to sanitize some special substrings in our char sets
            character_set = Anml.sanitize_symbol_set(character_set)

            if node in real_start_nodes:

                start_type = AnmlDefs.ALL_INPUT
            
            if node in accept:
                report_code = node
                match = True

            ste = self.AddSTE(character_set, start_type,
                    anmlId=node, match=match, reportCode=report_code)

            stes[node] = ste
        
        for src, dsts in edges.items():

            if src in start:
                continue

            if src not in nodes:
                continue

            for dst in dsts:

                if dst not in nodes:
                    continue

                self.AddAnmlEdge(stes[src], stes[dst], 0)

    @classmethod
    def from_anml(cls, anml_filename):

        with open(anml_filename, 'r') as f:

            anml_tree = ET.parse(anml_filename)
            anml_root = anml_tree.getroot()

            return anml_root
            


class Macro(Anml):
    """ A class that represents a Macro definition inherits from Anml"""
    
    class Parameter(object):
        """ Class definition for Macro Parameters"""
        
        def __init__(self, name, default_value):
            self.name_ = None
            self.default_value_ = None

    def __init__(self, *args, **kwargs):

        self.id_ = str(kwargs['anmlId'])
        #self.name_ = str(kwargs['name'])
        self.parameters_ = []
    
    def AddMacroParam(self, *args, **kwargs):
        """Add a parameter to the macro definition"""
        
        parameter = Parameter(kwargs['paramName'], kwargs['elementRefs'])
        
        self.parameters_.append(parameter)
        
    
    def __str__(self):
        """Override ANML's __str__ method for Macros"""

        string = "<macro-definition id=\"" + self.id_ + "\" + name=\"" + self.name_ + "\">\n"
        string += "\t<header>\n"
        string += "\t\t<interface-declarations>\n"
        # for interface_declaration in interface_declarations: **For now not implemented**
        string += "\t\t</interface-declarations\n"

        string += "\t\t<parameter-declarations>\n"
        for parameter in self.parameters_:
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
            string += '\t\t\t' + str(element)

        string += "\t</body>"
        string += '</macro-definition>\n'
        return string


if __name__ == "__main__":
    """ Test the class definitions"""

    #dotfile = '/home/tjt7a/src/hyperscan/build/bin/third_hyperscan/dump_3/Expr_0_00_before_asserts.dot'
    #dotfile = '/home/tjt7a/src/hyperscan/build/bin/first_hyperscan/dump_0/rose_nfa_1.dot'
    # dotfile = '/home/tjt7a/src/hyperscan/build/bin/first_hyperscan/dump_0/rose_nfa_2.dot'
    # automata_file = 'test_anml.anml'

    # anml = Anml()
    # anml = anml.FromDOT(dotfile)
    # anml.ExportAnml(automata_file)

    anml = Anml()

    root = Anml.from_anml("example_anml.anml")

    for child in root.iter('state-transition-element'):
        child_id = child.attrib["id"]
        child_symbolset = child.attrib["symbol-set"]
        child_start = child.attrib["start"]
        print("id: {}, symbol-set: {}, start: {}".format(child_id, child_symbolset, child_start))
        
        if child_start not "none":
            start_ste = anml.AddSTE()

        else:

        
    
    #anml.ExportAnml("example_output.anml")

    # anml = Anml()

    # stes = []

    # report_symbol = r"\x%02X" % 255

    # for i in range(10):
    #     if i == 0:
    #         start_ste = anml.AddSTE(report_symbol, AnmlDefs.ALL_INPUT,
    #                                 anmlId=i, match=False)
    #         stes.append(start_ste)
    #     else:
    #         character_class = r"\x%02X" % i
    #         ste = anml.AddSTE(character_class, AnmlDefs.NO_START,
    #                           anmlId=i, match=False)
    #         anml.AddAnmlEdge(stes[-1], ste, 0)
    #         stes.append(ste)

    # ste = anml.AddSTE(report_symbol, AnmlDefs.NO_START,
    #                   anmlId=10, reportCode=10)
    # anml.AddAnmlEdge(stes[-1], ste, 0)
