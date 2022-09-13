var input;
var claseId;

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

function back() {
    window.location.replace('/logout/');
}

function abrirModal(e) {
    var qrDom = $('#QrAsistencia')[0]; 
    qrDom.src = '';
    qrDom.height = 0;
    qrDom.width = 0;
    $('#AsistenciaModal').modal('toggle');
    claseId = e.id;
    $.get(`/api/v1/lista_asistencia/${claseId}/?format=json`, data => {
        var presente;
        var color;
        $('#tablaAsistencia')[0].innerHTML = '';
        data.data.forEach(elem => {
            var ramo = '';
            var fecha = elem['clase_id']['fecha'];
            ramo += elem['clase_id']['seccion_id']['ramo_id']['codigo_letra'];
            ramo += elem['clase_id']['seccion_id']['ramo_id']['codigo_numero'];
            ramo += ' - ';
            ramo += elem['clase_id']['seccion_id']['codigo_seccion'];
            ramo += elem['clase_id']['seccion_id']['tipo'];
            if(elem['presente']) {
                presente = 'Presente';
                color = 'success';
            } else {
                presente = '&nbsp;Ausente';
                color = 'danger';
            }
            $('#AsistenciaModalLabel')[0].innerHTML = `
                Asistencia clase: ${ramo} <br>Fecha: ${fecha}
            `;
            $('#tablaAsistencia')[0].innerHTML += `
                <tr class="text-center">
                <td class="pb-3">${elem['alumno_id']['nombre']} ${elem['alumno_id']['apellido']}<td>
                <td class="pb-3">&nbsp;&nbsp;&nbsp;</td>
                <td class='bg-${color} d-inline rounded p-1'>${presente}</td>
                </tr>
                `;
        });
    });
}

function reloadPage() {
    window.location.reload();
}

async function generarQr() {
    var tokenClase;
    tokenClase = generarTokenClase(claseId)
    new QRious({
        element: $('#QrAsistencia')[0],
        value: `${await tokenClase}`,
        size: 200,
        foreground: 'black',
        level: 'H'
    });
}

async function generarTokenClase(id) {
    var token;
    var csrftoken;
    csrftoken = getCSRF();
    await $.ajax({
        url: '/api/v1/generar_codigo_clase/',
        type: 'POST',
        headers: {"X-CSRFToken": csrftoken},
        data: `csrftoken=${csrftoken}&id=${id}`,
        success: function(data) {
            if(data.status === 'success') {
                token = data['data']['token'].slice();
            } else {
                console.log(data);
            }
        },
        error : function(data) {
            console.log(data);
        }
    });
    return token;
}

function modalClase() {
    $('#Modalclase').modal('toggle');
}

function borrarClase() {
    let swalConfirm = Swal.fire({
        title: '<strong>¿Desea borrar la clase seleccionada?</strong>',
        icon: 'question',
        backdrop: false,
        allowEscapeKey: false,
        allowEnterKey: false,
        showCancelButton: true,
        cancelButtonText: 'Cancelar',
        confirmButtonText: 'Aceptar',
        reverseButtons: true,
    });

    swalConfirm.then(elem => {
        if(elem.isConfirmed) {
            let csrftoken = getCSRF();
            $.ajax({
                url: '/api/v1/delclase/',
                type: 'POST',
                headers: {"X-CSRFToken": csrftoken},
                data: `csrftoken=${csrftoken}&id=${claseId}`,
                success: function(data) {
                    if(data.status === 'success') {
                        $('#ramoselect').trigger('change');
                        $('#AsistenciaModal').modal('hide');
                    } else {
                        console.log(data);
                    }
                },
                error : function(data) {
                    console.log(data);
                }
            });
        } else if(elem.isDismissed) {
            console.log('dismiss');
        }
    });
}

$(document).ready(function() {
    $('#selectramo').change(function() {
        $('#selectseccion').removeAttr('disabled');
        $.get(`/api/v1/secciones/${$('#selectramo').val()}/${$('#hiddenprofid').val()}/`)
        .then(elem => {
            if(elem.status === 'success') {
                $('#selectseccion')[0].innerHTML = `<option selected="" disabled="disabled">Secciones</option>`
                elem.data.forEach(seccion => {
                    $('#selectseccion')[0].innerHTML += `
                        <option value="${seccion.pk}">${seccion.codigo_seccion}${seccion.tipo}</option>
                    `;
                });
            }
        });
    });

    $('#ramoselect').change(() => {
        $.get(`/api/v1/clases/${$('#ramoselect').val()}/`)
        .then(elem => {
            if(elem.status === 'success') {
                $('#tablebody')[0].innerHTML = '';
                elem.data.forEach(clase => {
                    let letra = clase.seccion_id.ramo_id.codigo_letra;
                    let num = clase.seccion_id.ramo_id.codigo_numero;
                    let seccion = clase.seccion_id.codigo_seccion + clase.seccion_id.tipo;
                    let td1 = `${letra}${num}-${seccion}`;
                    let td2 = `${clase.fecha}`;
                    $('#tablebody')[0].innerHTML += `
                    <tr>
                        <td>${td1}</td>
                        <td>${td2}</td>
                        <td><button class="btn btn-primary" id="${clase.clase_id}" onclick="abrirModal(this)">Ver</button></td>
                    </tr>
                    `;
                });
            }
        });
    });

    $('#formmodal').submit(e => {
        e.preventDefault();
        let id = $('#formmodal')[0].selectseccion.value;
        let form = $('#formmodal').serialize()
        $.ajax({
            url: '/crearclase/',
            type: 'POST',
            data: form,
            success: data => {
                if(data.status === 'success') {
                    $('#ramoselect').val(id);
                    $('#ramoselect').trigger('change');
                    $('#Modalclase').modal('hide');
                } else {
                    console.log(data);
                }
            }
        });
    });
});