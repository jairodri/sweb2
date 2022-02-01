// inicializa datatable
function initdtables(icolumns, ibuttons) {
    var table = $('#dtable-buttons').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata',
                // {#'csrf_token':$('meta[name="csrf_token"]').attr("content")#}
            },
            dataSrc: ""
        },
        columns: icolumns,
        order: [[1, 'asc']],
        columnDefs: [
            // {#{orderable: false, targets: [0]}#}
            {
                targets: [0],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = ibuttons.replaceAll('rowid', row.id)
                    return buttons;
                }
            },
        ],
        language: {
            // url: "{% static 'I18N/es_es.json' %}"
            url: "/static/I18N/es_es.json"
        },

        initComplete: function (settings, json) {
            var api = this.api();

            new $.fn.dataTable.Buttons(api, {
                buttons: [
                    {
                        extend: "csv",
                        className: "btn-sm",
                        exportOptions: {
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
                telefono: {number: true},
                telperso: {number: true},
                extension: {number: true}
            }
            break
        // case 'Login':
        //     rules = {
        //         username: {required: true},
        //         password: {required: true}
        //     }
        //     break
        default:
            rules = {}
    }
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