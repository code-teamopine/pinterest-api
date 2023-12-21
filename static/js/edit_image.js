const imageApiObj = {imgIsActive: '', imgCatId: '', imgCatName: ''}

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

function getImage() {
    fetch(`/admin/api/image/${imgId}`, {method: 'GET', headers: {Authorization: 'Bearer ' + localStorage.getItem('access_token')}})
    .then(response => response.json())
    .then(body => {
        if (body.detail) {
            localStorage.removeItem('access_token')
            window.location.href = '/admin/login'
        }

        if (body.success === true) {
            imageApiObj.imgIsActive = Boolean(body.data.img_is_active), imageApiObj.imgCatId = body.data.cat_id, imageApiObj.imgCatName = body.data.cat_name
            document.querySelector('#imgImgId').src = '/' + body.data.img_file, document.querySelector('#imageIsActiveCheckBox').checked = imageApiObj.imgIsActive, document.querySelector('#catNameSelect').innerHTML = `<option value="${imageApiObj.imgCatId}" selected>${imageApiObj.imgCatName}</option>`
            categorySelect2()
        }
        else {
            alert(body.msg)
        }
    })
}

document.querySelector('#editImageFormId').addEventListener('submit', (e) => {
    e.preventDefault()
    const catNameInput = Number(e.target.elements['catNameSelect'].value), imageInput = e.target.elements['imageInput'].files[0], imgIsActive = e.target.elements['imageIsActiveCheckBox'].checked, formData = new FormData()
    let editFlag = false
    if (catNameInput && catNameInput != imageApiObj.imgCatId) {
        formData.append('cat_id', catNameInput), editFlag = true
    }
    if (imgIsActive != imageApiObj.imgIsActive) {
        formData.append('img_is_active', imgIsActive), editFlag = true
    }
    if (imageInput) {
        console.log(imageInput)
        const supportedFileType = ["image/png", "image/jpg", "image/jpeg"]
        if (! supportedFileType.includes(imageInput.type)) {
            alert("file type must be image/png or image/jpeg")
            return false
        }
        formData.append('img_file', imageInput), editFlag = true
    }
    if (editFlag === true) {
        fetch(`/admin/api/image/edit/${imgId}`, {method: 'PATCH', headers: {Authorization: 'Bearer ' + localStorage.getItem('access_token')}, body: formData})
        .then(response => response.json())
        .then(body => {
            if (body.detail) {
                localStorage.removeItem('access_token')
                window.location.href = '/admin/login'
            }
            if (body.success === true) {
                alert(body.msg)
                window.location.href = `/admin/`
            }
            else {
                alert(body.msg)
            }
        })
    }
    else {
        alert('please enter any value for edit image')
    }
})

document.addEventListener('DOMContentLoaded', function () {
    getImage()
})
