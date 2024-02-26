if (! localStorage.getItem('access_token')) {
    window.location.href = '/admin/login'
}

function forScrollerSet(pageNoAndFlagObj, callbackFunc, divIdStr) {
    callbackFunc()
    infiniteScroll(pageNoAndFlagObj, callbackFunc, divIdStr)
}

function logout() {
    localStorage.removeItem('access_token')
    window.location.href = '/admin/login'
}

function infiniteScroll(pageNoAndFlagObj, callbackFunc, divIdStr) {
    window.addEventListener('scroll', function() {
        if (window.scrollY + window.innerHeight >= document.querySelector(divIdStr).scrollHeight) {
            if(pageNoAndFlagObj.scrollFlag == false) {
                pageNoAndFlagObj.scrollFlag = true
                pageNoAndFlagObj.pageNo += 1
                callbackFunc()
            }
        }
    })
}
