function categorySelect2() {
    $('#catNameSelect').select2({
        placeholder: "Select Category",
        minimumInputLength: 1,
        ajax: {
            url: "/admin/api/search/category",
            type: "GET",
            dataType: 'json',
            headers: {Authorization: 'Bearer ' + localStorage.getItem('access_token')},
            data: function (params) {
                return {search: params.term,}
            },
            processResults: function (response) {
                if (response.detail) {
                    localStorage.removeItem('access_token')
                    window.location.href = '/admin/login'
                }
                if (response.success) {
                    return {results: response.data.map(catObj => ({'id': catObj.cat_id, 'text': catObj.cat_name}))}
                }
            }
        }
    })
}

document.addEventListener('DOMContentLoaded', function () {
    categorySelect2()
})
