---
datatable: true
layout: page
parent: Metadata Templates
permalink: docs/medication_history_metadata_template.html
title: Medication History Metadata Template
---

{% assign mydata=site.data.Metadata_Templates.medication_history_metadata_template %} 
{: .note-title } 
>Medication History Metadata Template
>
>VEOIBD Medication History Metadata Template [[Source]](https://docs.google.com/document/d/1yN6TlK2VGP-vKvW5E8wucLjKQq769xoz4QW5OjgR29k/edit#heading=h.agzpcnpjw4d9)
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
  var pages = ['type_key', 'specimen_area_biopsy', 'media', 'sample_id', 'sample_key', 'volume', 'inflammation', 'sample_type', 'project', 'biospecimen_metadata_template', 'clinical_metadata_template', 'medication_history_metadata_template', 'metadata_file_annotations', 'immunodeficiency', 'sex', 'perianal_involvement', 'age_at_diagnosis', 'individual_id', 'external_share', 'local_id', 'growth_delay', 'autoimmune', 'breastfed', 'participant_role', 'gi_phenotype', 'upper_disease_type', 'participant_id', 'family_id', 'race', 'site', 'gi_surgeries', 'jewish_origin', 'ethnicity', 'consanguinity', 'disease_activity_behavior', 'extraintestinal_manifestations', 'ibd_history', 'disease_activity_location', 'data_code', 'metadata_type', 'platform', 'resource_type', 'file_format', 'assay'];
  $('#myTable').DataTable({
    responsive: {
        details: {
            display: $.fn.dataTable.Responsive.display.modal( {
                header: function ( row ) {
                    var data = row.data();
                    return 'Details for '+data[0]+' ';
                }
            } ),
            renderer: $.fn.dataTable.Responsive.renderer.tableAll({
                tableClass: "table"
            })
        }
    },
   "deferRender": true,
   "columnDefs": [
      { 
         targets: 0,
         render : function(data, type, row, meta){
            if(type === 'display' & $.inArray( data, pages) != -1){
               return $('<a>')
                  .attr('href',row[7]+'/'+data)
                  .text(data)
                  .wrap('<div></div>')
                  .parent()
                  .html();} 
             else {
               return data;
            }
         }
      },
      {
        targets: [6,7],
          render : function(data, type, row, meta){
         if(type === 'display' & data != 'Sage Bionetworks'){
            return $('<a>')
               .attr('href', data)
               .text(data)
               .wrap('<div></div>')
               .parent()
               .html();} 
         if(type === 'display' & data == 'Sage Bionetworks'){
             return $('<a>')
                .attr('href', 'https://sagebionetworks.org/')
                .text(data)
                .wrap('<div></div>')
                .parent()
                .html();
         
         } else {
            return data;
         }
      }
   }
   ]
});
</script>