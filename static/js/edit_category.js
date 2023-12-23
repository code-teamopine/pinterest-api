const catApiDataObj = {catName: '', catSubTitle: '', catCoverImg: '', catIsActive: ''} 

function getCategoryData() {
    fetch(`/admin/api/category/${catId}`, {method: 'GET', headers: {Authorization: 'Bearer ' + localStorage.getItem('access_token')}})
    .then(response => response.json())
    .then(body => {
        if (body.detail) {
            localStorage.removeItem('access_token')
            window.location.href = '/admin/login'
        }
        if (body.success === true) {
            catApiDataObj.catName = body.data.cat_name, catApiDataObj.catCoverImg = body.data.cat_cover_image, catApiDataObj.catSubTitle = body.data.cat_sub_title, catApiDataObj.catIsActive = Boolean(body.data.cat_is_active)
            document.querySelector('#catCoverImageId').src = '/' + catApiDataObj.catCoverImg, document.querySelector('#catNameInput').value = catApiDataObj.catName, document.querySelector('#catSubTitleInput').value = catApiDataObj.catSubTitle, document.querySelector('#catIsActiveCheckBox').checked = catApiDataObj.catIsActive
        }
        else {
            console.log(body.msg)
            window.location.href = `/admin/`
        }
    })
}

document.querySelector('#editCategoryFormId').addEventListener('submit', (e) => {
    e.preventDefault()
    const catName = e.target.elements['catNameInput'].value, catSubTitle = e.target.elements['catSubTitleInput'].value, catCoverImage = e.target.elements['catCoverImageInput'].files[0], catIsActive = e.target.elements['catIsActiveCheckBox'].checked, formData = new FormData()
    let editFlag = false

    if (catName && catApiDataObj.catName != catName) {
        formData.append('cat_name', catName), editFlag = true
    }
    if (catSubTitle && catApiDataObj.catSubTitle != catSubTitle) {
        formData.append('cat_sub_title', catSubTitle), editFlag = true
    }
    if (catApiDataObj.catIsActive != catIsActive) {
        formData.append('cat_is_active', catIsActive), editFlag = true
    }
    if (catCoverImage) {
        const supportedFileType = ["image/png", "image/jpg", "image/jpeg"]
        if (! supportedFileType.includes(catCoverImage.type)) {
            alert("file type must be image/png or image/jpeg")
            return false
        }
        formData.append('cat_cover_image', catCoverImage), editFlag = true
    }

    if (editFlag === true) {
        fetch(`/admin/api/category/edit/${catId}`, {method: 'PATCH', headers: {Authorization: 'Bearer ' + localStorage.getItem('access_token')}, body: formData})
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
        alert('please enter any value for edit category')
    }
})

document.addEventListener('DOMContentLoaded', function () {
    getCategoryData()
})

