---
title: "data_code"
parent: Attributes
datatable: true
layout: page
nav_order: "47"
permalink: "docs/attributes/data_code.html"
date: "2025-03-18"
params:
  title: ""
  rank: ""
---
{% assign mydata=site.data.csv.attributes.data_code %} 

{% include content/data_code.md %}

<table id="myTable" class="display" style="width:100%">
    <thead>
    {% for column in mydata[0] %}
        <th>{{ column[0] }}</th>
    {% endfor %}
    </thead>
    <tbody>
    {% for row in mydata %}
        <tr>
        {% for cell in row %}
            <td>{{ cell[1] }}</td>
        {% endfor %}
        </tr>
    {% endfor %}
    </tbody>
</table>
<script type="text/javascript">
  $(document).ready(function () {
    $('#myTable').DataTable({
      responsive: true,
      deferRender: false,
      paging: false,
      order: [],
    });
  });
</script>
