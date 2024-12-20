
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

// el dato es Decimal si tiene punto decimal y luego 2 decimales
var isDecimal = function (value) {
    // console.log(value)
    if (value.toString().split(".").length === 2) {
        if (value.toString().split(".")[1].length === 2) {
            return true;
        }
    }
    return false;
};

var vbuttons = function () {
    let temp = [
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
    return temp
}
// configuramos columnDefs dependiendo de si recibimos o no el parámetro ibuttons
var columnDefs = function (ibuttons) {
    let temp = []
    //configuramos la columna 0 correspondiente a las Acciones
    let col0 = {
        targets: 0,
        class: 'text-center',
        orderable: false,
        render: function (data, type, row) {
            var buttons = ibuttons.replaceAll('rowid', row.id);
            return buttons;
        },
    }
    let coln =
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
                    } else if ($.isNumeric(data) && isDecimal(data)) {
                        data = data.replace('.', ',');   // en los decimal cambiamos punto por coma
                        data = '<div style="text-align: right">' + data + '</div>'; // alineamos a la derecha por las comas
                    }
                }
                return data;
            }
        }
    if (ibuttons) {
        temp.push(col0)
    }
    temp.push(coln)
    return temp
}

// inicializa datatable con paginación en cliente
function initdtables(icolumns, ibuttons, iorder, extrabuttons) {

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
                'action': 'searchdata_c',
            },
            headers: {
                'X-CSRFToken': csrftoken
            },
            dataSrc: ""
        },
        columns: icolumns,
        order: iorder,
        columnDefs: columnDefs(ibuttons),
        language: {
            decimal: ",",
            // url: "{% static 'I18N/es_es.json' %}"
            url: "/static/i18N/es_es.json",
        },

        initComplete: function (settings, json) {
            var api = this.api();
            new $.fn.dataTable.Buttons(api, {
                buttons: vbuttons()
            });
            api.buttons().container().appendTo('#dt-buttons');
        }
    });
}
// valicación de formularios
function validar(entity) {
    console.log(entity)
    switch (entity) {
        case 'Importar':
            rules = {
                fichero_tabla: {required: true},
            }
            break
        case 'Descuento MO':
            rules = {descuento: {number: true, min: 0, max: 100}}
            break
        case 'Forma de Pago':
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
        case 'Artículo':
            rules = {
                unidadCompra: {number: true, min: 0, step: 1},
                unidadVenta: {number: true, min: 0, step: 1},
                unidadStock: {number: true, min: 0, step: 1},
                multiplo: {number: true, min: 0, step: 1},
                consumoMedio: {number: true, min: 0, step: 1},
                tarifa: {number: true, min: 0.01},
            }
            break
        case 'Línea Entrada Almacén':
            rules = {
                cantidad: {number: true, step: 1},
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
    // console.log(err)
    Swal.fire({
        icon: 'error',
        title: 'Comprueba estos errores',
        html: err,
        // text: err,
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
        }).then((result) => {
            if (result.isConfirmed) {
                form.submit();
            }
        })
    });
}
// inicializa datatable con paginación en servidor
function initdtableserver(icolumns, ibuttons, iorder, extrabuttons, tipo_) {
    // console.log(extrabuttons)
    // console.log(tipo_)
    var table = $('#dtable-buttons').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        stateSave: true,
        serverSide: true,  //Paginación por servidor
        processing: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata_s',
                'tipo_': tipo_,
            },
            headers: {
                'X-CSRFToken': csrftoken
            },
            dataSrc: "data"
        },
        columns: icolumns,
        order: iorder,
        columnDefs: columnDefs(ibuttons),
        language: {
            decimal: ",",
            // url: "{% static 'I18N/es_es.json' %}"
            url: "/static/i18N/es_es.json",
        },

        initComplete: function (settings, json) {
            if (extrabuttons) {
                var api = this.api();
                new $.fn.dataTable.Buttons(api, {
                    buttons: vbuttons()
                });
                api.buttons().container().appendTo('#dt-buttons');
            }
        }
    });
    return table;

}

// inicializa datatable con paginación en servidor
function initdtableoper() {
    var table = $('#dtoperario').DataTable({
        searching: false,     // Search Box will Be Disabled
        ordering: false,      // Ordering (Sorting on Each Column)will Be Disabled
        info: false,          // Not show "1 to n of n entries" Text at bottom
        lengthChange: false,  // Will Disabled Record number per page
        bPaginate: false,     // Paginate buttons disabled
        responsive: true,
        columnDefs: [{
            targets: [0, 4],
            className: 'bolded',
        },
        ]
    });
    return table;
}

// acciones comunes asociadas a las líneas de movimiento
function lineaMovimiento(movimiento, action, list_url) {
    console.log(movimiento);
    console.log(action);
    console.log(list_url);
    var id_movimiento = '#id_'.concat(movimiento);
    $(id_movimiento).select2({
        theme: 'bootstrap4',
        language: 'es',
        minimumInputLength: 1,
        ajax: {
            url: window.location.pathname,
            dataType: 'json',
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: function (params) {
                var query = {
                    'term': params.term,
                    'action2': 'select2',
                    'tipo_': 'formbase',
                    'field': movimiento,
                }
                return query;
            },
            processResults: function (data) {
                return {
                    results: $.map(data, function (item) {
                        return {id: item.id, text: item.text};
                    })
                };
            },
        }
    });
    $('#id_referencia').select2({
        theme: 'bootstrap4',
        language: 'es',
        placeholder: 'Seleccione una referencia',
        minimumInputLength: 1,
        allowClear: true,
        ajax: {
            url: window.location.pathname,
            dataType: 'json',
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: function (params) {
                var query = {
                    'term': params.term,
                    'action2': 'select2',
                    'tipo_': 'formbase',
                    'field': 'referencia',
                }
                return query;
            },
            processResults: function (data) {
                return {
                    results: $.map(data, function (item) {
                        return {id: item.id, text: item.text};
                    })
                };
            },
        }
    });
    $('#id_referencia').on('select2:select', function (e) {
        var data = e.params.data;
        var refid = data.id
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action2': 'referdata',
                'tipo_': 'formbase',
                'refid': refid,
            },
            headers: {
                'X-CSRFToken': csrftoken
            },
            dataType: 'json',
        }).done(function (data) {
            if (data.hasOwnProperty('error')) {
                senderror(data.error)
            } else {
                // Recuperamos el % descuento del literal con formato 'cod - cod - dto%'
                var arrdto = data.codigoApro.split('-');
                var dto = arrdto[2].substring(1, arrdto[2].length - 1)
                $('input[name="existencias"]').val(data.existencias).change();
                $('input[name="ubicacion"]').val(data.ubicacion).change();
                $('input[name="codigoApro"]').val(data.codigoApro).change();
                $('input[name="codigoUrgte"]').val(data.codigoUrgte).change();
                $('input[name="codigoObsoleto"]').val(data.codigoObsoleto).change();
                $('input[name="tarifa"]').val(data.tarifa).change();
                $('input[name="precioCoste"]').val(data.precioCoste).change();
                $('input[name="precioCosteMedio"]').val(data.precioCosteMedio).change();
                $('input[name="pedidosPendientes"]').val(data.pedidosPendientes).change();
                $('input[name="reserva"]').val(data.reserva).change();
                $('input[name="familia"]').val(data.familia).change();
                $('input[name="precioCompra"]').val(data.tarifa).change();
                $('input[name="descuento"]').val(dto).change();

                if (data.sustituida) {
                    $('select[name="referencia"]').val(data.referencia.id).change();
                    sendmessage('Referencia sustituida')
                }
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {
        });
    });
    $('#btn_cancelar').on('click', function (e) {
        // cancelar en un alta puede provocar que se borre el movimiento si no hay más líneas
        e.preventDefault()
        if (action === 'add') {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action2': 'canceladd',
                    'tipo_': 'formbase',
                },
                headers: {
                    'X-CSRFToken': csrftoken
                },
                dataType: 'json',
            }).done(function (data) {
                if (data.hasOwnProperty('error')) {
                    senderror(data.error)
                } else {
                    window.location.href = data.url
                }
            }).fail(function (jqXHR, textStatus, errorThrown) {
                alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {
            });
        } else {
            // si no es un alta seguimos con el Cancelar
            window.location.href = list_url
        }
    });
}
