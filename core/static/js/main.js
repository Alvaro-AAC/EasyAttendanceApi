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
    // TODO: Volver al login
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
        value: `${await tokenClase}`, // Definir token !
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
$(document).ready(function() {
    $('#selectramo').change(function() {
        $('#selectseccion').removeAttr('disabled');

    });
});
