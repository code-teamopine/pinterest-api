const imageApiObj = {imgIsActive: '', imgCatId: '', imgCatName: ''}

document.querySelector('#selectMobileViewDevice').addEventListener('change', (e) => {
    const iPhoneDevicesObj = {
        iphone14ProMax15Plus15ProMax : {iphoneMocup: {height: '932px', width: '430px'}, iphoneInnerBorder: {height: '912px', width: '410px'}},
        iphone14Pro1515Pro: {iphoneMocup: {height: '852px', width: '393px'}, iphoneInnerBorder: {height: '832px', width: '373px'}},
        iphone12ProMax14Plus: {iphoneMocup: {height: '926px', width: '428px'}, iphoneInnerBorder: {height: '906px', width: '408px'}},
        iphone1212Pro1313Pro14: {iphoneMocup: {height: '844px', width: '390px'}, iphoneInnerBorder: {height: '824px', width: '370px'}},
        iphoneX11Pro12Mini13Mini: {iphoneMocup: {height: '812px', width: '375px'}, iphoneInnerBorder: {height: '792px', width: '355px'}},
        iphoneXR1111ProMax: {iphoneMocup: {height: '896px', width: '414px'}, iphoneInnerBorder: {height: '876px', width: '394px'}},
        iphoneSE2nd3rdGen: {iphoneMocup: {height: '568px', width: '320px'}, iphoneInnerBorder: {height: '548px', width: '300px'}}
    }

    document.querySelector('.iphone-mocup').style.height = iPhoneDevicesObj[e.target.value].iphoneMocup.height, document.querySelector('.iphone-mocup').style.width = iPhoneDevicesObj[e.target.value].iphoneMocup.width
    document.querySelector('.iphone-inner-border').style.height = document.querySelector('.img-div').style.height = iPhoneDevicesObj[e.target.value].iphoneInnerBorder.height, document.querySelector('.iphone-inner-border').style.width = document.querySelector('.img-div').style.width = iPhoneDevicesObj[e.target.value].iphoneInnerBorder.width
})

function getImageData() {
    fetch(`/admin/api/image/${imgId}`, {method: 'GET', headers: {Authorization: 'Bearer ' + localStorage.getItem('access_token')}})
    .then(response => response.json())
    .then(body => {
        if (body.detail) {
            localStorage.removeItem('access_token')
            window.location.href = '/admin/login'
        }
        if (body.success === true) {
            imageApiObj.imgIsActive = Boolean(body.data.img_is_active), imageApiObj.imgCatId = body.data.cat_id, imageApiObj.imgCatName = body.data.cat_name
            document.querySelector('#imgImgId').src = document.querySelector('#editImgId').src = '/' + body.data.img_file, document.querySelector('#catNameSelect').innerHTML = `<option value="${body.data.cat_id}" selected>${body.data.cat_name}</option>`, document.querySelector('#imageIsActiveCheckBox').checked = Boolean(body.data.img_is_active)
            categorySelect2()
        }
        else {
            console.log(body.msg)
            window.location.href = '/admin/'
        }
    })
}

function categorySelect2() {
    $('#catNameSelect').select2({
        placeholder: "Select Category",
        dropdownParent: $('#editImageModal'),
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
                window.location.href = `/admin/image/${imgId}`
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
    document.querySelector('#editImgBtnId').href = `/admin/image/edit/${imgId}`
    getImageData()
})
