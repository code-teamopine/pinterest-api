document.querySelector('#addCategoryFormId').addEventListener("submit", (e) => {
    e.preventDefault()
    const catName = e.target.elements['catNameInput'].value
    const catSubTitle = e.target.elements['catSubTitleInput'].value
    const catCoverImage = e.target.elements['catCoverImageInput'].files[0]
    const catIsActive = e.target.elements['catIsActiveCheckBox'].checked
    
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
