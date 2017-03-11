from __future__ import print_function
from tccMChecker.formula import Formula
from tccMChecker.model_checking_algorithm import model_satisfies_property

# Main
if __name__ == "__main__":
    # TCC Structure
    tcc_structure = {1: {"store": [Formula({"": "da=0"}),
                                   Formula({"~": "dd"}),
                                   Formula({"~": "tc"}),
                                   Formula({"~": "tt"}),
                                   Formula({"^": {"": "b=1", " ": "sm=0"}}),
                                   Formula({"v": {"~": "b=2", " ~": "sm=0"}}),
                                   Formula({"v": {"~": "b=3", " ~": "sm=0"}}),
                                   Formula({"v": {"~": "b=0", " ~": "sm=5"}}),
                                   Formula({"v": {"~": "b=0", " ~": "sm=10"}}),
                                   Formula({"v": {"~": "b=0", " ~": "sm=0"}})
                                   ],
                         "normal": [],
                         "temporal": ["p27"],
                         "edges": [1, 2, 3, 4, 5, 6],
                         "initial": True
                         },
                     2: {"store": [Formula({"": "da=0"}),
                                   Formula({"~": "dd"}),
                                   Formula({"~": "tc"}),
                                   Formula({"~": "tt"}),
                                   Formula({"v": {"~": "b=1", " ~": "sm=0"}}),
                                   Formula({"^": {"": "b=2", " ": "sm=0"}}),
                                   Formula({"v": {"~": "b=3", " ~": "sm=0"}}),
                                   Formula({"v": {"~": "b=0", " ~": "sm=5"}}),
                                   Formula({"v": {"~": "b=0", " ~": "sm=10"}}),
                                   Formula({"v": {"~": "b=0", " ~": "sm=0"}})
                                   ],
                         "normal": [],
                         "temporal": ["p31"],
                         "edges": [1, 2, 3, 4, 5, 6],
                         "initial": True
                         },
                     3: {"store": [Formula({"": "da=0"}),
                                   Formula({"~": "dd"}),
                                   Formula({"~": "tc"}),
                                   Formula({"~": "tt"}),
                                   Formula({"v": {"~": "b=1", " ~": "sm=0"}}),
                                   Formula({"v": {"~": "b=2", " ~": "sm=0"}}),
                                   Formula({"^": {"": "b=3", " ": "sm=0"}}),
                                   Formula({"v": {"~": "b=0", " ~": "sm=5"}}),
                                   Formula({"v": {"~": "b=0", " ~": "sm=10"}}),
                                   Formula({"v": {"~": "b=0", " ~": "sm=0"}})
                                   ],
                         "normal": [],
                         "temporal": ["p35"],
                         "edges": [1, 2, 3, 4, 5, 6],
                         "initial": True
                         },
                     4: {"store": [Formula({"": "da=0"}),
                                   Formula({"~": "dd"}),
                                   Formula({"~": "tc"}),
                                   Formula({"~": "tt"}),
                                   Formula({"v": {"~": "b=1", " ~": "sm=0"}}),
                                   Formula({"v": {"~": "b=2", " ~": "sm=0"}}),
                                   Formula({"v": {"~": "b=3", " ~": "sm=0"}}),
                                   Formula({"^": {"": "b=0", " ": "sm=5"}}),
                                   Formula({"v": {"~": "b=0", " ~": "sm=10"}}),
                                   Formula({"v": {"~": "b=0", " ~": "sm=0"}})
                                   ],
                         "normal": [],
                         "temporal": ["p39"],
                         "edges": [7, 8, 9, 10, 11, 12],
                         "initial": True
                         },
                     5: {"store": [Formula({"": "da=0"}),
                                   Formula({"~": "dd"}),
                                   Formula({"~": "tc"}),
                                   Formula({"~": "tt"}),
                                   Formula({"v": {"~": "b=1", " ~": "sm=0"}}),
                                   Formula({"v": {"~": "b=2", " ~": "sm=0"}}),
                                   Formula({"v": {"~": "b=3", " ~": "sm=0"}}),
                                   Formula({"v": {"~": "b=0", " ~": "sm=5"}}),
                                   Formula({"^": {"": "b=0", " ": "sm=10"}}),
                                   Formula({"v": {"~": "b=0", " ~": "sm=0"}})
                                   ],
                         "normal": [],
                         "temporal": ["p43"],
                         "edges": [13, 14, 15, 16, 17, 18],
                         "initial": True
                         },
                     6: {"store": [Formula({"": "da=0"}),
                                   Formula({"~": "dd"}),
                                   Formula({"~": "tc"}),
                                   Formula({"~": "tt"}),
                                   Formula({"v": {"~": "b=1", " ~": "sm=0"}}),
                                   Formula({"v": {"~": "b=2", " ~": "sm=0"}}),
                                   Formula({"v": {"~": "b=3", " ~": "sm=0"}}),
                                   Formula({"v": {"~": "b=0", " ~": "sm=5"}}),
                                   Formula({"v": {"~": "b=0", " ~": "sm=10"}}),
                                   Formula({"^": {"": "b=0", " ": "sm=0"}}),
                                   ],
                         "normal": [],
                         "temporal": ["p46"],
                         "edges": [1, 2, 3, 4, 5, 6],
                         "initial": True
                         },
                     7: {"store": [Formula({"": "da=5"}),
                                   Formula({"~": "dd"}),
                                   Formula({"~": "tc"}),
                                   Formula({"~": "tt"}),
                                   Formula({"^": {"": "b=1", " ": "sm=0"}}),
                                   Formula({"v": {"~": "b=2", " ~": "sm=0"}}),
                                   Formula({"v": {"~": "b=3", " ~": "sm=0"}}),
                                   Formula({"v": {"~": "b=0", " ~": "sm=5"}}),
                                   Formula({"v": {"~": "b=0", " ~": "sm=10"}}),
                                   Formula({"v": {"~": "b=0", " ~": "sm=0"}})
                                   ],
                         "normal": [],
                         "temporal": ["p53"],
                         "edges": [7, 8, 9, 10, 11, 12],
                         "initial": False
                         },
                     8: {"store": [Formula({"": "da=5"}),
                                   Formula({"~": "dd"}),
                                   Formula({"~": "tc"}),
                                   Formula({"~": "tt"}),
                                   Formula({"v": {"~": "b=1", " ~": "sm=0"}}),
                                   Formula({"^": {"": "b=2", " ": "sm=0"}}),
                                   Formula({"v": {"~": "b=3", " ~": "sm=0"}}),
                                   Formula({"v": {"~": "b=0", " ~": "sm=5"}}),
                                   Formula({"v": {"~": "b=0", " ~": "sm=10"}}),
                                   Formula({"v": {"~": "b=0", " ~": "sm=0"}})
                                   ],
                         "normal": [],
                         "temporal": ["tell58", "p59"],
                         "edges": [19],
                         "initial": False
                         },
                     9: {"store": [Formula({"": "da=5"}),
                                   Formula({"~": "dd"}),
                                   Formula({"~": "tc"}),
                                   Formula({"~": "tt"}),
                                   Formula({"v": {"~": "b=1", " ~": "sm=0"}}),
                                   Formula({"v": {"~": "b=2", " ~": "sm=0"}}),
                                   Formula({"^": {"": "b=3", " ": "sm=0"}}),
                                   Formula({"v": {"~": "b=0", " ~": "sm=5"}}),
                                   Formula({"v": {"~": "b=0", " ~": "sm=10"}}),
                                   Formula({"v": {"~": "b=0", " ~": "sm=0"}})
                                   ],
                         "normal": [],
                         "temporal": ["tell64", "p65"],
                         "edges": [20],
                         "initial": False
                         },
                     10: {"store": [Formula({"": "da=5"}),
                                    Formula({"~": "dd"}),
                                    Formula({"~": "tc"}),
                                    Formula({"~": "tt"}),
                                    Formula({"v": {"~": "b=1", " ~": "sm=0"}}),
                                    Formula({"v": {"~": "b=2", " ~": "sm=0"}}),
                                    Formula({"v": {"~": "b=3", " ~": "sm=0"}}),
                                    Formula({"^": {"": "b=0", " ": "sm=5"}}),
                                    Formula({"v": {"~": "b=0", " ~": "sm=10"}}),
                                    Formula({"v": {"~": "b=0", " ~": "sm=0"}})
                                    ],
                          "normal": [],
                          "temporal": ["p69"],
                          "edges": [13, 14, 15, 16, 17, 18],
                          "initial": False
                          },
                     11: {"store": [Formula({"": "da=5"}),
                                    Formula({"~": "dd"}),
                                    Formula({"~": "tc"}),
                                    Formula({"~": "tt"}),
                                    Formula({"v": {"~": "b=1", " ~": "sm=0"}}),
                                    Formula({"v": {"~": "b=2", " ~": "sm=0"}}),
                                    Formula({"v": {"~": "b=3", " ~": "sm=0"}}),
                                    Formula({"v": {"~": "b=0", " ~": "sm=5"}}),
                                    Formula({"^": {"": "b=0", " ": "sm=10"}}),
                                    Formula({"v": {"~": "b=0", " ~": "sm=0"}})
                                    ],
                          "normal": [],
                          "temporal": ["tell74", "p75"],
                          "edges": [21],
                          "initial": False
                          },
                     12: {"store": [Formula({"": "da=5"}),
                                    Formula({"~": "dd"}),
                                    Formula({"~": "tc"}),
                                    Formula({"~": "tt"}),
                                    Formula({"v": {"~": "b=1", " ~": "sm=0"}}),
                                    Formula({"v": {"~": "b=2", " ~": "sm=0"}}),
                                    Formula({"v": {"~": "b=3", " ~": "sm=0"}}),
                                    Formula({"v": {"~": "b=0", " ~": "sm=5"}}),
                                    Formula({"v": {"~": "b=0", " ~": "sm=10"}}),
                                    Formula({"^": {"": "b=0", " ": "sm=0"}})
                                    ],
                          "normal": [],
                          "temporal": ["p78"],
                          "edges": [7, 8, 9, 10, 11, 12],
                          "initial": False
                          },
                     13: {"store": [Formula({"": "da=10"}),
                                    Formula({"~": "dd"}),
                                    Formula({"~": "tc"}),
                                    Formula({"~": "tt"}),
                                    Formula({"^": {"": "b=1", " ": "sm=0"}}),
                                    Formula({"v": {"~": "b=2", " ~": "sm=0"}}),
                                    Formula({"v": {"~": "b=3", " ~": "sm=0"}}),
                                    Formula({"v": {"~": "b=0", " ~": "sm=5"}}),
                                    Formula({"v": {"~": "b=0", " ~": "sm=10"}}),
                                    Formula({"v": {"~": "b=0", " ~": "sm=0"}})
                                    ],
                          "normal": [],
                          "temporal": ["tell86", "p87"],
                          "edges": [22],
                          "initial": False
                          },
                     14: {"store": [Formula({"": "da=10"}),
                                    Formula({"~": "dd"}),
                                    Formula({"~": "tc"}),
                                    Formula({"~": "tt"}),
                                    Formula({"v": {"~": "b=1", " ~": "sm=0"}}),
                                    Formula({"^": {"": "b=2", " ": "sm=0"}}),
                                    Formula({"v": {"~": "b=3", " ~": "sm=0"}}),
                                    Formula({"v": {"~": "b=0", " ~": "sm=5"}}),
                                    Formula({"v": {"~": "b=0", " ~": "sm=10"}}),
                                    Formula({"v": {"~": "b=0", " ~": "sm=0"}})
                                    ],
                          "normal": [],
                          "temporal": ["tell92", "p93"],
                          "edges": [23],
                          "initial": False
                          },
                     15: {"store": [Formula({"": "da=10"}),
                                    Formula({"~": "dd"}),
                                    Formula({"~": "tc"}),
                                    Formula({"~": "tt"}),
                                    Formula({"v": {"~": "b=1", " ~": "sm=0"}}),
                                    Formula({"v": {"~": "b=2", " ~": "sm=0"}}),
                                    Formula({"^": {"": "b=3", " ": "sm=0"}}),
                                    Formula({"v": {"~": "b=0", " ~": "sm=5"}}),
                                    Formula({"v": {"~": "b=0", " ~": "sm=10"}}),
                                    Formula({"v": {"~": "b=0", " ~": "sm=0"}})
                                    ],
                          "normal": [],
                          "temporal": ["tell98", "p99"],
                          "edges": [24],
                          "initial": False
                          },
                     16: {"store": [Formula({"": "da=10"}),
                                    Formula({"~": "dd"}),
                                    Formula({"~": "tc"}),
                                    Formula({"~": "tt"}),
                                    Formula({"v": {"~": "b=1", " ~": "sm=0"}}),
                                    Formula({"v": {"~": "b=2", " ~": "sm=0"}}),
                                    Formula({"v": {"~": "b=3", " ~": "sm=0"}}),
                                    Formula({"^": {"": "b=0", " ": "sm=5"}}),
                                    Formula({"v": {"~": "b=0", " ~": "sm=10"}}),
                                    Formula({"v": {"~": "b=0", " ~": "sm=0"}})
                                    ],
                          "normal": [],
                          "temporal": ["tell104", "p105"],
                          "edges": [21],
                          "initial": False
                          },
                     17: {"store": [Formula({"": "da=10"}),
                                    Formula({"~": "dd"}),
                                    Formula({"~": "tc"}),
                                    Formula({"~": "tt"}),
                                    Formula({"v": {"~": "b=1", " ~": "sm=0"}}),
                                    Formula({"v": {"~": "b=2", " ~": "sm=0"}}),
                                    Formula({"v": {"~": "b=3", " ~": "sm=0"}}),
                                    Formula({"v": {"~": "b=0", " ~": "sm=5"}}),
                                    Formula({"^": {"": "b=0", " ": "sm=10"}}),
                                    Formula({"v": {"~": "b=0", " ~": "sm=0"}})
                                    ],
                          "normal": [],
                          "temporal": ["tell110", "p111"],
                          "edges": [25],
                          "initial": False
                          },
                     18: {"store": [Formula({"": "da=10"}),
                                    Formula({"~": "dd"}),
                                    Formula({"~": "tc"}),
                                    Formula({"~": "tt"}),
                                    Formula({"v": {"~": "b=1", " ~": "sm=0"}}),
                                    Formula({"v": {"~": "b=2", " ~": "sm=0"}}),
                                    Formula({"v": {"~": "b=3", " ~": "sm=0"}}),
                                    Formula({"v": {"~": "b=0", " ~": "sm=5"}}),
                                    Formula({"v": {"~": "b=0", " ~": "sm=10"}}),
                                    Formula({"^": {"": "b=0", " ": "sm=0"}})
                                    ],
                          "normal": [],
                          "temporal": ["p114"],
                          "edges": [13, 14, 15, 16, 17, 18],
                          "initial": False
                          },
                     19: {"store": [Formula({"": "da=0"}),
                                    Formula({"~": "dd"}),
                                    Formula({"~": "tc"}),
                                    Formula({"": "tt"}),
                                    Formula({"": "dc"})
                                    ],
                          "normal": [],
                          "temporal": ["p8"],
                          "edges": [1, 2, 3, 4, 5, 6],
                          "initial": False
                          },
                     20: {"store": [Formula({"": "da=5"}),
                                    Formula({"~": "tc"}),
                                    Formula({"~": "tt"}),
                                    Formula({"": "dd"})
                                    ],
                          "normal": [],
                          "temporal": ["p13"],
                          "edges": [1, 2, 3, 4, 5, 6],
                          "initial": False
                          },
                     21: {"store": [Formula({"": "da=15"}),
                                    Formula({"~": "tc"}),
                                    Formula({"~": "tt"}),
                                    Formula({"": "dd"})
                                    ],
                          "normal": [],
                          "temporal": ["p13"],
                          "edges": [1, 2, 3, 4, 5, 6],
                          "initial": False
                          },
                     22: {"store": [Formula({"": "da=0"}),
                                    Formula({"~": "dd"}),
                                    Formula({"": "tc"}),
                                    Formula({"~": "tt"}),
                                    Formula({"": "dc"})
                                    ],
                          "normal": [],
                          "temporal": ["p20"],
                          "edges": [1, 2, 3, 4, 5, 6],
                          "initial": False
                          },
                     23: {"store": [Formula({"": "da=5"}),
                                    Formula({"~": "dd"}),
                                    Formula({"~": "tc"}),
                                    Formula({"": "tt"}),
                                    Formula({"": "dc"})
                                    ],
                          "normal": [],
                          "temporal": ["p8"],
                          "edges": [1, 2, 3, 4, 5, 6],
                          "initial": False
                          },
                     24: {"store": [Formula({"": "da=10"}),
                                    Formula({"~": "tc"}),
                                    Formula({"~": "tt"}),
                                    Formula({"": "dd"})
                                    ],
                          "normal": [],
                          "temporal": ["p13"],
                          "edges": [1, 2, 3, 4, 5, 6],
                          "initial": False
                          },
                     25: {"store": [Formula({"": "da=20"}),
                                    Formula({"~": "tc"}),
                                    Formula({"~": "tt"}),
                                    Formula({"": "dd"})
                                    ],
                          "normal": [],
                          "temporal": ["p13"],
                          "edges": [1, 2, 3, 4, 5, 6],
                          "initial": False
                          }
                     }

    # Formula
    # phi = Formula({"<>":{"^":{"^":{"":"da=5", " ":"b=1"}, "~":{"o":"tc"}}}})
    # phi = Formula({"<>":{"^":{"^":{"":"da=10", " ":"b=1"}, "~":{"o":"tc"}}}})

    # phi = Formula({"[]":{"^":{"^":{"":"da=10", " ":"b=1"}, "~":{"o":"tc"}}}}) # (output True)

    # phi = Formula({"<>":{"^":{"": "dd", "~":{"o":"da=5"}}}}) # funciona (output False)
    # phi = Formula({"<>":{"^":{"": "dd", "~":{"o":"da=0"}}}}) # funciona (output True)

    # phi = Formula({"<>":{"^":{"": "tt", "~":{"o":"da=5"}}}}) # funciona (output False)
    phi = Formula({"<>": {"^": {"": "tt", "~": {"o": "da=0"}}}})

    print("Formula: ")
    print(phi.get_formula())

    # Report
    print("***************** REPORT *****************")
    result = model_satisfies_property(phi, tcc_structure)

    print("***************** RESULT: *****************")
    print("Model Satisfies Formula: ", not result)
