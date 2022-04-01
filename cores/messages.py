RESPONSE_ERROR = {
    'GENERAL_ERROR_REQUEST': {
        'status': 510,
        'code': 'GENERAL_ERROR_REQUEST',
        'message': 'Permintaan tidak bisa diproses. Mohon menunggu selama beberapa waktu sebelum mencoba lagi. Jika masih mengalami kendala Hubungi CS 12345.'
    },
    'INVALID_HEADERS_JSON': {
        'status': 420,
        'code': 'INVALID_HEADERS_JSON',
        'message': 'Permintaan tidak bisa diproses. Pastikan data yang anda kirim menggunakan format json.'
    },
    'INVALID_REQUEST_PARAMETER': {
        'status': 420,
        'code': 'INVALID_REQUEST_PARAMETER',
        'message': 'Permintaan tidak bisa diproses. Mohon menunggu selama beberapa waktu sebelum mencoba lagi. Jika masih mengalami kendala Hubungi CS 12345.'
    },
    'EVENT_ID_ALREADY_EXIST': {
        'status': 420,
        'code': 'EVENT_ID_ALREADY_EXIST',
        'message': 'Permintaan tidak bisa diproses. Silahkan masukkan kembali event_id dengan nilai yang berbeda.'
    },
}

RESPONSE_SUCCESS = {
    'SUCCESS_CREATE': {
        'status': 201,
        'code': 'SUCCESS',
        'message': 'Request processed successfully'
    },
    'SUCCESS': {
        'status': 200,
        'code': 'SUCCESS',
        'message': 'Request processed successfully'
    },
}
