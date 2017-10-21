import gviz_api
from ..models import DataPoint


def as_html(detailed_url, all):
    html = """
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
  <script src='http://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>
  
    <script type="text/javascript">
      google.charts.load("current", {{packages: ["corechart"]}});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {{
        var data = new google.visualization.DataTable({0})
        
        var date_formatter = new google.visualization.DateFormat({{pattern: 'd.MMM HH:mm'}});
        date_formatter.format(data, 0);

        var options = {{
          title: '{1}',
          curveType: 'line',
          legend: {{ position: 'none' }},
          hAxis: {{format: 'HH:mm'}},
          vAxis: {{format: '#'}},
        chartArea: {{
            left: 30,
            top: 5,
            bottom: 50,
            right: 5,
            width: '80%',
            height: '100%'
        }},
        pointSize: 5,
        dataOpacity: 0.5,
        }};

        var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

        chart.draw(data, options);
      }}
      

    $(window).resize(function(){{
      drawChart();
    }});
    </script>
    <div id="curve_chart" style="width: 100%; min-height: 350px; padding-top: -25px"></div>
    """

    vars = DataPoint.url_to_variables[detailed_url]
    lookup = DataPoint.variable_lookup

    description = {"time": ("datetime", "Year")}
    variable_description = {var : ("number", lookup[var]['verbal']) for var in vars}
    description.update(variable_description)
    data = []
    for entry in all:
        data_add = {"time": entry.time.astimezone()}
        data_add.update({var : getattr(entry, var) for var in vars})
        data.append(data_add)

    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)

    # Creating a JSon string
    columns = ("time",) + tuple(var for var in vars)
    json = data_table.ToJSon(columns_order=columns, order_by="time")

    # Put the JS code and JSON string into the template.
    html = html.format(json, detailed_url)
    return html


def html_graph(detailed_url, start, end):
    all = DataPoint.objects.filter(time__range=(start, end))
    return as_html(detailed_url, all)
