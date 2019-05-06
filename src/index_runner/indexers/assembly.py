# from utils.get_path import get_path
from .indexer_utils import mean


def index_assembly(obj_data, ws_info, obj_data_v1):
    """
    Currently Handles the follownig workspace types:
         KBaseGenomeAnnotations.Assembly-6.0
    """
    data = obj_data['data'][0]
    info = data['info']
    if not data.get('data'):
        raise Exception("no data in object")
    data = data['data']

    workspace_id = info[6]
    object_id = info[0]

    # get assembly type
    assembly_type = info[2].split('-')[0]
    assembly_type_version = info[2].split('-')[1]

    # get mean contig length
    if data.get('contigs'):
        # we do not include the contig if it does not store the requisite field
        mean_contig_length = mean([contig.get('length') for contig_id, contig
                                   in data['contigs'].items() if contig.get('length')])
        percent_complete_contigs = mean([contig.get('is_complete') for contig_id, contig
                                         in data['contigs'].items() if contig.get('is_complete')])
        percent_circle_contigs = mean([contig.get('is_circ') for contig_id, contig
                                       in data['contigs'].items() if contig.get('is_circ')])
    else:
        mean_contig_length, percent_complete_contigs, percent_circle_contigs = None, None, None
    return {
        'doc': {
            "assembly_name": data.get("name", None),
            "mean_contig_length": mean_contig_length,
            "percent_complete_contigs": percent_complete_contigs,
            "percent_circle_contigs": percent_circle_contigs,
            "assembly_type": assembly_type,
            "assembly_type_version": assembly_type_version,
            "assembly_id": data.get('assembly_id', None),
            "gc_content": data.get('gc_content', None),
            "size": data.get('dna_size', None),
            "num_contigs": data.get('num_contigs', None),
            "taxon_ref": data.get('taxon_ref', None),
            "external_origination_date": data.get('external_source_origination_date', None),
            "external_source_id": data.get('external_source_id', None),
            "external_source": data.get('external_source', None),
        },
        'index': "assembly",
        'id': f"{workspace_id}:{object_id}",
    }