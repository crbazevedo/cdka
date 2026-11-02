// Generated from exact Fraction certificates; do not hand-edit.
export const DATA = {
  "revision": "v9",
  "base_commit": "b0176b3d6fbdded67caad1cbe5cb4ae4521a5d1a",
  "contract": "v6 Contract; k=0,b=4; hidden health; physical syndrome/resources after each step",
  "scope": "K is diagnostic-code states, not all controller memory; two-epoch exact library",
  "tables": {
    "1": {
      "enumerated": 4,
      "plans": [
        {
          "id": 0,
          "first": "hold",
          "second": [],
          "alpha": [
            0.894557536,
            0.872081216
          ],
          "exact_alpha": [
            "27954923/31250000",
            "13626269/15625000"
          ]
        },
        {
          "id": 2,
          "first": "refresh",
          "second": [],
          "alpha": [
            0.945778666584,
            0.6594959384
          ],
          "exact_alpha": [
            "118222333323/125000000000",
            "824369923/1250000000"
          ]
        }
      ],
      "intervals": [
        {
          "lo": 0.0,
          "hi": 0.8058381866589297,
          "id": 0,
          "exact_lo": "0",
          "exact_hi": "26573159700/32975801023"
        },
        {
          "lo": 0.8058381866589297,
          "hi": 1.0,
          "id": 2,
          "exact_lo": "26573159700/32975801023",
          "exact_hi": "1"
        }
      ]
    },
    "2": {
      "enumerated": 64,
      "plans": [
        {
          "id": 50,
          "first": "service",
          "second": [
            [
              [
                0,
                3
              ],
              "hold"
            ],
            [
              [
                1,
                3
              ],
              "refresh"
            ]
          ],
          "alpha": [
            0.8025448039856933,
            0.7761289343364671
          ],
          "exact_alpha": [
            "1253976256227645703901/1562500000000000000000",
            "3789692062189781061/4882812500000000000"
          ]
        },
        {
          "id": 58,
          "first": "service",
          "second": [
            [
              [
                0,
                3
              ],
              "refresh"
            ],
            [
              [
                1,
                3
              ],
              "refresh"
            ]
          ],
          "alpha": [
            0.8434924698615122,
            0.7748634516785332
          ],
          "exact_alpha": [
            "329489246039653206671/390625000000000000000",
            "945878236912272031/1220703125000000000"
          ]
        },
        {
          "id": 42,
          "first": "refresh",
          "second": [
            [
              [
                0,
                3
              ],
              "refresh"
            ],
            [
              [
                1,
                3
              ],
              "refresh"
            ]
          ],
          "alpha": [
            0.8809592813190144,
            0.4349348927660966
          ],
          "exact_alpha": [
            "275299775412191992637151/312500000000000000000000",
            "679585769947025929/1562500000000000000"
          ]
        }
      ],
      "intervals": [
        {
          "lo": 0.0,
          "hi": 0.029978400140469416,
          "id": 50,
          "exact_lo": "0",
          "exact_hi": "3734866303040/124585244227163"
        },
        {
          "lo": 0.029978400140469416,
          "hi": 0.9007226521597878,
          "id": 58,
          "exact_lo": "3734866303040/124585244227163",
          "exact_hi": "106227674660136454136000/117936053240605881436351"
        },
        {
          "lo": 0.9007226521597878,
          "hi": 1.0,
          "id": 42,
          "exact_lo": "106227674660136454136000/117936053240605881436351",
          "exact_hi": "1"
        }
      ]
    }
  },
  "default": [
    {
      "capacity": 1,
      "value": 0.8091779607700227,
      "exact_value": "632170281851580256591/781250000000000000000",
      "loss": 0.011512069642133055,
      "exact_loss": "1079256528949973872874149/93750000000000000000000000",
      "encoding": [
        0,
        0,
        0
      ],
      "selected_plans": {
        "0": 58
      },
      "root_loss": 0.011230952584600926,
      "tail_loss": 0.00028111705753212826
    },
    {
      "capacity": 2,
      "value": 0.8204089133546236,
      "exact_value": "76913335626995967639518749/93750000000000000000000000",
      "loss": 0.00028111705753212826,
      "exact_loss": "43924540239395040459/156250000000000000000000",
      "encoding": [
        0,
        0,
        1
      ],
      "selected_plans": {
        "0": 58,
        "1": 42
      },
      "root_loss": 0.0,
      "tail_loss": 0.00028111705753212826
    },
    {
      "capacity": 3,
      "value": 0.8206900304121558,
      "exact_value": "76939690351139604663794149/93750000000000000000000000",
      "loss": 0.0,
      "exact_loss": "0",
      "encoding": [
        0,
        1,
        2
      ],
      "selected_plans": {
        "0": 50,
        "1": 58,
        "2": 42
      },
      "root_loss": 0.0,
      "tail_loss": 0.0
    }
  ],
  "cardinality": [
    {
      "tail": 0.0,
      "one_epoch": 2,
      "two_epochs": 3
    },
    {
      "tail": 0.01,
      "one_epoch": 2,
      "two_epochs": 3
    },
    {
      "tail": 0.03,
      "one_epoch": 2,
      "two_epochs": 2
    },
    {
      "tail": 0.1,
      "one_epoch": 2,
      "two_epochs": 1
    },
    {
      "tail": 0.15,
      "one_epoch": 2,
      "two_epochs": 1
    },
    {
      "tail": 0.2,
      "one_epoch": 1,
      "two_epochs": 1
    },
    {
      "tail": 0.5,
      "one_epoch": 1,
      "two_epochs": 1
    }
  ]
};
