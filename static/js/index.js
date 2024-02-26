const pageNoAndFlagObj = {pageNo: 1, scrollFlag: false}

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

document.querySelector('#addCategoryFormId').addEventListener("submit", (e) => {
    e.preventDefault()
    const catName = e.target.elements['catNameInput'].value, catSubTitle = e.target.elements['catSubTitleInput'].value, catCoverImage = e.target.elements['catCoverImageInput'].files[0], catIsActive = e.target.elements['catIsActiveCheckBox'].checked
    
    if (! catName) {
        alert('Category Name is required.')
        return false
    }
    if (! catSubTitle) {
        alert('Category Sub Title is required.')
        return false
    }
    if (! catCoverImage) {
        alert('image is required.')
        return false
    }
    const supportedFileType = ["image/png", "image/jpg", "image/jpeg"]
    if (! supportedFileType.includes(catCoverImage.type)) {
        alert("file type must be image/png or image/jpeg")
        return false
    }
    
    const formData = new FormData()
    formData.append('cat_name', catName)
    formData.append('cat_sub_title', catSubTitle)
    formData.append('cat_cover_image', catCoverImage)
    formData.append('cat_is_active', catIsActive)

    fetch(`/admin/api/category/add`, {method: 'POST', headers: {Authorization: 'Bearer ' + localStorage.getItem('access_token')}, body: formData})
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

function getCategory() {
    fetch(`/admin/api/category?page_no=${pageNoAndFlagObj.pageNo}`, {method: 'GET', headers: {Authorization: 'Bearer ' + localStorage.getItem('access_token')}})
    .then(response => response.json())
    .then(body => {
        if (body.detail) {
            localStorage.removeItem('access_token')
            window.location.href = '/admin/login'
        }
        if (body.success === true) {
            let htmlStr = ``
            body.data.forEach(categoryObj => {
                htmlStr += `<div class="col-lg mb-3">
                                    <div class="card category-card">
                                            <a href="/admin/category/${categoryObj.cat_id}" class="text-decoration-none">
                                                <div class="card-img">
                                                    <img src="/${categoryObj.cat_cover_image}" class="card-img-top lazyLoad" alt="...">
                                                </div>
                                                <div class="card-body">
                                                    <h5 class="card-title">${categoryObj.cat_name}</h5>
                                                    <p title="${categoryObj.cat_sub_title}" class="card-text">${categoryObj.cat_sub_title}</p>
                                                <button><span> Active </span></button>
                                                </div>
                                            </a>
                                        </div>
                                    </div>
                            `
            })
            document.querySelector('#categoryGridDivId').innerHTML += htmlStr
            pageNoAndFlagObj.scrollFlag = false
        }
        else {
            console.log(body.msg)
        }
    })
}

document.addEventListener('DOMContentLoaded', function () {
    forScrollerSet(pageNoAndFlagObj, getCategory, '#categoryGridDivId')
    categorySelect2()
})
