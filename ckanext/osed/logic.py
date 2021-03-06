from collections import OrderedDict
from ckan.plugins.toolkit import get_or_bust, side_effect_free
from ckan.logic import NotFound
import ckan.plugins.toolkit as tk
from ckanext.osed.helpers import get_content_headers

import logging
log = logging.getLogger(__name__)


@side_effect_free
def osed_dataset_count(context, data_dict):
    '''
    Return the total number of datasets and the number of dataset per group.
    '''
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    req_context = {'user': user['name']}

    # group_list contains the number of datasets in the 'packages' field
    groups = tk.get_action('group_list')(req_context, {'all_fields': True})
    group_count = OrderedDict()
    for group in groups:
        group_count[group['name']] = group['package_count']

    # get the total number of dataset from package_search
    search_result = tk.get_action('package_search')(
        req_context,
        {'rows': 0, 'fq': '+dataset_type:dataset'}
    )

    return {
        'total_count': search_result['count'],
        'groups': group_count,
    }


@side_effect_free
def osed_content_headers(context, data_dict):
    '''
    Returns some headers of a remote resource
    '''
    url = get_or_bust(data_dict, 'url')
    response = get_content_headers(url)
    return {
        'status_code': response.status_code,
        'content-length': response.headers.get('content-length', ''),
        'content-type': response.headers.get('content-type', ''),
    }


@side_effect_free
def osed_dataset_terms_of_use(context, data_dict):
    '''
    Returns the terms of use for the requested dataset.

    By definition the terms of use of a dataset corresponds
    to the least open rights statement of all distributions of
    the dataset
    '''
    terms = [
        'NonCommercialAllowed-CommercialAllowed-ReferenceNotRequired',
        'NonCommercialAllowed-CommercialAllowed-ReferenceRequired',
        'NonCommercialAllowed-CommercialWithPermission-ReferenceNotRequired',
        'NonCommercialAllowed-CommercialWithPermission-ReferenceRequired',
        'ClosedData',
    ]
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    req_context = {'user': user['name']}
    pkg_id = get_or_bust(data_dict, 'id')
    pkg = tk.get_action('package_show')(req_context, {'id': pkg_id})

    least_open = None
    for res in pkg['resources']:
        try:
            if res['rights'] not in terms:
                least_open = 'ClosedData'
                break
            if least_open is None:
                least_open = res['rights']
                continue
            if terms.index(res['rights']) > terms.index(least_open):
                least_open = res['rights']
        except KeyError:
            pass

    if least_open is None:
        least_open = 'ClosedData'

    return {
        'dataset_rights': least_open
    }


@side_effect_free
def osed_dataset_by_identifier(context, data_dict):
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context.update({'user': user['name']})
    identifier = get_or_bust(data_dict, 'identifier')

    param = 'identifier:%s' % identifier
    result = tk.get_action('package_search')(context, {'fq': param})
    try:
        return result['results'][0]
    except (KeyError, IndexError, TypeError):
        raise NotFound
