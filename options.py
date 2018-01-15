""
"  Contains the Options for the Highcharts "
""

OPTIONS = {
    "chart": {
        "zoomType": 'x'
    },
    "xAxis": {
        "type": 'datetime'
    },
    "yAxis": {
        "title": {
            "text": 'Air Quality Index'
        }
    },
    "legend": {
        "enabled": False
    },
    "plotOptions": {
        "area": {
            "fillColor": {
                "linearGradient": {
                    "x1": 0,
                    "y1": 0,
                    "x2": 0,
                    "y2": 1
                },
                "stops": [
                    [0, Highcharts.getOptions().colors[0]],
                    [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                ]
            },
            "marker": {
                "radius": 2
            },
            "lineWidth": 1,
            "states": {
                "hover": {
                    "lineWidth": 1
                }
            },
            "threshold": None
        }
    }
}