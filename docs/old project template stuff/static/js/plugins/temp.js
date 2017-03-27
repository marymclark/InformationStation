
        $(function() {
            var _alert = '{{ alert }}';
            var _icon;
            var _title;
            var _type = '{{ alert_code }}';
            if (_type == null) {
                _type = 'info';
            }
            if (_alert != null) {
                    console.log("Alert ( " + _type + " ) :" + _alert);
                    if (_type == 'success') {
                        _icon = 'fa fa-thumbs-up';
                        _title = 'Success';
                    }
                    else if (_type == 'warning') {
                        _icon = 'fa fa-exclamation';
                        _title = 'Warning';
                    }
                    else if (_type == 'error') {
                        _icon = 'fa fa-warning';
                        _title = 'Error';
                    }
                    else {
                        _icon = 'fa fa-exclamation';
                        _title = 'Note';
                    }
                    $.notify({
                        icon : _icon,
                        title : _title,
                        message : _alert,
                        target: '_blank'
                        },{
                        element: 'body',
                        position: null,
                        type: _type,
                        allow_dismiss: true,
                        newest_on_top: false,
                        showProgressbar: false,
                        placement: {
                            from: "bottom",
                            align: "left"
                        },
                        offset: 20,
                        spacing: 10,
                        z_index: 1000,
                        delay: 5000,
                        timer: 4000,
                        url_target: '_blank',
                        mouse_over: null,
                        animate: {
                            enter: 'animated fadeInDown',
                            exit: 'animated fadeOutUp'
                        },
                        onShow: null,
                        onShown: null,
                        onClose: null,
                        onClosed: null,
                        icon_type: 'class',
                        template:   '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
                                        '<button type="button" aria-hidden="true" class="close" data-notify="dismiss">×</button>' +
                                        '<span data-notify="icon"></span> ' +
                                        '<span data-notify="title">{1}</span> ' +
                                        '<span data-notify="message">{2}</span>' +
                                    '</div>'
                    });
            }
        });