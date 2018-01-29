"""Contains all static references"""

DATA_DIR = "datas"

PLOT_DIR = "plots"

HEATMAP_DIR = "heatmap"

LINE_DIR = "line"

DIRECTORIES = [DATA_DIR, PLOT_DIR, PLOT_DIR + "\\" + HEATMAP_DIR]

REQ_COLUMNS = ['Stn Code', 'Sampling Date', 'State', 'City/Town/Village/Area',
               'Location of Monitoring Station', 'SO2', 'NO2',
               'RSPM/PM10']

HEATMAP_COLUMNS = ['Stn Code', 'City', 'Year',
                   'Month', 'AQI']

LINE_COLUMNS = ['Stn Code', 'City', 'Year',
                'MaxAQI', 'MinAQI', 'MedianAQI']

LOCATION = {
    38: "Kathivakkam, Chennai",
    71: "Manali, Chennai",
    72: "Thiruvottiyur, Chennai",
    159: "Madras Medical College, Chennai",
    160: "NEERI CSIR Campus, Chennai",
    237: "SIDCO Office, Coimbatore",
    238: "Dist. Collector's Office, Coimbatore",
    239: "Fisheries College, Tuticorin",
    240: " Raja Agencies, Tuticorin",
    306: "Highways Project Building, Madurai",
    307: "Fenner, Madurai",
    308: "Kunnathur Chatram East Avani Mollai Street, Madurai",
    366: "AVM Jewellery Building, Tuticorin",
    375: "Poniarajapuram, Coimbatore",
    764: "Adyar, Chennai",
    765: "Anna Nagar, Chennai",
    766: "Thiyagaraya Nagar, Chennai",
    767: "Kilpauk, Chennai",
    769: "Gandhi Market, Trichy",
    770: "Main Guard Gate, Trichy",
    771: "Bishop Heber College, Trichy",
    772: "Golden Rock, Trichy",
    773: "Central Bus Stand, Trichy"
}
