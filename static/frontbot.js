function logout(){
    console.log('logout');
    fetch('/auth/logout', {
        method: 'POST',
        redirect: 'manual'
    }).then(res => {
        if (res.ok) {
            window.location.href = '/auth/login'
        } else {
            console.log('logout failed')
        }
    });
}

function init(){
    // logout button
    document.getElementById('logout-btn').addEventListener('click', e => {
        logout()
    })
}

// init();