
GROUP_ID_KEYS = {
    'SAMP': {
        'samp_id_keys': ['SAMP_ID'],
        'comp_id_keys': ['LOCA_ID', 'SAMP_TOP', 'SAMP_TYPE', 'SAMP_REF']
    },
    'CBRT': {
        'samp_id_keys': ['SAMP_ID', 'CBRT_TESN'],
        'comp_id_keys': ['LOCA_ID', 'SAMP_TOP', 'SAMP_TYPE', 'SAMP_REF', 'CBRT_TESN']
    },
    'CHOC': {
        'samp_id_keys': ['SAMP_ID', 'CHOC_REF'],
        'comp_id_keys': ['LOCA_ID', 'SAMP_TOP', 'SAMP_TYPE', 'SAMP_REF', 'CHOC_REF']
    },
    'CMPG': {
        'samp_id_keys': ['SAMP_ID', 'CMPG_TESN'],
        'comp_id_keys': ['LOCA_ID', 'SAMP_TOP', 'SAMP_TYPE', 'SAMP_REF', 'CMPG_TESN']
    },
    'CMPT': {
        'samp_id_keys': ['SAMP_ID', 'CMPG_TESN', 'CMPT_TESN'],
        'comp_id_keys': ['LOCA_ID', 'SAMP_TOP', 'SAMP_TYPE', 'SAMP_REF', 'CMPG_TESN', 'CMPT_TESN']
    },
    'CONS': {
        'samp_id_keys': ['SAMP_ID', 'CONS_INCN'],
        'comp_id_keys': ['LOCA_ID', 'SAMP_TOP', 'SAMP_TYPE', 'SAMP_REF', 'CONS_INCN']
    },
    'ERES': {
        'samp_id_keys': ['SAMP_ID', 'ERES_CODE', 'ERES_MATX', 'ERES_METH', 'ERES_RTYP'],
        'comp_id_keys': ['LOCA_ID', 'SAMP_TOP', 'SAMP_TYPE', 'SAMP_REF',
                         'ERES_CODE', 'ERES_MATX', 'ERES_METH', 'ERES_RTYP']
    },
    'ESCT': {
        'samp_id_keys': ['SAMP_ID', 'ESCT_INCN'],
        'comp_id_keys': ['LOCA_ID', 'SAMP_TOP', 'SAMP_TYPE', 'SAMP_REF', 'ESCT_INCN']
    },
    'GCHM': {
        'samp_id_keys': ['SAMP_ID', 'GCHM_CODE', 'GCHM_METH', 'GCHM_TTYP'],
        'comp_id_keys': ['LOCA_ID', 'SAMP_TOP', 'SAMP_TYPE', 'SAMP_REF', 'GCHM_CODE', 'GCHM_METH', 'GCHM_TTYP']
    },
    'GRAT': {
        'samp_id_keys': ['SAMP_ID', 'GRAT_SIZE'],
        'comp_id_keys': ['LOCA_ID', 'SAMP_TOP', 'SAMP_TYPE', 'SAMP_REF', 'GRAT_SIZE']
    },
    'LBST': {
        'samp_id_keys': ['SAMP_ID', 'LBSG_REF', 'LBST_TEST'],
        'comp_id_keys': ['LOCA_ID', 'SAMP_TOP', 'SAMP_TYPE', 'SAMP_REF', 'LBSG_REF', 'LBST_TEST']
    },
    'LSTT': {
        'samp_id_keys': ['SAMP_ID', 'LSTT_TESN'],
        'comp_id_keys': ['LOCA_ID', 'SAMP_TOP', 'SAMP_TYPE', 'SAMP_REF', 'LSTT_TESN']
    },
    'MCVT': {
        'samp_id_keys': ['SAMP_ID', 'MCVT_TESN'],
        'comp_id_keys': ['LOCA_ID', 'SAMP_TOP', 'SAMP_TYPE', 'SAMP_REF', 'MCVT_TESN']
    },
    'RCCV': {
        'samp_id_keys': ['SAMP_ID', 'RCCV_TESN'],
        'comp_id_keys': ['LOCA_ID', 'SAMP_TOP', 'SAMP_TYPE', 'SAMP_REF', 'RCCV_TESN']
    },
    'SHBT': {
        'samp_id_keys': ['SAMP_ID', 'SHBT_TESN'],
        'comp_id_keys': ['LOCA_ID', 'SAMP_TOP', 'SAMP_TYPE', 'SAMP_REF', 'SHBT_TESN']
    },
    'TNPC': {
        'samp_id_keys': ['SAMP_ID', 'TNPC_TESN'],
        'comp_id_keys': ['LOCA_ID', 'SAMP_TOP', 'SAMP_TYPE', 'SAMP_REF', 'TNPC_TESN']
    },
    'TRET': {
        'samp_id_keys': ['SAMP_ID', 'TRET_TESN'],
        'comp_id_keys': ['LOCA_ID', 'SAMP_TOP', 'SAMP_TYPE', 'SAMP_REF', 'TRET_TESN']
    },
    'TRIT': {
        'samp_id_keys': ['SAMP_ID', 'TRIT_TESN'],
        'comp_id_keys': ['LOCA_ID', 'SAMP_TOP', 'SAMP_TYPE', 'SAMP_REF', 'TRIT_TESN']
    },
}


def get_group_id_keys(group):
    return GROUP_ID_KEYS.get(group, GROUP_ID_KEYS['SAMP'])
