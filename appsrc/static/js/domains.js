var domains;
$(document).ready(function () {
    domains = {
        _init: false,
        domainValidate : /^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9](?:\.[a-zA-Z]{2,})+$/ ,
        init: function () {
            if (this._init) return;
            this.bind(function () {
                log.d("Domains.js loaded");
            });
            this._init = true;
        },
        bind: function (c) {
            c = c || null;

            if (typeof c === "function")
                c();

        },
        settings: {
            GetDomain: "/domain/id/",   // {id}
            SaveDomain: "",
            DeleteDomain: "",
            formdomain : "#form_domain"
        }
    };

    domains.getDomain = function(id){
        log.d("Get Domain ", id);
        $.ajax({
            url: domains.settings.GetDomain+id,
            dataType: "json",
            // data: $('form').serialize(),
            type: 'GET',
            success: function(response) {
                //response = JSON.parse(response);
                log.d("Response : ", response.data[0]);
                ShowForm(true)
                $('#id').val(response.data[0][0]);
                $('#domain').val(response.data[0][1]);
                setValidation();
            },
            error: function(error) {
                console.log(error);
            }
        });
    };

    domains.delDomain = function(){
        if ($('#id').val() === "0") return;
        r = confirm("Confirm delete of this domain "+$('#domain').val()+" and all its email addresses");
        if (r){
            $('#_method').val("DELETE");
            domains.submit();
            //window.location.replace("/managedomains");
            //window.location.href = "/managedomains";
            //$(location).attr('href','/managedomains');
        }
        ShowForm(false);
    }

     domains.newDomain = function(){
         ShowForm();
         resetForm();
         ShowForm(true);
         $('#domain').focus();
         setValidation();
     };

     domains.submit = function(){
        if ( $('#_domain_form').valid() ){
            log.d( $('#_domain_form').serialize() )
            $('#_domain_form').submit();
            ShowForm(false);
        }
     };

     domains.clear = function(){
         ShowForm(false);
     };

    domains.init();

    function resetForm(){
        $('#id').val("0");
        $('#domain').val("");
    }

    function ShowForm(s){
        (s) ? $(domains.settings.formdomain).removeClass('hide') : $(domains.settings.formdomain).addClass('hide');
    }

    jQuery.validator.addMethod("vdomain", function(value, element) {
        return this.optional(element) || domains.domainValidate.test(value);
    }, "Please specify a vaild domain");

    function setValidation() {
        $.validator.setDefaults({debug: false});
        
        $('#_domain_form').validate({
            rules: {
                ignore: ':not(select:hidden, input:visible, textarea:visible)',
                name: {
                    required: true,
                    vdomain: true
                }
            },
            messages: {
                name: {
                    required: "Enter a valid domain "
                }
            }
        });
    }

});