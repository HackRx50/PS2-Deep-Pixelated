graph [
  directed 1
  node [
    id 1
    label "IVDD"
    description "Intervertebral Disc Degeneration"
  ]
  node [
    id 2
    label "L4-L6"
    description "Lumbar Vertebrae from L4 to L6"
  ]
  node [
    id 3
    label "L6-L7"
    description "Lumbar Vertebrae from L6 to L7"
  ]
  node [
    id 4
    label "CAD"
    description "Coronary Artery Disease"
  ]
  node [
    id 5
    label "ACS"
    description "Acute Coronary Syndrome"
  ]
  node [
    id 6
    label "CA"
    description "Cancer"
  ]
  node [
    id 7
    label "R BREAST"
    description "Right Breast"
  ]
  node [
    id 8
    label "CKD"
    description "Chronic Kidney Disease"
  ]
  node [
    id 9
    label "DM"
    description "Diabetes Mellitus"
  ]
  node [
    id 10
    label "UTI"
    description "Urinary Tract Infection"
  ]
  node [
    id 11
    label "HIN"
    description "Hypertension"
  ]
  node [
    id 12
    label "DCLD"
    description "Decompensated Chronic Liver Disease"
  ]
  node [
    id 13
    label "PRIMI"
    description "First Pregnancy"
  ]
  node [
    id 14
    label "G2PILI"
    description "Gravida 2 Para 1 Living 1"
  ]
  node [
    id 15
    label "HT"
    description "Hypertension"
  ]
  node [
    id 16
    label "MHD"
    description "Maintenance Hemodialysis"
  ]
  node [
    id 17
    label "CA L LUNG"
    description "Cancer of Left Lung"
  ]
  node [
    id 18
    label "CVA"
    description "Cerebrovascular Accident"
  ]
  node [
    id 19
    label "RE EYE CATARACT"
    description "Cataract in Right Eye"
  ]
  edge [
    source 1
    target 2
   relation "relation"
    description "Degeneration at lumbar spine levels L4 to L6"
  ]
  edge [
    source 1
    target 3
   relation "relation"
    description "Degeneration at lumbar spine levels L6 to L7"
  ]
  edge [
    source 4
    target 5
   relation "relation"
    description "Relation between coronary artery disease and acute coronary syndrome"
  ]
  edge [
    source 6
    target 7
   relation "relation"
    description "Cancer in the right breast"
  ]
  edge [
    source 8
    target 11
   relation "relation"
    description "Chronic kidney disease with hypertension"
  ]
  edge [
    source 9
    target 10
   relation "relation"
    description "Diabetes with urinary tract infection"
  ]
  edge [
    source 12
    target 10
   relation "relation"
    description "Chronic liver disease causing urinary tract infection"
  ]
  edge [
    source 13
    target 14
   relation "relation"
    description "First pregnancy with Gravida 2 Para 1"
  ]
  edge [
    source 16
    target 17
   relation "relation"
    description "Maintenance hemodialysis due to cancer of left lung"
  ]
  edge [
    source 18
    target 19
   relation "relation"
    description "Cerebrovascular accident impacting right eye with cataract"
  ]
]
