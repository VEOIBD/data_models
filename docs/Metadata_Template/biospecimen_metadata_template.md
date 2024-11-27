---
datatable: true
layout: page
parent: Metadata_Template
permalink: docs/Biospecimen_Metadata_Template.html
title: Biospecimen_Metadata_Template
---

{% assign mydata=site.data.Metadata_Template.biospecimen_metadata_template %} 
{: .note-title } 
>Biospecimen_Metadata_Template
>
>VEOIBD Biospecimen Metadata Template [[Source]](https://docs.google.com/document/d/11xPPfJp89Ge0dZGzud4T6ixQhXj8a_BJtkTQ7K1UDyU/edit#heading=h.agzpcnpjw4d9)
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
  var pages = ['type_key', 'sample_tissue_type', 'specimen_area_biopsy', 'media', 'sample_key', 'volume', 'inflammation', 'sample_type', 'project', 'rna_batch', 'ratio260over230', 'library_preparation_method', 'rna_isolation_kit', 'ratio260over280', 'RIN', 'DV200', 'immunodeficiency', 'sex', 'perianal_involvement', 'age_at_diagnosis', 'individual_id', 'external_share', 'local_id', 'growth_delay', 'autoimmune', 'breastfed', 'participant_role', 'gi_phenotype', 'upper_disease_type', 'participant_id', 'family_id', 'race', 'site', 'gi_surgeries', 'jewish_origin', 'ethnicity', 'consanguinity', 'disease_activity_behavior', 'extraintestinal_manifestations', 'ibd_history', 'disease_activity_location', 'filename', 'biospecimen_metadata_template', 'bulk_RNASeq_assay_template', 'scRNASeq_assay_template', 'clinical_metadata_template', 'medication_history_metadata_template', 'metadata_type', 'resource_type', 'file_format', 'metadata_file_annotations', 'bulk_RNASeq_raw_file_annotations', 'bulk_RNASeq_counts_file_annotations', 'run_type', 'reference_set', 'median_genes', 'alignment_information', 'read_length', 'unique_genes', 'genomic_sex', 'data_subtype', 'read_strand_origin', 'median_umis', 'total_unmapped_reads', 'data_type', 'number_cells', 'mapped_reads', 'library_version', 'analysis_type', 'sequencing_batch', 'kit_number', 'total_reads', 'library_type', 'is_stranded', 'rRNA_rate', 'vendor', 'platform', 'valid_barcode_reads', 'library_prep', 'analysis_thresholds', 'ratio_mitochondria', 'library_id', 'duplication_rate', 'sample_status', 'nucleic_acid_source', 'sample_barcode', 'assay', 'library_batch'];
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