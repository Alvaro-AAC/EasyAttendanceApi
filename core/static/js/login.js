function getCSRF() {
    var cookies_array = document.cookie.split(';');
    var cookies_dict = [];
    var csrftoken;
    cookies_array.forEach(elem => {
        var temp = elem.split('=');
        cookies_dict.push({
            key: temp[0],
            value: temp[1]
        });
    });
    cookies_dict.forEach(elem => {
        if(elem.key.trim() == 'csrftoken') {
            csrftoken = elem.value;
        }
    });
    return csrftoken;
}

$(document).ready(() => {
    let csrftoken = getCSRF();
    $('#inisess').click(() => {
        let user = $('#usuario').val();
        let password = $('#contrasena').val();
        $.ajax({
            url: '/verifyLogin/',
            type: 'POST',
            headers: {"X-CSRFToken": csrftoken},
            data: `csrftoken=${csrftoken}&user=${user}&pwd=${password}`,
            success: data => {
                if(data.status === 'success') {
                    let swalModal = Swal.fire({
                        title: '<strong>Sesión iniciada</strong>',
                        icon: 'success',
                        backdrop: false,
                        allowEscapeKey: false,
                        allowEnterKey: false,
                        confirmButtonText: 'Aceptar',
                    });

                    swalModal.then(elem => {
                        if(elem.isConfirmed) {
                            window.location.replace('/clases/');
                        }
                    });
                } else if (data.status === 'dataerror') {
                    Swal.fire({
                        title: '<strong>Usuario o contraseña incorrecto</strong>',
                        icon: 'error',
                        confirmButtonText: 'Aceptar',
                    });
                } else {
                    Swal.fire({
                        title: '<strong>Se ha producido un error</strong>',
                        icon: 'error',
                        confirmButtonText: 'Aceptar',
                    });
                }
            },
            error : data => {
                console.log(data);
            }
        });
    });

    $('#loginform').submit(e => {
        e.preventDefault();
        $('#inisess').trigger('click');
    });
});