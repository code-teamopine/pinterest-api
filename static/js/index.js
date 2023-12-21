const pageNoAndFlagObj = {pageNo: 1, scrollFlag: false}

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
                htmlStr += `<div class="col">
                                <div class="card" style="width: 18rem;">
                                    <a href="/admin/category/${categoryObj.cat_id}" class="text-decoration-none">
                                        <img src="/${categoryObj.cat_cover_image}" class="card-img-top" alt="...">
                                        <div class="card-body">
                                            <h5 class="card-title">${categoryObj.cat_name}</h5>
                                            <p class="card-text">${categoryObj.cat_sub_title}</p>
                                            <span>Active </span><i class="${categoryObj.cat_is_active ? "bi bi-check-circle" : "bi bi-x-circle"}"></i>
                                        </div>
                                    </a>
                                </div>
                            </div>`
            })
            document.querySelector('#categoryGridDivId').innerHTML += htmlStr
            pageNoAndFlagObj.scrollFlag = false
        }
        else {
            alert(body.msg)
        }
    })
}

document.addEventListener('DOMContentLoaded', function () {
    forScrollerSet(pageNoAndFlagObj, getCategory, '#categoryGridDivId')
})
