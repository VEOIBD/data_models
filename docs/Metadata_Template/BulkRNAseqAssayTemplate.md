---
datatable: true
layout: page
parent: Metadata_Template
permalink: docs/ Bulk Rnaseq Assay Template.html
title: ' Bulk Rnaseq Assay Template'
---

{% assign mydata=site.data.Metadata_Template.BulkRNAseqAssayTemplate %} 
{: .note-title } 
> Bulk Rnaseq Assay Template
>
>VEOIBD Bulk RNASeq Assay Metadata Template [[Source]](https://docs.google.com/document/d/1ADIApJgEpbA1XaLig1dlxwUE5VfQkESyxHerabsbXPY/edit#heading=h.agzpcnpjw4d9)
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
  var pages = ['rnaIsolationKit', 'ratio260over230', 'DV200', 'RIN', 'libraryPreparationMethod', 'ratio260over280', 'cellViability', 'rnaBatch', 'BulkRNAseqRawFileAnnotations', 'MetadataFileAnnotations', 'BulkRNASeqCountsFileAnnotations', 'metadataType', 'resourceType', 'fileFormat', 'ageAtDiagnosis', 'jewishOrigin', 'Sibling', 'growthDelay', 'autoimmune', 'breastfed', 'breastfeedingDuration', 'immunodeficiencyDiagnosis', 'birthCountry', 'participantRole', 'sex', 'diseaseActivityLocation', 'extraintestinalManifestationsHistory', 'GISurgeries', 'isRC2', 'race', 'GISurgeriesDetails', 'upperDiseaseType', 'localID', 'perianalInvolvement', 'individualID', 'diseaseActivityBehavior', 'siblingType', 'site', 'secondHandSmokeExposure', 'autoimmuneDetails', 'IBDHistory', 'ethnicity', 'GIPhenotype', 'familyID', 'consanguinity', 'Proband', 'numberCells', 'dataType', 'totalReads', 'medianGenes', 'medianUMIs', 'kitNumber', 'readLength', 'analysisThresholds', 'alignmentInformation', 'referenceSet', 'vendor', 'assay', 'readStrandOrigin', 'mappedReads', 'sequencingBatch', 'totalUnmappedReads', 'validBarcodeReads', 'nucleicAcidSource', 'runType', 'sampleStatus', 'analysisType', 'dataSubtype', 'isStranded', 'uniqueGenes', 'platform', 'ratioMitochondria', 'libraryVersion', 'sampleBarcode', 'genomicSex', 'libraryType', 'libraryBatch', 'libraryID', 'rRNARate', 'libraryPrep', 'duplicationRate', 'uniqueID', 'volumeUnit', 'specimenIDSource', 'preservationMethod', 'sampleType', 'cellNumber', 'notes', 'shippingTrackingNumber', 'fundingSource', 'Biopsy', 'collectionDate', 'biopsyInflammationStatus', 'Serum', 'biopsyLocation', 'volume', 'PBMC', 'sampleKey', 'PAX', 'specimenID', 'biopsiesNumber', 'diagnosisCategory', 'shippingVendor', 'sampleTissueType', 'Filename'];
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