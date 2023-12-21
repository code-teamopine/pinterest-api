document.querySelector('#loginFormId').addEventListener("submit", (e) => {
    e.preventDefault()
    const username = e.target.elements['usernameInput'].value
    const password = e.target.elements['passwordInput'].value

    if (! username) {
        alert('Username is required.')
        return false
    }
    if (! password) {
        alert('Password is required.')
        return false
    }

    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)

    fetch(`/admin/api/login`, {method: 'POST', body: formData})
    .then(response => response.json())
    .then(body => {
        if (body.success) {
            localStorage.setItem('access_token', body.token)
            window.location.href = '/admin/'
        }
        else {
            alert(body.detail)
            return false
        }
    })
})
