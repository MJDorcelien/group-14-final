
def test_get_all_courses_empty(test_client):
    resp=test_client.get('/courses')
    resp_data=resp.data.decode('utf-8')

    assert '<div class="row align-items-start">' not in resp_data
    assert '<div class="col">' not in resp_data