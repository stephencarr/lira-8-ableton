{
  "patcher": {
    "fileversion": 1,
    "appversion": {
      "major": 9,
      "minor": 0,
      "revision": 0,
      "architecture": "x64",
      "modernui": 1
    },
    "classnamespace": "box",
    "rect": [
      0,
      0,
      790,
      700
    ],
    "openinpresentation": 1,
    "devicewidth": 790,
    "bgcolor": [
      0.095,
      0.075,
      0.09,
      1
    ],
    "editing_bgcolor": [
      0.095,
      0.075,
      0.09,
      1
    ],
    "default_fontsize": 11,
    "default_fontname": "Arial",
    "boxes": [
      {
        "box": {
          "id": "brand",
          "maxclass": "comment",
          "patching_rect": [
            10,
            8,
            145,
            26
          ],
          "presentation": 1,
          "presentation_rect": [
            10,
            8,
            145,
            26
          ],
          "fontsize": 19,
          "textcolor": [
            0.64,
            0.73,
            0.69,
            1
          ],
          "fontname": "Arial",
          "text": "LIRA DELAY"
        }
      },
      {
        "box": {
          "id": "description",
          "maxclass": "comment",
          "patching_rect": [
            12,
            40,
            135,
            34
          ],
          "presentation": 1,
          "presentation_rect": [
            12,
            40,
            135,
            34
          ],
          "fontsize": 10,
          "textcolor": [
            0.95,
            0.92,
            0.94,
            1
          ],
          "fontname": "Arial",
          "text": "DUAL MOD DELAY\n+ DISTORTION"
        }
      },
      {
        "box": {
          "id": "routinghint",
          "maxclass": "comment",
          "patching_rect": [
            12,
            98,
            137,
            58
          ],
          "presentation": 1,
          "presentation_rect": [
            12,
            98,
            137,
            58
          ],
          "fontsize": 10,
          "textcolor": [
            0.95,
            0.92,
            0.94,
            1
          ],
          "fontname": "Arial",
          "text": "Insert or return\nReturn: Mix at 127\nStereo input \u2192 mono"
        }
      },
      {
        "box": {
          "id": "lfopanel",
          "maxclass": "panel",
          "patching_rect": [
            154,
            4,
            140,
            160
          ],
          "presentation": 1,
          "presentation_rect": [
            154,
            4,
            140,
            160
          ],
          "bgcolor": [
            0.16,
            0.13,
            0.155,
            1
          ],
          "rounded": 8,
          "border": 0,
          "background": 1,
          "ignoreclick": 1
        }
      },
      {
        "box": {
          "id": "lfopanellabel",
          "maxclass": "comment",
          "patching_rect": [
            162,
            9,
            124,
            18
          ],
          "presentation": 1,
          "presentation_rect": [
            162,
            9,
            124,
            18
          ],
          "fontsize": 11,
          "textcolor": [
            0.64,
            0.73,
            0.69,
            1
          ],
          "fontname": "Arial",
          "text": "HYPER LFO"
        }
      },
      {
        "box": {
          "id": "delaypanel",
          "maxclass": "panel",
          "patching_rect": [
            300,
            4,
            278,
            160
          ],
          "presentation": 1,
          "presentation_rect": [
            300,
            4,
            278,
            160
          ],
          "bgcolor": [
            0.16,
            0.13,
            0.155,
            1
          ],
          "rounded": 8,
          "border": 0,
          "background": 1,
          "ignoreclick": 1
        }
      },
      {
        "box": {
          "id": "delaypanellabel",
          "maxclass": "comment",
          "patching_rect": [
            308,
            9,
            262,
            18
          ],
          "presentation": 1,
          "presentation_rect": [
            308,
            9,
            262,
            18
          ],
          "fontsize": 11,
          "textcolor": [
            0.64,
            0.73,
            0.69,
            1
          ],
          "fontname": "Arial",
          "text": "MOD DELAY"
        }
      },
      {
        "box": {
          "id": "outpanel",
          "maxclass": "panel",
          "patching_rect": [
            584,
            4,
            200,
            160
          ],
          "presentation": 1,
          "presentation_rect": [
            584,
            4,
            200,
            160
          ],
          "bgcolor": [
            0.16,
            0.13,
            0.155,
            1
          ],
          "rounded": 8,
          "border": 0,
          "background": 1,
          "ignoreclick": 1
        }
      },
      {
        "box": {
          "id": "outpanellabel",
          "maxclass": "comment",
          "patching_rect": [
            592,
            9,
            184,
            18
          ],
          "presentation": 1,
          "presentation_rect": [
            592,
            9,
            184,
            18
          ],
          "fontsize": 11,
          "textcolor": [
            0.64,
            0.73,
            0.69,
            1
          ],
          "fontname": "Arial",
          "text": "INPUT / DISTORTION / OUT"
        }
      },
      {
        "box": {
          "id": "srclabel",
          "maxclass": "comment",
          "patching_rect": [
            503,
            30,
            70,
            16
          ],
          "presentation": 1,
          "presentation_rect": [
            503,
            30,
            70,
            16
          ],
          "fontsize": 8,
          "textcolor": [
            0.95,
            0.92,
            0.94,
            1
          ],
          "fontname": "Arial",
          "text": "MOD SOURCE"
        }
      },
      {
        "box": {
          "id": "wavelabel",
          "maxclass": "comment",
          "patching_rect": [
            503,
            90,
            70,
            16
          ],
          "presentation": 1,
          "presentation_rect": [
            503,
            90,
            70,
            16
          ],
          "fontsize": 8,
          "textcolor": [
            0.95,
            0.92,
            0.94,
            1
          ],
          "fontname": "Arial",
          "text": "LFO WAVE"
        }
      },
      {
        "box": {
          "id": "time1",
          "maxclass": "live.dial",
          "patching_rect": [
            308,
            31,
            58,
            55
          ],
          "presentation": 1,
          "presentation_rect": [
            308,
            31,
            58,
            55
          ],
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            "float"
          ],
          "parameter_enable": 1,
          "varname": "time1",
          "saved_attribute_attributes": {
            "valueof": {
              "parameter_longname": "Delay Time 1",
              "parameter_shortname": "Time 1",
              "parameter_type": 0,
              "parameter_mmin": 0,
              "parameter_mmax": 127,
              "parameter_initial_enable": 1,
              "parameter_initial": [
                60
              ],
              "parameter_unitstyle": 0
            }
          },
          "fontsize": 10,
          "appearance": 0,
          "showname": 1,
          "shownumber": 0,
          "activefgdialcolor": [
            0.64,
            0.73,
            0.69,
            1
          ],
          "activeneedlecolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "activebgcolor": [
            0.3,
            0.27,
            0.3,
            1
          ],
          "textcolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "activefgcolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "hint": "Delay Time 1 \u2014 0\u2013127, same scale as Pure Data"
        }
      },
      {
        "box": {
          "id": "send_time1",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            528,
            180,
            22
          ],
          "text": "prepend time1"
        }
      },
      {
        "box": {
          "id": "read_time1",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            552,
            180,
            22
          ],
          "text": "pattr @bindto time1 @autorestore 0"
        }
      },
      {
        "box": {
          "id": "time2",
          "maxclass": "live.dial",
          "patching_rect": [
            371,
            31,
            58,
            55
          ],
          "presentation": 1,
          "presentation_rect": [
            371,
            31,
            58,
            55
          ],
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            "float"
          ],
          "parameter_enable": 1,
          "varname": "time2",
          "saved_attribute_attributes": {
            "valueof": {
              "parameter_longname": "Delay Time 2",
              "parameter_shortname": "Time 2",
              "parameter_type": 0,
              "parameter_mmin": 0,
              "parameter_mmax": 127,
              "parameter_initial_enable": 1,
              "parameter_initial": [
                68
              ],
              "parameter_unitstyle": 0
            }
          },
          "fontsize": 10,
          "appearance": 0,
          "showname": 1,
          "shownumber": 0,
          "activefgdialcolor": [
            0.64,
            0.73,
            0.69,
            1
          ],
          "activeneedlecolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "activebgcolor": [
            0.3,
            0.27,
            0.3,
            1
          ],
          "textcolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "activefgcolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "hint": "Delay Time 2 \u2014 0\u2013127, same scale as Pure Data"
        }
      },
      {
        "box": {
          "id": "send_time2",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            600,
            180,
            22
          ],
          "text": "prepend time2"
        }
      },
      {
        "box": {
          "id": "read_time2",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            624,
            180,
            22
          ],
          "text": "pattr @bindto time2 @autorestore 0"
        }
      },
      {
        "box": {
          "id": "dmod1",
          "maxclass": "live.dial",
          "patching_rect": [
            308,
            96,
            58,
            55
          ],
          "presentation": 1,
          "presentation_rect": [
            308,
            96,
            58,
            55
          ],
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            "float"
          ],
          "parameter_enable": 1,
          "varname": "dmod1",
          "saved_attribute_attributes": {
            "valueof": {
              "parameter_longname": "Delay Mod 1",
              "parameter_shortname": "Mod 1",
              "parameter_type": 0,
              "parameter_mmin": 0,
              "parameter_mmax": 127,
              "parameter_initial_enable": 1,
              "parameter_initial": [
                0
              ],
              "parameter_unitstyle": 0
            }
          },
          "fontsize": 10,
          "appearance": 0,
          "showname": 1,
          "shownumber": 0,
          "activefgdialcolor": [
            0.64,
            0.73,
            0.69,
            1
          ],
          "activeneedlecolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "activebgcolor": [
            0.3,
            0.27,
            0.3,
            1
          ],
          "textcolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "activefgcolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "hint": "Delay Mod 1 \u2014 0\u2013127, same scale as Pure Data"
        }
      },
      {
        "box": {
          "id": "send_dmod1",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            672,
            180,
            22
          ],
          "text": "prepend dmod1"
        }
      },
      {
        "box": {
          "id": "read_dmod1",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            696,
            180,
            22
          ],
          "text": "pattr @bindto dmod1 @autorestore 0"
        }
      },
      {
        "box": {
          "id": "dmod2",
          "maxclass": "live.dial",
          "patching_rect": [
            371,
            96,
            58,
            55
          ],
          "presentation": 1,
          "presentation_rect": [
            371,
            96,
            58,
            55
          ],
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            "float"
          ],
          "parameter_enable": 1,
          "varname": "dmod2",
          "saved_attribute_attributes": {
            "valueof": {
              "parameter_longname": "Delay Mod 2",
              "parameter_shortname": "Mod 2",
              "parameter_type": 0,
              "parameter_mmin": 0,
              "parameter_mmax": 127,
              "parameter_initial_enable": 1,
              "parameter_initial": [
                0
              ],
              "parameter_unitstyle": 0
            }
          },
          "fontsize": 10,
          "appearance": 0,
          "showname": 1,
          "shownumber": 0,
          "activefgdialcolor": [
            0.64,
            0.73,
            0.69,
            1
          ],
          "activeneedlecolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "activebgcolor": [
            0.3,
            0.27,
            0.3,
            1
          ],
          "textcolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "activefgcolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "hint": "Delay Mod 2 \u2014 0\u2013127, same scale as Pure Data"
        }
      },
      {
        "box": {
          "id": "send_dmod2",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            744,
            180,
            22
          ],
          "text": "prepend dmod2"
        }
      },
      {
        "box": {
          "id": "read_dmod2",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            768,
            180,
            22
          ],
          "text": "pattr @bindto dmod2 @autorestore 0"
        }
      },
      {
        "box": {
          "id": "feedback",
          "maxclass": "live.dial",
          "patching_rect": [
            434,
            31,
            58,
            55
          ],
          "presentation": 1,
          "presentation_rect": [
            434,
            31,
            58,
            55
          ],
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            "float"
          ],
          "parameter_enable": 1,
          "varname": "feedback",
          "saved_attribute_attributes": {
            "valueof": {
              "parameter_longname": "Feedback",
              "parameter_shortname": "Feedback",
              "parameter_type": 0,
              "parameter_mmin": 0,
              "parameter_mmax": 127,
              "parameter_initial_enable": 1,
              "parameter_initial": [
                35
              ],
              "parameter_unitstyle": 0
            }
          },
          "fontsize": 10,
          "appearance": 0,
          "showname": 1,
          "shownumber": 0,
          "activefgdialcolor": [
            0.64,
            0.73,
            0.69,
            1
          ],
          "activeneedlecolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "activebgcolor": [
            0.3,
            0.27,
            0.3,
            1
          ],
          "textcolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "activefgcolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "hint": "Feedback \u2014 0\u2013127, same scale as Pure Data"
        }
      },
      {
        "box": {
          "id": "send_feedback",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            816,
            180,
            22
          ],
          "text": "prepend feedback"
        }
      },
      {
        "box": {
          "id": "read_feedback",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            840,
            180,
            22
          ],
          "text": "pattr @bindto feedback @autorestore 0"
        }
      },
      {
        "box": {
          "id": "dmix",
          "maxclass": "live.dial",
          "patching_rect": [
            434,
            96,
            58,
            55
          ],
          "presentation": 1,
          "presentation_rect": [
            434,
            96,
            58,
            55
          ],
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            "float"
          ],
          "parameter_enable": 1,
          "varname": "dmix",
          "saved_attribute_attributes": {
            "valueof": {
              "parameter_longname": "Delay Mix",
              "parameter_shortname": "Mix",
              "parameter_type": 0,
              "parameter_mmin": 0,
              "parameter_mmax": 127,
              "parameter_initial_enable": 1,
              "parameter_initial": [
                127
              ],
              "parameter_unitstyle": 0
            }
          },
          "fontsize": 10,
          "appearance": 0,
          "showname": 1,
          "shownumber": 0,
          "activefgdialcolor": [
            0.64,
            0.73,
            0.69,
            1
          ],
          "activeneedlecolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "activebgcolor": [
            0.3,
            0.27,
            0.3,
            1
          ],
          "textcolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "activefgcolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "hint": "Delay Mix: 0 dry, 127 wet. Use 127 on a return track."
        }
      },
      {
        "box": {
          "id": "send_dmix",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            888,
            180,
            22
          ],
          "text": "prepend dmix"
        }
      },
      {
        "box": {
          "id": "read_dmix",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            912,
            180,
            22
          ],
          "text": "pattr @bindto dmix @autorestore 0"
        }
      },
      {
        "box": {
          "id": "dsource",
          "maxclass": "live.menu",
          "patching_rect": [
            503,
            49,
            67,
            20
          ],
          "presentation": 1,
          "presentation_rect": [
            503,
            49,
            67,
            20
          ],
          "numinlets": 1,
          "numoutlets": 3,
          "outlettype": [
            "",
            "",
            "float"
          ],
          "parameter_enable": 1,
          "varname": "dsource",
          "saved_attribute_attributes": {
            "valueof": {
              "parameter_longname": "Delay Source",
              "parameter_shortname": "Delay Source",
              "parameter_type": 2,
              "parameter_mmin": 0,
              "parameter_mmax": 2,
              "parameter_initial_enable": 1,
              "parameter_initial": [
                1
              ],
              "parameter_unitstyle": 9,
              "parameter_enum": [
                "Self",
                "Off",
                "LFO"
              ]
            }
          },
          "fontsize": 10,
          "items": [
            "Self",
            "Off",
            "LFO"
          ],
          "activebgcolor": [
            0.19,
            0.165,
            0.19,
            1
          ],
          "activetextcolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "hint": "Delay Source \u2014 Select Delay Source"
        }
      },
      {
        "box": {
          "id": "send_dsource",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            960,
            180,
            22
          ],
          "text": "prepend dsource"
        }
      },
      {
        "box": {
          "id": "read_dsource",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            984,
            180,
            22
          ],
          "text": "pattr @bindto dsource @autorestore 0"
        }
      },
      {
        "box": {
          "id": "dwave",
          "maxclass": "live.menu",
          "patching_rect": [
            503,
            109,
            67,
            20
          ],
          "presentation": 1,
          "presentation_rect": [
            503,
            109,
            67,
            20
          ],
          "numinlets": 1,
          "numoutlets": 3,
          "outlettype": [
            "",
            "",
            "float"
          ],
          "parameter_enable": 1,
          "varname": "dwave",
          "saved_attribute_attributes": {
            "valueof": {
              "parameter_longname": "Delay Wave",
              "parameter_shortname": "Delay Wave",
              "parameter_type": 2,
              "parameter_mmin": 0,
              "parameter_mmax": 1,
              "parameter_initial_enable": 1,
              "parameter_initial": [
                0
              ],
              "parameter_unitstyle": 9,
              "parameter_enum": [
                "Triangle",
                "Square"
              ]
            }
          },
          "fontsize": 10,
          "items": [
            "Triangle",
            "Square"
          ],
          "activebgcolor": [
            0.19,
            0.165,
            0.19,
            1
          ],
          "activetextcolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "hint": "Delay Wave \u2014 Select Delay Wave"
        }
      },
      {
        "box": {
          "id": "send_dwave",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            1032,
            180,
            22
          ],
          "text": "prepend dwave"
        }
      },
      {
        "box": {
          "id": "read_dwave",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            1056,
            180,
            22
          ],
          "text": "pattr @bindto dwave @autorestore 0"
        }
      },
      {
        "box": {
          "id": "lfo1",
          "maxclass": "live.dial",
          "patching_rect": [
            164,
            32,
            56,
            55
          ],
          "presentation": 1,
          "presentation_rect": [
            164,
            32,
            56,
            55
          ],
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            "float"
          ],
          "parameter_enable": 1,
          "varname": "lfo1",
          "saved_attribute_attributes": {
            "valueof": {
              "parameter_longname": "LFO A",
              "parameter_shortname": "Rate A",
              "parameter_type": 0,
              "parameter_mmin": 0,
              "parameter_mmax": 127,
              "parameter_initial_enable": 1,
              "parameter_initial": [
                64
              ],
              "parameter_unitstyle": 0
            }
          },
          "fontsize": 10,
          "appearance": 0,
          "showname": 1,
          "shownumber": 0,
          "activefgdialcolor": [
            0.64,
            0.73,
            0.69,
            1
          ],
          "activeneedlecolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "activebgcolor": [
            0.3,
            0.27,
            0.3,
            1
          ],
          "textcolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "activefgcolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "hint": "LFO A \u2014 0\u2013127, same scale as Pure Data"
        }
      },
      {
        "box": {
          "id": "send_lfo1",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            1104,
            180,
            22
          ],
          "text": "prepend lfo1"
        }
      },
      {
        "box": {
          "id": "read_lfo1",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            1128,
            180,
            22
          ],
          "text": "pattr @bindto lfo1 @autorestore 0"
        }
      },
      {
        "box": {
          "id": "lfo2",
          "maxclass": "live.dial",
          "patching_rect": [
            228,
            32,
            56,
            55
          ],
          "presentation": 1,
          "presentation_rect": [
            228,
            32,
            56,
            55
          ],
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            "float"
          ],
          "parameter_enable": 1,
          "varname": "lfo2",
          "saved_attribute_attributes": {
            "valueof": {
              "parameter_longname": "LFO B",
              "parameter_shortname": "Rate B",
              "parameter_type": 0,
              "parameter_mmin": 0,
              "parameter_mmax": 127,
              "parameter_initial_enable": 1,
              "parameter_initial": [
                72
              ],
              "parameter_unitstyle": 0
            }
          },
          "fontsize": 10,
          "appearance": 0,
          "showname": 1,
          "shownumber": 0,
          "activefgdialcolor": [
            0.64,
            0.73,
            0.69,
            1
          ],
          "activeneedlecolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "activebgcolor": [
            0.3,
            0.27,
            0.3,
            1
          ],
          "textcolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "activefgcolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "hint": "LFO B \u2014 0\u2013127, same scale as Pure Data"
        }
      },
      {
        "box": {
          "id": "send_lfo2",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            1176,
            180,
            22
          ],
          "text": "prepend lfo2"
        }
      },
      {
        "box": {
          "id": "read_lfo2",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            1200,
            180,
            22
          ],
          "text": "pattr @bindto lfo2 @autorestore 0"
        }
      },
      {
        "box": {
          "id": "link",
          "maxclass": "live.text",
          "patching_rect": [
            170,
            118,
            108,
            22
          ],
          "presentation": 1,
          "presentation_rect": [
            170,
            118,
            108,
            22
          ],
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            ""
          ],
          "parameter_enable": 1,
          "varname": "link",
          "saved_attribute_attributes": {
            "valueof": {
              "parameter_longname": "LFO Link",
              "parameter_shortname": "LFO Link",
              "parameter_type": 1,
              "parameter_mmin": 0,
              "parameter_mmax": 1,
              "parameter_initial_enable": 1,
              "parameter_initial": [
                0
              ],
              "parameter_unitstyle": 0
            }
          },
          "fontsize": 10,
          "mode": 1,
          "text": "Link",
          "texton": "Link",
          "activebgcolor": [
            0.29,
            0.26,
            0.29,
            1
          ],
          "activebgoncolor": [
            0.973,
            0.643,
            0.769,
            1
          ],
          "activetextcolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "activetextoncolor": [
            0.08,
            0.065,
            0.08,
            1
          ],
          "bgcolor": [
            0.29,
            0.26,
            0.29,
            1
          ],
          "bgoncolor": [
            0.973,
            0.643,
            0.769,
            1
          ],
          "textcolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "textoncolor": [
            0.08,
            0.065,
            0.08,
            1
          ],
          "hint": "LFO Link \u2014 Select LFO Link"
        }
      },
      {
        "box": {
          "id": "send_link",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            1248,
            180,
            22
          ],
          "text": "prepend link"
        }
      },
      {
        "box": {
          "id": "read_link",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            1272,
            180,
            22
          ],
          "text": "pattr @bindto link @autorestore 0"
        }
      },
      {
        "box": {
          "id": "drive",
          "maxclass": "live.dial",
          "patching_rect": [
            602,
            96,
            74,
            55
          ],
          "presentation": 1,
          "presentation_rect": [
            602,
            96,
            74,
            55
          ],
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            "float"
          ],
          "parameter_enable": 1,
          "varname": "drive",
          "saved_attribute_attributes": {
            "valueof": {
              "parameter_longname": "Drive",
              "parameter_shortname": "Drive",
              "parameter_type": 0,
              "parameter_mmin": 0,
              "parameter_mmax": 127,
              "parameter_initial_enable": 1,
              "parameter_initial": [
                20
              ],
              "parameter_unitstyle": 0
            }
          },
          "fontsize": 10,
          "appearance": 0,
          "showname": 1,
          "shownumber": 0,
          "activefgdialcolor": [
            0.64,
            0.73,
            0.69,
            1
          ],
          "activeneedlecolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "activebgcolor": [
            0.3,
            0.27,
            0.3,
            1
          ],
          "textcolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "activefgcolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "hint": "Drive \u2014 0\u2013127, same scale as Pure Data"
        }
      },
      {
        "box": {
          "id": "send_drive",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            1320,
            180,
            22
          ],
          "text": "prepend drive"
        }
      },
      {
        "box": {
          "id": "read_drive",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            1344,
            180,
            22
          ],
          "text": "pattr @bindto drive @autorestore 0"
        }
      },
      {
        "box": {
          "id": "distmix",
          "maxclass": "live.dial",
          "patching_rect": [
            692,
            96,
            74,
            55
          ],
          "presentation": 1,
          "presentation_rect": [
            692,
            96,
            74,
            55
          ],
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            "float"
          ],
          "parameter_enable": 1,
          "varname": "distmix",
          "saved_attribute_attributes": {
            "valueof": {
              "parameter_longname": "Dist Mix",
              "parameter_shortname": "Mix",
              "parameter_type": 0,
              "parameter_mmin": 0,
              "parameter_mmax": 127,
              "parameter_initial_enable": 1,
              "parameter_initial": [
                30
              ],
              "parameter_unitstyle": 0
            }
          },
          "fontsize": 10,
          "appearance": 0,
          "showname": 1,
          "shownumber": 0,
          "activefgdialcolor": [
            0.64,
            0.73,
            0.69,
            1
          ],
          "activeneedlecolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "activebgcolor": [
            0.3,
            0.27,
            0.3,
            1
          ],
          "textcolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "activefgcolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "hint": "Dist Mix \u2014 0\u2013127, same scale as Pure Data"
        }
      },
      {
        "box": {
          "id": "send_distmix",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            1392,
            180,
            22
          ],
          "text": "prepend distmix"
        }
      },
      {
        "box": {
          "id": "read_distmix",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            1416,
            180,
            22
          ],
          "text": "pattr @bindto distmix @autorestore 0"
        }
      },
      {
        "box": {
          "id": "volume",
          "maxclass": "live.dial",
          "patching_rect": [
            692,
            31,
            74,
            55
          ],
          "presentation": 1,
          "presentation_rect": [
            692,
            31,
            74,
            55
          ],
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            "float"
          ],
          "parameter_enable": 1,
          "varname": "volume",
          "saved_attribute_attributes": {
            "valueof": {
              "parameter_longname": "Master",
              "parameter_shortname": "Master",
              "parameter_type": 0,
              "parameter_mmin": 0,
              "parameter_mmax": 127,
              "parameter_initial_enable": 1,
              "parameter_initial": [
                80
              ],
              "parameter_unitstyle": 0
            }
          },
          "fontsize": 10,
          "appearance": 0,
          "showname": 1,
          "shownumber": 0,
          "activefgdialcolor": [
            0.64,
            0.73,
            0.69,
            1
          ],
          "activeneedlecolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "activebgcolor": [
            0.3,
            0.27,
            0.3,
            1
          ],
          "textcolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "activefgcolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "hint": "Master \u2014 0\u2013127, same scale as Pure Data"
        }
      },
      {
        "box": {
          "id": "send_volume",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            1464,
            180,
            22
          ],
          "text": "prepend volume"
        }
      },
      {
        "box": {
          "id": "read_volume",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            1488,
            180,
            22
          ],
          "text": "pattr @bindto volume @autorestore 0"
        }
      },
      {
        "box": {
          "id": "inputgain",
          "maxclass": "live.dial",
          "patching_rect": [
            602,
            31,
            74,
            55
          ],
          "presentation": 1,
          "presentation_rect": [
            602,
            31,
            74,
            55
          ],
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            "float"
          ],
          "parameter_enable": 1,
          "varname": "inputgain",
          "saved_attribute_attributes": {
            "valueof": {
              "parameter_longname": "Input",
              "parameter_shortname": "Input",
              "parameter_type": 0,
              "parameter_mmin": 0,
              "parameter_mmax": 127,
              "parameter_initial_enable": 1,
              "parameter_initial": [
                127
              ],
              "parameter_unitstyle": 0
            }
          },
          "fontsize": 10,
          "appearance": 0,
          "showname": 1,
          "shownumber": 0,
          "activefgdialcolor": [
            0.64,
            0.73,
            0.69,
            1
          ],
          "activeneedlecolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "activebgcolor": [
            0.3,
            0.27,
            0.3,
            1
          ],
          "textcolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "activefgcolor": [
            0.96,
            0.93,
            0.94,
            1
          ],
          "hint": "Input gain. 127 = unity; 0 stops new audio entering the delay."
        }
      },
      {
        "box": {
          "id": "send_inputgain",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            1536,
            180,
            22
          ],
          "text": "prepend inputgain"
        }
      },
      {
        "box": {
          "id": "read_inputgain",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            1560,
            180,
            22
          ],
          "text": "pattr @bindto inputgain @autorestore 0"
        }
      },
      {
        "box": {
          "id": "engine",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            1584,
            180,
            22
          ],
          "patcher": {
            "fileversion": 1,
            "classnamespace": "dsp.gen",
            "rect": [
              0,
              0,
              900,
              650
            ],
            "boxes": [
              {
                "box": {
                  "id": "code",
                  "maxclass": "codebox",
                  "code": "\n// Adapted from LIRA-8, Copyright Miguel Moreno. See License.txt.\n// Gen port: explicit 64-sample inter-pair feedback; see port notes.\nlira_sat(x) { z=clamp(x,-3,3); return z*(27+z*z)/(27+9*z*z); }\nlira_ramp(x,ms) {\n History previous(0);\n History value(0);\n History remaining(0);\n History increment(0);\n if (x != previous) {\n   remaining = max(1, ms * samplerate / 1000);\n   increment = (x - value) / remaining;\n }\n previous = x;\n if (remaining > 0) {\n   value = value + increment;\n   remaining = max(0, remaining - 1);\n } else {\n   value = x;\n }\n return value;\n}\n\nlira_lp(x,f) { History y(0); a=clamp(6.28318530718*f/samplerate,0,1); y=y+a*(x-y); return y; }\nlira_hp(x,f) {\n History input_memory(0);\n History output_memory(0);\n coefficient = clamp(1 - 6.28318530718 * f / samplerate, 0, 1);\n result = (1 + coefficient) * 0.5 * (x - input_memory) + coefficient * output_memory;\n input_memory = x;\n output_memory = result;\n return result;\n}\n\nlira_blep(p,d) { a=p/max(d,0.00000001); b=(p-1)/max(d,0.00000001); return p<d ? 2*a-a*a-1 : p>1-d ? b*b+2*b+1 : 0; }\nlira_osc(freq,duty) {\n History phase(0), width(0.53125), last(0), filt(0);\n f=abs(freq); dt=f/samplerate; p=phase; phase=wrap(p+dt,0,1);\n if(p<last){width=clamp(duty,0,1);} last=p;\n q=wrap(p+width,0,1);\n square=(2*p-1-lira_blep(p,dt))-(2*q-1-lira_blep(q,dt))+2*width-1;\n a=exp(-6.28318530718*clamp(max(f/4,100),0,samplerate/2)/samplerate);\n filt=(1-a)*square+a*filt;\n return square*0.59, filt*2.65-0.145;\n}\nlira_voice(arg_freq,arg_sharp,arg_gate,arg_hold,arg_fast,arg_duty) {\n envelope_value=lira_ramp(arg_gate,arg_gate>0 ? (arg_fast>0?100:200) : (arg_fast>0?100:8000));\n sq,tr=lira_osc(arg_freq,arg_duty);\n return (sq*arg_sharp+tr*(1-arg_sharp)+sin(envelope_value*6.28318530718)*0.5)*min(1,envelope_value*envelope_value+arg_hold);\n}\nlira_dynamics(x) {\n History env(0), sumsq(0);\n Delay rmsbuf(512);\n a=exp(-4.60517/(samplerate*0.0025)); env=abs(x)+a*(env-abs(x));\n gain=clamp(((env-0.2511886432)/5+0.2511886432)/max(env,0.0000000001),0,1);\n comp=x*lira_sat(gain);\n sq=comp*comp; old=rmsbuf.read(512); rmsbuf.write(sq);\n sumsq=max(0,sumsq+sq-old);\n db=10*log10(max(sumsq/512,0.000000000001));\n // 512-sample rectangular RMS approximation to Pd env~ Hann detector.\n eg=lira_ramp(pow(10,min(0,(db+60)*0.8)/20),11);\n return comp*eg;\n}\nHistory hpf_0_x(0), hpf_0_y(0);\nHistory hpf_1_x(0), hpf_1_y(0);\nHistory hpf_2_x(0), hpf_2_y(0);\nHistory hpf_3_x(0), hpf_3_y(0);\nHistory hpf_4_x(0), hpf_4_y(0);\nHistory hpf_5_x(0), hpf_5_y(0);\nHistory hpf_6_x(0), hpf_6_y(0);\nHistory hpf_7_x(0), hpf_7_y(0);\nHistory hpf_8_x(0), hpf_8_y(0);\nParam time1(60,min=0,max=127);\nParam time2(68,min=0,max=127);\nParam dmod1(0,min=0,max=127);\nParam dmod2(0,min=0,max=127);\nParam feedback(35,min=0,max=127);\nParam dmix(127,min=0,max=127);\nParam dsource(1,min=0,max=2);\nParam dwave(0,min=0,max=1);\nParam lfo1(64,min=0,max=127);\nParam lfo2(72,min=0,max=127);\nParam link(0,min=0,max=1);\nParam drive(20,min=0,max=127);\nParam distmix(30,min=0,max=127);\nParam volume(80,min=0,max=127);\nParam inputgain(127,min=0,max=127);\nDelay delay1(1048576),delay2(1048576);\nHistory lphase1(0),lphase2(0);\nfla=lira_ramp(mtof(pow(lfo1/127,2)*127-75),23.22);\nflb=lira_ramp(mtof(pow(lfo2/127,2)*127-75),23.22);\nls1=clamp(cos(lphase1*6.28318530718)*1000,-1,1);\nls2=clamp(cos(lphase2*6.28318530718)*1000,-1,1);\nltri=((abs(lphase1-0.5)*4-1)+(abs(lphase2-0.5)*4-1))*0.5;\nlsqr=(ls1+ls2)*0.5;\nlphase1=wrap(lphase1+fla/samplerate,0,1);\nlphase2=wrap(lphase2+(flb+ls1*flb*0.5*link)/samplerate,0,1);\ndry=(in1+in2)*0.5*lira_ramp(inputgain/127,23.22);\nfb=lira_ramp(feedback/127*pow(2,2*feedback/127),23.22);\ndlfo=(dwave>0?lsqr:ltri)*(dsource==2);\nself1=lira_lp(delay1.read(64)*0.5*(dsource==0),689);\nself2=lira_lp(delay2.read(64)*0.5,689)*(dsource==0);\nms1=lira_ramp(pow(2,time1/127*12)*1.45125,23.22)+(self1+dlfo)*lira_ramp(pow(dmod1/127,2)*10,23.22);\nms2=lira_ramp(pow(2,time2/127*12)*1.45125,23.22)+(self2+dlfo)*lira_ramp(pow(dmod2/127,2)*10,23.22);\nhpf_4_a = clamp(1 - 6.28318530718 * (1) / samplerate, 0, 1); hpf_4_input = delay1.read(clamp(ms1*samplerate/1000,64,1048575),interp=\"cubic\"); hpf_4_out = (1+hpf_4_a)*0.5*(hpf_4_input-hpf_4_x)+hpf_4_a*hpf_4_y; hpf_4_x=hpf_4_input; hpf_4_y=hpf_4_out;\nd1=lira_dynamics(lira_lp(hpf_4_out,4000));\nhpf_5_a = clamp(1 - 6.28318530718 * (1) / samplerate, 0, 1); hpf_5_input = delay2.read(clamp(ms2*samplerate/1000,64,1048575),interp=\"cubic\"); hpf_5_out = (1+hpf_5_a)*0.5*(hpf_5_input-hpf_5_x)+hpf_5_a*hpf_5_y; hpf_5_x=hpf_5_input; hpf_5_y=hpf_5_out;\nd2=lira_dynamics(lira_lp(hpf_5_out,4000));\nn=noise()*0.001;\ndelay1.write(dry+n+d1*fb);delay2.write(dry+n+d2*fb);\nwet=lira_sat((d1+d2)*0.5/max(fb,1.5));\ndm=lira_ramp(dmix/127,23.22); mixed=dry*(1-dm)+wet*dm;\ndg=lira_ramp(pow(10,(pow(3,1+2*drive/127)+3)/20),23.22);\nhpf_6_a = clamp(1 - 6.28318530718 * (20) / samplerate, 0, 1); hpf_6_input = mixed*dg; hpf_6_out = (1+hpf_6_a)*0.5*(hpf_6_input-hpf_6_x)+hpf_6_a*hpf_6_y; hpf_6_x=hpf_6_input; hpf_6_y=hpf_6_out;\ndist=lira_sat(hpf_6_out);\nhpf_7_a = clamp(1 - 6.28318530718 * (10) / samplerate, 0, 1); hpf_7_input = dist+pow(dist,31)*0.25; hpf_7_out = (1+hpf_7_a)*0.5*(hpf_7_input-hpf_7_x)+hpf_7_a*hpf_7_y; hpf_7_x=hpf_7_input; hpf_7_y=hpf_7_out;\ndist=hpf_7_out/clamp(dg,1,4)+mixed*0.1;\nmixd=lira_ramp(distmix/127,23.22);\nmaster=lira_sat(mixed*(1-mixd)+dist*mixd);\nout1=master*lira_ramp(pow(volume/127,2),23.22);\nout2=out1;\n",
                  "numinlets": 2,
                  "numoutlets": 2,
                  "patching_rect": [
                    20,
                    20,
                    850,
                    600
                  ]
                }
              },
              {
                "box": {
                  "id": "out1",
                  "maxclass": "newobj",
                  "text": "out 1",
                  "patching_rect": [
                    100,
                    640,
                    50,
                    22
                  ]
                }
              },
              {
                "box": {
                  "id": "out2",
                  "maxclass": "newobj",
                  "text": "out 2",
                  "patching_rect": [
                    200,
                    640,
                    50,
                    22
                  ]
                }
              },
              {
                "box": {
                  "id": "in1",
                  "maxclass": "newobj",
                  "text": "in 1",
                  "patching_rect": [
                    100,
                    0,
                    50,
                    22
                  ],
                  "numinlets": 0,
                  "numoutlets": 1
                }
              },
              {
                "box": {
                  "id": "in2",
                  "maxclass": "newobj",
                  "text": "in 2",
                  "patching_rect": [
                    200,
                    0,
                    50,
                    22
                  ],
                  "numinlets": 0,
                  "numoutlets": 1
                }
              }
            ],
            "lines": [
              {
                "patchline": {
                  "source": [
                    "code",
                    0
                  ],
                  "destination": [
                    "out1",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "code",
                    1
                  ],
                  "destination": [
                    "out2",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "in1",
                    0
                  ],
                  "destination": [
                    "code",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "in2",
                    0
                  ],
                  "destination": [
                    "code",
                    1
                  ]
                }
              }
            ]
          },
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "signal",
            "signal"
          ],
          "text": "gen~"
        }
      },
      {
        "box": {
          "id": "input",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            1608,
            180,
            22
          ],
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "signal",
            "signal"
          ],
          "text": "plugin~"
        }
      },
      {
        "box": {
          "id": "output",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            1632,
            180,
            22
          ],
          "numinlets": 2,
          "numoutlets": 0,
          "text": "plugout~"
        }
      },
      {
        "box": {
          "id": "boot",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            1656,
            180,
            22
          ],
          "text": "live.thisdevice"
        }
      },
      {
        "box": {
          "id": "defer",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            1680,
            180,
            22
          ],
          "text": "deferlow"
        }
      },
      {
        "box": {
          "id": "banks",
          "maxclass": "newobj",
          "patching_rect": [
            20,
            1704,
            180,
            22
          ],
          "text": "live.banks"
        }
      }
    ],
    "lines": [
      {
        "patchline": {
          "source": [
            "time1",
            0
          ],
          "destination": [
            "send_time1",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "send_time1",
            0
          ],
          "destination": [
            "engine",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "defer",
            0
          ],
          "destination": [
            "read_time1",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "read_time1",
            0
          ],
          "destination": [
            "send_time1",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "time2",
            0
          ],
          "destination": [
            "send_time2",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "send_time2",
            0
          ],
          "destination": [
            "engine",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "defer",
            0
          ],
          "destination": [
            "read_time2",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "read_time2",
            0
          ],
          "destination": [
            "send_time2",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "dmod1",
            0
          ],
          "destination": [
            "send_dmod1",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "send_dmod1",
            0
          ],
          "destination": [
            "engine",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "defer",
            0
          ],
          "destination": [
            "read_dmod1",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "read_dmod1",
            0
          ],
          "destination": [
            "send_dmod1",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "dmod2",
            0
          ],
          "destination": [
            "send_dmod2",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "send_dmod2",
            0
          ],
          "destination": [
            "engine",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "defer",
            0
          ],
          "destination": [
            "read_dmod2",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "read_dmod2",
            0
          ],
          "destination": [
            "send_dmod2",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "feedback",
            0
          ],
          "destination": [
            "send_feedback",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "send_feedback",
            0
          ],
          "destination": [
            "engine",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "defer",
            0
          ],
          "destination": [
            "read_feedback",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "read_feedback",
            0
          ],
          "destination": [
            "send_feedback",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "dmix",
            0
          ],
          "destination": [
            "send_dmix",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "send_dmix",
            0
          ],
          "destination": [
            "engine",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "defer",
            0
          ],
          "destination": [
            "read_dmix",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "read_dmix",
            0
          ],
          "destination": [
            "send_dmix",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "dsource",
            0
          ],
          "destination": [
            "send_dsource",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "send_dsource",
            0
          ],
          "destination": [
            "engine",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "defer",
            0
          ],
          "destination": [
            "read_dsource",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "read_dsource",
            0
          ],
          "destination": [
            "send_dsource",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "dwave",
            0
          ],
          "destination": [
            "send_dwave",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "send_dwave",
            0
          ],
          "destination": [
            "engine",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "defer",
            0
          ],
          "destination": [
            "read_dwave",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "read_dwave",
            0
          ],
          "destination": [
            "send_dwave",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "lfo1",
            0
          ],
          "destination": [
            "send_lfo1",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "send_lfo1",
            0
          ],
          "destination": [
            "engine",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "defer",
            0
          ],
          "destination": [
            "read_lfo1",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "read_lfo1",
            0
          ],
          "destination": [
            "send_lfo1",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "lfo2",
            0
          ],
          "destination": [
            "send_lfo2",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "send_lfo2",
            0
          ],
          "destination": [
            "engine",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "defer",
            0
          ],
          "destination": [
            "read_lfo2",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "read_lfo2",
            0
          ],
          "destination": [
            "send_lfo2",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "link",
            0
          ],
          "destination": [
            "send_link",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "send_link",
            0
          ],
          "destination": [
            "engine",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "defer",
            0
          ],
          "destination": [
            "read_link",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "read_link",
            0
          ],
          "destination": [
            "send_link",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "drive",
            0
          ],
          "destination": [
            "send_drive",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "send_drive",
            0
          ],
          "destination": [
            "engine",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "defer",
            0
          ],
          "destination": [
            "read_drive",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "read_drive",
            0
          ],
          "destination": [
            "send_drive",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "distmix",
            0
          ],
          "destination": [
            "send_distmix",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "send_distmix",
            0
          ],
          "destination": [
            "engine",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "defer",
            0
          ],
          "destination": [
            "read_distmix",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "read_distmix",
            0
          ],
          "destination": [
            "send_distmix",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "volume",
            0
          ],
          "destination": [
            "send_volume",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "send_volume",
            0
          ],
          "destination": [
            "engine",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "defer",
            0
          ],
          "destination": [
            "read_volume",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "read_volume",
            0
          ],
          "destination": [
            "send_volume",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "inputgain",
            0
          ],
          "destination": [
            "send_inputgain",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "send_inputgain",
            0
          ],
          "destination": [
            "engine",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "defer",
            0
          ],
          "destination": [
            "read_inputgain",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "read_inputgain",
            0
          ],
          "destination": [
            "send_inputgain",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "input",
            0
          ],
          "destination": [
            "engine",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "engine",
            0
          ],
          "destination": [
            "output",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "input",
            1
          ],
          "destination": [
            "engine",
            1
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "engine",
            1
          ],
          "destination": [
            "output",
            1
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "boot",
            0
          ],
          "destination": [
            "defer",
            0
          ]
        }
      }
    ],
    "parameters": {
      "time1": [
        "Delay Time 1",
        "Time 1",
        0
      ],
      "time2": [
        "Delay Time 2",
        "Time 2",
        0
      ],
      "dmod1": [
        "Delay Mod 1",
        "Mod 1",
        0
      ],
      "dmod2": [
        "Delay Mod 2",
        "Mod 2",
        0
      ],
      "feedback": [
        "Feedback",
        "Feedback",
        0
      ],
      "dmix": [
        "Delay Mix",
        "Mix",
        0
      ],
      "dsource": [
        "Delay Source",
        "Delay Source",
        0
      ],
      "dwave": [
        "Delay Wave",
        "Delay Wave",
        0
      ],
      "lfo1": [
        "LFO A",
        "Rate A",
        0
      ],
      "lfo2": [
        "LFO B",
        "Rate B",
        0
      ],
      "link": [
        "LFO Link",
        "LFO Link",
        0
      ],
      "drive": [
        "Drive",
        "Drive",
        0
      ],
      "distmix": [
        "Dist Mix",
        "Mix",
        0
      ],
      "volume": [
        "Master",
        "Master",
        0
      ],
      "inputgain": [
        "Input",
        "Input",
        0
      ],
      "parameterbanks": {
        "0": {
          "index": 0,
          "name": "Delay",
          "parameters": [
            "Delay Time 1",
            "Delay Time 2",
            "Delay Mod 1",
            "Delay Mod 2",
            "Feedback",
            "Delay Mix",
            "Delay Source",
            "Delay Wave"
          ]
        },
        "1": {
          "index": 1,
          "name": "Hyper LFO",
          "parameters": [
            "LFO A",
            "LFO B",
            "LFO Link",
            "Delay Source",
            "Delay Wave",
            "Delay Mod 1",
            "Delay Mod 2",
            "Feedback"
          ]
        },
        "2": {
          "index": 2,
          "name": "Output",
          "parameters": [
            "Input",
            "Drive",
            "Dist Mix",
            "Master",
            "Delay Mix",
            "Feedback",
            "Delay Time 1",
            "Delay Time 2"
          ]
        }
      },
      "inherited_shortname": 1
    },
    "dependency_cache": []
  }
}