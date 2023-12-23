document.querySelector('#selectMobileViewDevice').addEventListener('change', (e) => {
    const iPhoneDevicesObj = {
        iphone14ProMax15Plus15ProMax : {iphoneMocup: {height: '932px', width: '430px'}, iphoneInnerBorder: {height: '912px', width: '410px'}},
        iphone14Pro1515Pro: {iphoneMocup: {height: '852px', width: '393px'}, iphoneInnerBorder: {height: '832px', width: '373px'}},
        iphone12ProMax14Plus: {iphoneMocup: {height: '926px', width: '428px'}, iphoneInnerBorder: {height: '906px', width: '408px'}},
        iphone1212Pro1313Pro14: {iphoneMocup: {height: '844px', width: '390px'}, iphoneInnerBorder: {height: '824px', width: '370px'}},
        iphoneX11Pro12Mini13Mini: {iphoneMocup: {height: '812px', width: '375px'}, iphoneInnerBorder: {height: '792px', width: '355px'}},
        iphoneXR1111ProMax: {iphoneMocup: {height: '896px', width: '414px'}, iphoneInnerBorder: {height: '876px', width: '394px'}},
        iphoneSE2nd3rdGen: {iphoneMocup: {height: '666px', width: '375px'}, iphoneInnerBorder: {height: '742px', width: '355px'}}
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
            document.querySelector('#imgImgId').src = '/' + body.data.img_file  
        }
        else {
            console.log(body.msg)
            window.location.href = '/admin/'
        }
    })
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#editImgBtnId').href = `/admin/image/edit/${imgId}`
    getImageData()
})
