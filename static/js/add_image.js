document.querySelector('#addImageFormId').addEventListener("submit", (e) => {
    e.preventDefault()
    const categoryId = Number(e.target.elements['catNameSelect'].value), imgFile = e.target.elements['imageInput'].files[0], imgIsActive = e.target.elements['imageIsActiveCheckBox'].checked

    if (! categoryId) {
        alert('please select any category.')
        return false
    }
    if (! imgFile) {
        alert('image is required.')
        return false
    }
    const supportedFileType = ["image/png", "image/jpg", "image/jpeg"]
    if (! supportedFileType.includes(imgFile.type)) {
        alert("file type must be image/png or image/jpeg")
        return false
    }

    const formData = new FormData()
    formData.append('cat_id', categoryId)
    formData.append('img_is_active', imgIsActive)
    formData.append('img_file', imgFile)

    fetch(`/admin/api/image/add`, {method: 'POST', headers: {Authorization: 'Bearer ' + localStorage.getItem('access_token')}, body: formData})
    .then(response => response.json())
    .then(body => {
        if (body.detail) {
            localStorage.removeItem('access_token')
            window.location.href = '/admin/login'
        }
        if (body.success === true) {
            alert(body.msg)
            window.location.href = '/admin/'
        }
        else {
            alert(body.msg)
            document.querySelector('#addCategoryFormId').reset()
        }
    })
})

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
