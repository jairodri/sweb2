//
// function validar(entity) {
//     // console.log(entity)
//     switch (entity) {
//         case 'DescuentoMO':
//             rules = {descuento: {number: true, min: 0, max: 100}}
//             break
//         case 'FormaDePago':
//             rules = {
//                 recibos: {number: true},
//                 diasvto: {number: true}
//             }
//             break
//         case 'Banco':
//             rules = {
//                 telefono: {number: true},
//                 telperso: {number: true},
//                 extension: {number: true}
//             }
//             break
//         // case 'Login':
//         //     rules = {
//         //         username: {required: true},
//         //         password: {required: true}
//         //     }
//         //     break
//         default:
//             rules = {}
//     }
//     $('#idform').validate({
//         rules: rules,
//         messages: {},
//         errorElement: 'span',
//         errorPlacement: function (error, element) {
//             error.addClass('invalid-feedback');
//             element.closest('.form-group').append(error);
//         },
//         highlight: function (element, errorClass, validClass) {
//             $(element).addClass('is-invalid');
//         },
//         unhighlight: function (element, errorClass, validClass) {
//             $(element).removeClass('is-invalid');
//         }
//     });
// }

// function message_error(obj) {
//     var html = '';
//     if (typeof (obj) === 'object') {
//         html = '<ul style="text-align: left;">';
//         $.each(obj, function (key, value) {
//             html += '<li>' + key + ': ' + value + '</li>';
//         });
//         html += '</ul>';
//     } else {
//         html = '<p>' + obj + '</p>';
//     }
//     Swal.fire({
//         title: 'Error!',
//         html: html,
//         icon: 'error'
//     });
// }

// function submit_with_ajax(url, title, content, parameters, callback) {
//     $.confirm({
//         theme: 'material',
//         title: title,
//         icon: 'fa fa-info',
//         content: content,
//         columnClass: 'small',
//         typeAnimated: true,
//         cancelButtonClass: 'btn-primary',
//         draggable: true,
//         dragWindowBorder: false,
//         buttons: {
//             info: {
//                 text: "Si",
//                 btnClass: 'btn-primary',
//                 action: function () {
//                     $.ajax({
//                         url: url, //window.location.pathname
//                         type: 'POST',
//                         data: parameters,
//                         dataType: 'json',
//                     }).done(function (data) {
//                         console.log(data);
//                         if (!data.hasOwnProperty('error')) {
//                             callback();
//                             return false;
//                         }
//                         message_error(data.error);
//                     }).fail(function (jqXHR, textStatus, errorThrown) {
//                         alert(textStatus + ': ' + errorThrown);
//                     }).always(function (data) {
//
//                     });
//                 }
//             },
//             danger: {
//                 text: "No",
//                 btnClass: 'btn-red',
//                 action: function () {
//
//                 }
//             },
//         }
//     })
// }