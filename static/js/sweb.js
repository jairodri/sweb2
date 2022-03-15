function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// inicializa datatable
function initdtables(icolumns, ibuttons) {
    var table = $('#dtable-buttons').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        stateSave: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata',
            },
            headers: {
                'X-CSRFToken': csrftoken
            },
            dataSrc: ""
        },
        columns: icolumns,
        // Gestionamos el ordenamiento en models
        // order: [[1, 'asc']],
        columnDefs: [
            // La columna 0 es la de las Acciones, donde van los botones
            {
                targets: [0],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = ibuttons.replaceAll('rowid', row.id)
                    return buttons;
                }
            },
            // Tenemos que gestionar los booleans de manera diferente
            {
                targets: '_all',
                render: function (data, type, row) {
                    if (type === 'exportpdf' || type === 'exportxls' || type === 'exportcsv') {
                        if (data === true) {
                            data = 'Si'
                        } else if (data === false) {
                            data = 'No'
                        }
                    } else {
                        if (data === true) {
                            data = '<input type="checkbox" class="checkbox" checked  />'
                        } else if (data === false) {
                            data = '<input type="checkbox" class="checkbox"  />'
                        }
                    }
                    return data;
                }
            },
        ],
        language: {
            // url: "{% static 'I18N/es_es.json' %}"
            url: "/static/i18N/es_es.json"
        },

        initComplete: function (settings, json) {
            var api = this.api();

            new $.fn.dataTable.Buttons(api, {
                buttons: [
                    {
                        extend: "csv",
                        className: "btn-sm",
                        exportOptions: {
                            orthogonal: 'exportcsv',
                            columns: function (idx, data, node) {
                                if (node.innerHTML == "Acciones")
                                    return false;
                                return true;
                            }
                        },
                    },
                    {
                        extend: "excel",
                        className: "btn-sm",
                        exportOptions: {
                            orthogonal: 'exportxls',
                            columns: function (idx, data, node) {
                                if (node.innerHTML == "Acciones")
                                    return false;
                                return true;
                            }
                        },
                    },
                    {
                        extend: "pdfHtml5",
                        className: "btn-sm",
                        exportOptions: {
                            orthogonal: 'exportpdf',
                            columns: function (idx, data, node) {
                                if (node.innerHTML == "Acciones")
                                    return false;
                                return true;
                            }
                        },
                    }
                ]
            });
            api.buttons().container().appendTo('#dt-buttons');
        }
    });
}
// valicación de formularios
function validar(entity) {
    // console.log(entity)
    switch (entity) {
        case 'Importar':
            rules = {
                fichero_tabla: {required: true},
            }
            break
        case 'DescuentoMO':
            rules = {descuento: {number: true, min: 0, max: 100}}
            break
        case 'FormaDePago':
            rules = {
                recibos: {number: true},
                diasvto: {number: true}
            }
            break
        case 'Banco':
            rules = {
                telefono: {number: true}, // está definido como numérico en bbdd
                telperso: {number: true},
                extension: {number: true}
            }
            break
        case 'Login':
            rules = {
                username: {required: true},
                password: {required: true}
            }
            break
        case 'Cliente':
            rules = {
                diaPagoDesde: {number: true, min: 1, max: 31},
                diaPagoHasta: {number: true, min: 1, max: 31},
                dtoEpecial: {number: true, min: 0, max: 100},
                ivaEpecial: {number: true, min: 0, max: 100},
                precioMo: {number: true, max: 999.99},
                // telefono: {number: true},
                // tlfmovil: {number: true},
            }
            break
        default:
            rules = {}
    }
    // console.log(rules)
    $('#idform').validate({
        rules: rules,
        messages: {},
        errorElement: 'span',
        errorPlacement: function (error, element) {
            error.addClass('invalid-feedback');
            element.closest('.form-group').append(error);
        },
        highlight: function (element, errorClass, validClass) {
            $(element).addClass('is-invalid');
        },
        unhighlight: function (element, errorClass, validClass) {
            $(element).removeClass('is-invalid');
        }
    });
}

function sendmessage(msg) {
    Swal.fire({
        icon: 'success',
        titleText: msg,
        backdrop: true,
        footer: '<b>Srio</b>Web',
        toast: true,
        position: 'center',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: false
    });
}

function senderror(err) {
    Swal.fire({
        icon: 'error',
        title: 'Comprueba estos errores',
        text: err,
        backdrop: true,
        footer: '<b>Srio</b>Web',
        // toast: true,
        position: 'center',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: false
    });
}

function confirmdelete() {
    $('#idform').on('submit', function (e) {
        var form = this;
        e.preventDefault();
        Swal.fire({
            title: 'Se va a borrar este registro',
            text: '¿Estás seguro?',
            icon: 'warning',
            backdrop: true,
            footer: '<b>Srio</b>Web',
            // toast: true,
            // position: 'center',
            showCancelButton: true,
            confirmButtonText: 'Borrar',
            cancelButtonText: 'Cancelar',
            allowOutsideClick: false,
            allowEscapeKey: false,
            // customClass: {
            //     container: 'container-class',
            //     popup: 'popup-class',
            //     header: 'header-class',
            //     title: 'title-class',
            //     closeButton: 'close-button-class',
            //     icon: 'icon-class',
            //     image: 'image-class',
            //     content: 'content-class',
            //     input: 'input-class',
            //     actions: 'actions-class',
            //     confirmButton: 'confirm-button-class',
            //     cancelButton: 'cancel-button-class',
            //     footer: 'footer-class'
            // }
        }).then((result) => {
            if (result.isConfirmed) {
                form.submit();
            }
        })
    });
}