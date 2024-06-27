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
  var pages = ['data_subtype', 'rRNA_rate', 'platform', 'library_version', 'total_unmapped_reads', 'vendor', 'sample_barcode', 'sequencing_batch', 'run_type', 'read_strand_origin', 'total_reads', 'mapped_reads', 'kit_number', 'unique_genes', 'nucleic_acid_source', 'median_umis', 'alignment_information', 'number_cells', 'is_stranded', 'sample_status', 'valid_barcode_reads', 'genomic_sex', 'ratio_mitochondria', 'median_genes', 'analysis_type', 'data_type', 'library_batch', 'library_id', 'analysis_thresholds', 'library_type', 'assay', 'library_prep', 'read_length', 'reference_set', 'duplication_rate', 'file_format', 'resource_type', 'metadata_type', 'metadata_file_annotations', 'bulk_RNASeq_counts_file_annotations', 'bulk_RNASeq_raw_file_annotations', 'library_preparation_method', 'ratio260over230', 'DV200', 'ratio260over280', 'RIN', 'rna_batch', 'rna_isolation_kit', 'filename', 'race', 'gi_phenotype', 'disease_activity_location', 'ethnicity', 'consanguinity', 'family_id', 'site', 'external_share', 'breastfed', 'extraintestinal_manifestations', 'jewish_origin', 'autoimmune', 'individual_id', 'participant_role', 'age_at_diagnosis', 'gi_surgeries', 'perianal_involvement', 'upper_disease_type', 'disease_activity_behavior', 'local_id', 'immunodeficiency', 'sex', 'participant_id', 'ibd_history', 'growth_delay', 'specimen_area_biopsy', 'inflammation', 'project', 'volume', 'sample_tissue_type', 'sample_type', 'media', 'sample_key', 'type_key', 'collection_date', 'biospecimen_metadata_template', 'bulk_RNASeq_assay_template', 'medication_history_metadata_template', 'clinical_metadata_template', 'scRNASeq_assay_template'];
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