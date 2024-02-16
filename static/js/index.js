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
                htmlStr += `<div class="col-lg mb-3">
                                    <div class="card category-card">
                                            <a href="/admin/category/${categoryObj.cat_id}" class="text-decoration-none">
                                                <div class="card-img">
                                                    <img src="/${categoryObj.cat_cover_image}" class="card-img-top" alt="...">
                                                </div>
                                                <div class="card-body">
                                                    <h5 class="card-title">${categoryObj.cat_name}</h5>
                                                    <p title="${categoryObj.cat_sub_title}" class="card-text">${categoryObj.cat_sub_title}</p>
                                                <button  <span> Active </span></button>
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
})
