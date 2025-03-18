---
title: "jewish_origin"
parent: Attributes
datatable: true
layout: page
nav_order: "86"
permalink: "docs/attributes/jewish_origin.html"
date: "2025-03-18"
params:
  title: ""
  rank: ""
---
{% assign mydata=site.data.csv.attributes.jewish_origin %} 

{% include content/jewish_origin.md %}

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
