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