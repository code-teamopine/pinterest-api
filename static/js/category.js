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
            console.log(body.msg)
            window.location.href = `/admin/`
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
                htmlStr += `<div class="col-lg mb-3">
                                <div class="card" >
                                    <a href="/admin/image/${imgObj.img_id}">
                                    <div class="card-img">
                                        <img src="/${imgObj.img_file}" class="card-img-top" alt="...">
                                    </div>
                                        <div class="card-body text-center">
                                            <button class="${imgObj.img_is_active ? "activeBtn" : "inactiveBtn"}">  <span> ${imgObj.img_is_active ? "Active" : "Inactive" }</span></button> 
                                        </div>
                                    </a>
                                </div>
                            </div>`
            })
            document.querySelector('#categoryImagesGridId').innerHTML += htmlStr
            pageNoAndFlagObj.scrollFlag = false
        }
        else {
            console.log(body.msg)
        }
    })
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#editCategoryBtnId').href = `/admin/category/edit/${catId}`
    getCategoryData()
})

