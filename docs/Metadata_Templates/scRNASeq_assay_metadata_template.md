---
datatable: true
layout: page
parent: Metadata Templates
permalink: docs/scRNASeq_assay_metadata_template.html
title: Sc Rnaseq Assay Metadata Template
---

{% assign mydata=site.data.Metadata_Templates.scRNASeq_assay_metadata_template %} 
{: .note-title } 
>Sc Rnaseq Assay Metadata Template
>
>Template for collecting metadata about scRNA-seq data. [[Source]](nan)
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
  var pages = ['clinical_metadata_template', 'medication_history_metadata_template', 'scRNASeq_assay_metadata_template', 'biospecimen_metadata_template', 'ibd_history', 'participant_role', 'immunodeficiency', 'family_id', 'perianal_involvement', 'age_at_diagnosis', 'jewish_origin', 'site', 'local_id', 'ethnicity', 'individual_id', 'gi_phenotype', 'autoimmune', 'disease_activity_location', 'race', 'breastfed', 'gi_surgeries', 'external_share', 'participant_id', 'extraintestinal_manifestations', 'disease_activity_behavior', 'upper_disease_type', 'sex', 'growth_delay', 'consanguinity', 'sample_type', 'sample_id', 'sample_key', 'media', 'volume', 'project', 'type_key', 'collection_id', 'collection_age', 'sample_num', 'vial_label', 'specimen_area_biopsy', 'inflammation', 'collection_num', 'assay_metadata_synID', 'biospecimen_metadata_synID', 'metadata_type', 'data_level', 'specimen_modality', 'resource_type', 'cellranger_output_class', 'data_type', 'file_format', 'platform', 'scRNASeq_level_3_file_annotations_template', 'scRNASeq_level_1_file_annotations_template', 'metadata_file_annotations', 'data_code', 'i5_index', 'library_date', 'avg_reads_cell', 'sequencing_saturation', 'confident_transcriptome', 'estimated_cells', 'library_prep_method', 'digestion_cdna_date', 'genes_detected', 'Q30_read', 'confident_reads', 'confident_intergenic', 'gex_con_ng_uL', 'reads_mapped', 'total_reads', 'median_UMI_cell', 'fragment_size_bp', 'software_and_version', 'percent_cell_viability', 'Q30_bc', 'confident_exonic', 'confident_intronic', 'Q30_UMI', 'alignment_reference', 'i7_index', 'cell_count_1mL', 'reads_antisense', 'reads_in_cells', 'median_genes_cell', 'valid_bc', 'valid_UMI'];
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