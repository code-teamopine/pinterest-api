const pageNoAndFlagObj = {pageNo: 1, scrollFlag: false}

function getCategoryData() {
    fetch(`/admin/api/category/${catId}`, {method: 'GET', headers: {Authorization: 'Bearer ' + localStorage.getItem('access_token')}})
    .then(response => response.json())
    .then(body => {
        if (body.detail) {
            localStorage.removeItem('access_token')
            window.location.href = '/admin/login'
        }

        if (body.success === true) {
            document.querySelector('#catNameId').innerHTML = body.data.cat_name
            document.querySelector('#catSubTitleId').innerHTML = body.data.cat_sub_title
            forScrollerSet(pageNoAndFlagObj, getCategoryImages, '#categoryImagesGridId')
        }
        else {
            alert(body.msg)
        }
    })
}

function getCategoryImages() {
    fetch(`/admin/api/category/${catId}/images?page_no=${pageNoAndFlagObj.pageNo}`, {method: 'GET', headers: {Authorization: 'Bearer ' + localStorage.getItem('access_token')}})
    .then(response => response.json())
    .then(body => {
        if (body.detail) {
            localStorage.removeItem('access_token')
            window.location.href = '/admin/login'
        }
        if (body.success === true) {
            let htmlStr = ``
            body.data.forEach(imgObj => {
                htmlStr += `<div class="col">
                                <div class="card" style="width: 18rem;">
                                    <img src="/${imgObj.img_file}" class="card-img-top" alt="...">
                                    <div class="card-body">
                                        <a class="btn btn-warning btn-sm" href="/admin/image/edit/${imgObj.img_id}">Edit</a>
                                        <span>Active - <i class="${imgObj.img_is_active ? "bi bi-check-circle" : "bi bi-x-circle"}"></i></span>
                                    </div>
                                </div>
                            </div>`
            })
            document.querySelector('#categoryImagesGridId').innerHTML += htmlStr
            pageNoAndFlagObj.scrollFlag = false
        }
        else {
            alert(body.msg)
        }
    })
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#editCategoryBtnId').href = `/admin/category/edit/${catId}`
    getCategoryData()
})

