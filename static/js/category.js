const pageNoAndFlagObj = {pageNo: 1, scrollFlag: false}

function getCategoryData() {
    fetch(`/admin/api/category/${catId}`, {method: 'GET', headers: {Authorization: 'Bearer ' + localStorage.getItem('access_token')}})
    .then(response => response.json())
    .then(body => {
        if (body.detail) {
            localStorage.removeItem('access_token')
            window.location.href = '/admin/login'
        }

        if (body.success) {
            document.querySelector('#catNameId').innerHTML = body.data.cat_name
            document.querySelector('#catSubTitleId').innerHTML = body.data.cat_sub_title
            forScrollerSet(pageNoAndFlagObj, getCategoryImages, '#categoryImagesGridId')
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
    getCategoryData()
})

